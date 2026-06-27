import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatMessage, ActionPreview, ActionResult, ExcelAction } from '@/types'
import { chatService } from '@/services/chatService'
import { aiProviderService, parseAIResponse, EXCEL_SYSTEM_PROMPT } from '@/services/aiProviderService'
import type { ProviderChatMessage } from '@/services/aiProviderService'
import { useProvidersStore } from '@/stores/providersStore'
import { useExcelStore } from '@/stores/excelStore'
import { PROVIDER_MAP } from '@/config/providers'

function generateId(): string {
  return Math.random().toString(36).slice(2) + Date.now().toString(36)
}

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([])
  const loading = ref(false)
  const pendingPlan = ref<ActionPreview[] | null>(null)
  const pendingMessage = ref<string>('')
  const showActionModal = ref(false)

  const hasMessages = computed(() => messages.value.length > 0)
  const lastMessage = computed(() => messages.value.at(-1))

  function addUserMessage(content: string, imageUrl?: string): ChatMessage {
    const msg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      status: 'done',
      timestamp: new Date(),
      imageUrl
    }
    messages.value.push(msg)
    return msg
  }

  function addAssistantMessage(partial?: Partial<ChatMessage>): ChatMessage {
    const msg: ChatMessage = {
      id: generateId(),
      role: 'assistant',
      content: '',
      status: 'streaming',
      timestamp: new Date(),
      ...partial
    }
    messages.value.push(msg)
    return msg
  }

  function updateMessage(id: string, patch: Partial<ChatMessage>): void {
    const idx = messages.value.findIndex((m) => m.id === id)
    if (idx === -1) return
    const merged = { ...messages.value[idx], ...patch }
    
    if (merged.status === 'done' && !merged.content?.trim()) {
      merged.content = 'No response was received from the AI. Please check your provider settings or try again.'
    }
    messages.value[idx] = merged
  }

  

  async function sendViaProvider(content: string, assistantMsgId: string, imageUrl?: string): Promise<void> {
    const providersStore = useProvidersStore()
    const excelStore = useExcelStore()
    const ap = providersStore.active!
    const cfg = providersStore.getConfig(ap.providerId)
    const def = PROVIDER_MAP[ap.providerId]

    const systemPrompt = EXCEL_SYSTEM_PROMPT
      .replace('{workbook_name}', excelStore.workbookName || 'None')
      .replace('{sheet_name}', excelStore.activeSheet || 'None')
      .replace('{selected_range}', excelStore.selectedRange || 'None')
      .replace('{used_range}', excelStore.usedRange || 'None')
      .replace('{available_sheets}', JSON.stringify(excelStore.availableSheets || []))

    const history: ProviderChatMessage[] = [
      { role: 'system', content: systemPrompt }
    ]
    const recent = messages.value.slice(-11, -1) 
    for (const m of recent) {
      if (m.role === 'user' || m.role === 'assistant') {
        history.push({ role: m.role, content: m.content, imageUrl: m.imageUrl })
      }
    }
    history.push({ role: 'user', content, imageUrl })

    const rawText = await aiProviderService.chat(
      history,
      ap.providerId,
      ap.modelId,
      def.requiresNoKey ? 'ollama' : cfg.apiKey,
      cfg.customBaseUrl || undefined
    )

    if (!rawText.trim()) {
      updateMessage(assistantMsgId, {
        content: 'The model returned an empty response. Try rephrasing your message or check the model settings.',
        status: 'done'
      })
      return
    }

    const { message, actions } = parseAIResponse(rawText)

    if (actions && actions.length > 0) {
      
      const plan: ActionPreview[] = actions.map((a) => ({
        action: a as ExcelAction,
        is_valid: true,
        error_message: null
      }))

      updateMessage(assistantMsgId, {
        content: message,
        status: 'done',
        plan,
        allValid: true
      })

      pendingPlan.value = plan
      pendingMessage.value = content
      showActionModal.value = true
    } else {
      updateMessage(assistantMsgId, { content: message, status: 'done' })
    }
  }

  

  async function sendViaBackend(content: string, assistantMsgId: string): Promise<void> {
    const response = await chatService.sendMessage(content)
    const summary = buildPlanSummary(response.plan)

    updateMessage(assistantMsgId, {
      content: summary,
      status: 'done',
      plan: response.plan,
      allValid: response.all_valid
    })

    if (response.plan.length > 0) {
      pendingPlan.value = response.plan
      pendingMessage.value = content
      showActionModal.value = true
    }
  }

  

  async function sendMessage(content: string, imageUrl?: string): Promise<void> {
    if ((!content.trim() && !imageUrl) || loading.value) return

    loading.value = true
    addUserMessage(content, imageUrl)
    const assistantMsg = addAssistantMessage()

    try {
      const excelStore = useExcelStore()
      await excelStore.refreshState()
      
      const providersStore = useProvidersStore()
      if (providersStore.active) {
        await sendViaProvider(content, assistantMsg.id, imageUrl)
      } else {
        await sendViaBackend(content, assistantMsg.id)
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err)
      updateMessage(assistantMsg.id, {
        content: `Error: ${msg}. Please check your API key or backend connection.`,
        status: 'error'
      })
    } finally {
      loading.value = false
    }
  }

  

  async function executeApprovedPlan(actions: ExcelAction[]): Promise<void> {
    const actionsPlan = pendingPlan.value || []
    showActionModal.value = false
    loading.value = true

    const execMsg = addAssistantMessage({
      content: `Preparing to execute ${actions.length} action(s)...`,
      status: 'streaming',
      plan: actionsPlan,
      results: []
    })

    const results: ActionResult[] = []
    let successCount = 0
    let failureCount = 0

    try {
      for (let i = 0; i < actions.length; i++) {
        const action = actions[i]
        const actionName = formatActionName(action.action)
        
        updateMessage(execMsg.id, {
          content: `Executing action ${i + 1} of ${actions.length}: **${actionName}**...`
        })

        const response = await chatService.executeActions([action])
        const singleResult = response.results[0]
        
        results.push(singleResult)
        if (singleResult.success) {
          successCount++
        } else {
          failureCount++
        }

        updateMessage(execMsg.id, {
          results: [...results]
        })
      }

      const summary = buildExecutionSummary(results, successCount, failureCount)
      updateMessage(execMsg.id, {
        content: summary,
        status: 'done'
      })
    } catch (err) {
      updateMessage(execMsg.id, {
        content: 'Execution failed. Please check Excel is open and accessible.',
        status: 'error'
      })
    } finally {
      loading.value = false
      pendingPlan.value = null
      pendingMessage.value = ''
    }
  }

  function rejectPlan(): void {
    showActionModal.value = false
    pendingPlan.value = null
    pendingMessage.value = ''

    addAssistantMessage({
      content: 'Actions cancelled. No changes were made to your spreadsheet.',
      status: 'done'
    })
  }

  function clearConversation(): void {
    messages.value = []
    pendingPlan.value = null
    pendingMessage.value = ''
    showActionModal.value = false
  }

  function buildPlanSummary(plan: ActionPreview[]): string {
    if (plan.length === 0) {
      return [
        "I received your message but couldn't identify specific Excel actions to perform.",
        '',
        'Try phrasing your request more specifically, for example:',
        '- *"Write 100 to cell A1"*',
        '- *"Make A1:D1 bold"*',
        '- *"Apply formula =SUM(A1:A10) to A11"*',
        '',
        'Or connect an AI provider in **Settings → Integrations** to enable full natural language understanding.'
      ].join('\n')
    }
    const valid = plan.filter((p) => p.is_valid).length
    const total = plan.length
    const actionNames = plan.map((p) => formatActionName(p.action.action as string)).join(', ')
    return `I've prepared ${total} action${total > 1 ? 's' : ''} for your spreadsheet: **${actionNames}**.\n\n${valid < total ? `⚠ ${total - valid} action(s) have validation issues.` : 'All actions are ready to execute.'}\n\nPlease review and approve to apply changes.`
  }

  function buildExecutionSummary(results: ActionResult[], successes: number, failures: number): string {
    if (failures === 0) return `✓ All ${successes} action${successes > 1 ? 's' : ''} executed successfully in Excel.`
    return `Completed with ${successes} success${successes !== 1 ? 'es' : ''} and ${failures} failure${failures !== 1 ? 's' : ''}. Check the details below.`
  }

  function formatActionName(action: string): string {
    return action.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
  }

  return {
    messages,
    loading,
    pendingPlan,
    pendingMessage,
    showActionModal,
    hasMessages,
    lastMessage,
    sendMessage,
    executeApprovedPlan,
    rejectPlan,
    clearConversation
  }
})
