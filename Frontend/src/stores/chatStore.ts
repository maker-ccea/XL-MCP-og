import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatMessage, ActionPreview, ActionResult, ExcelAction } from '@/types'
import { chatService } from '@/services/chatService'
import { aiProviderService, parseAIResponse, EXCEL_SYSTEM_PROMPT } from '@/services/aiProviderService'
import type { ProviderChatMessage } from '@/services/aiProviderService'
import { useProvidersStore } from '@/stores/providersStore'
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

  function addUserMessage(content: string): ChatMessage {
    const msg: ChatMessage = {
      id: generateId(),
      role: 'user',
      content,
      status: 'done',
      timestamp: new Date()
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
    // Safety net: a 'done' message must always have visible content.
    if (merged.status === 'done' && !merged.content?.trim()) {
      merged.content = 'No response was received from the AI. Please check your provider settings or try again.'
    }
    messages.value[idx] = merged
  }

  // ── Frontend provider chat ─────────────────────────────────────────────────

  async function sendViaProvider(content: string, assistantMsgId: string): Promise<void> {
    const providersStore = useProvidersStore()
    const ap = providersStore.active!
    const cfg = providersStore.getConfig(ap.providerId)
    const def = PROVIDER_MAP[ap.providerId]

    // Build conversation history for context (last 10 messages)
    const history: ProviderChatMessage[] = [
      { role: 'system', content: EXCEL_SYSTEM_PROMPT }
    ]
    const recent = messages.value.slice(-11, -1) // exclude the just-added user msg
    for (const m of recent) {
      if (m.role === 'user' || m.role === 'assistant') {
        history.push({ role: m.role, content: m.content })
      }
    }
    history.push({ role: 'user', content })

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
      // Convert raw action objects to ActionPreview (optimistic validity)
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

  // ── Backend chat ───────────────────────────────────────────────────────────

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

  // ── Main sendMessage ───────────────────────────────────────────────────────

  async function sendMessage(content: string): Promise<void> {
    if (!content.trim() || loading.value) return

    loading.value = true
    addUserMessage(content)
    const assistantMsg = addAssistantMessage()

    try {
      const providersStore = useProvidersStore()
      if (providersStore.active) {
        await sendViaProvider(content, assistantMsg.id)
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

  // ── Execute & lifecycle ────────────────────────────────────────────────────

  async function executeApprovedPlan(actions: ExcelAction[]): Promise<void> {
    showActionModal.value = false
    loading.value = true

    const execMsg = addAssistantMessage({ content: 'Executing actions in Excel…', status: 'streaming' })

    try {
      const result = await chatService.executeActions(actions)
      const summary = buildExecutionSummary(result.results, result.success_count, result.failure_count)

      updateMessage(execMsg.id, {
        content: summary,
        status: 'done',
        results: result.results
      })
    } catch {
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
