import type { ProviderID } from '@/config/providers'
import { PROVIDER_MAP } from '@/config/providers'

export interface ProviderChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface TestResult {
  success: boolean
  latencyMs: number
  error?: string
  modelUsed?: string
}

export interface ParsedAIResponse {
  message: string
  actions: Record<string, unknown>[] | null
}

// ─── System prompt ────────────────────────────────────────────────────────────

export const EXCEL_SYSTEM_PROMPT = `You are XL-MCP, an expert AI assistant integrated with Microsoft Excel. You help users analyze spreadsheet data, write formulas, automate tasks, and perform operations through natural language.

When the user asks you to perform operations IN Excel (writing values, applying formulas, formatting, creating sheets, etc.), always include a structured actions block.

Format your response:
1. A clear explanation of what you will do
2. The actions block (only when Excel operations are needed):

\`\`\`excel-actions
[{"action": "action_name", ...params}]
\`\`\`

Available actions:
- {"action": "write_cell", "cell": "A1", "value": "Hello"}
- {"action": "write_range", "range": "A1", "data": [["Name", "Score"], ["Alice", 95]]}
- {"action": "apply_formula", "cell": "B2", "formula": "=SUM(A1:A10)"}
- {"action": "fill_formula", "range": "B2:B10", "formula": "=A2*1.1"}
- {"action": "clear_cells", "range": "A1:D10"}
- {"action": "set_bold", "range": "A1:D1", "bold": true}
- {"action": "set_italic", "range": "A1", "italic": true}
- {"action": "set_font_size", "range": "A1:D1", "size": 14}
- {"action": "set_font_color", "range": "A1", "color": "#FF0000"}
- {"action": "set_background_color", "range": "A1:D1", "color": "#F0F0F0"}
- {"action": "auto_fit_columns", "range": "A:D"}
- {"action": "create_sheet", "name": "Summary"}
- {"action": "rename_sheet", "old_name": "Sheet1", "new_name": "Data"}
- {"action": "delete_sheet", "name": "OldSheet"}
- {"action": "activate_sheet", "name": "Sheet2"}
- {"action": "save_workbook"}
- {"action": "create_chart", "data_range": "A1:E4", "chart_type": "column", "title": "Sales Overview"}
  Supported chart_type values: column, column_stacked, bar, bar_stacked, line, line_markers, pie, scatter, area, area_stacked, doughnut
- {"action": "delete_chart", "name": "Sales Overview"}
- {"action": "update_chart_title", "name": "Chart 1", "title": "New Title"}

For analysis, explanations, formula suggestions, or questions that don't require modifying Excel, respond conversationally without an actions block.`

// ─── IPC bridge ───────────────────────────────────────────────────────────────
// All requests go through Electron main process to avoid CORS restrictions.

async function ipcPost(
  url: string,
  headers: Record<string, string>,
  body: unknown
): Promise<unknown> {
  const api = window.electronAPI
  if (!api?.aiRequest) {
    throw new Error('AI request bridge unavailable — not running inside Electron.')
  }

  const result = await api.aiRequest({ url, method: 'POST', headers, body })

  if (!result.ok) {
    throw new Error(result.error ?? `HTTP ${result.status}`)
  }

  return result.data
}

// ─── Provider-specific call builders ─────────────────────────────────────────

async function callOpenAI(
  messages: ProviderChatMessage[],
  modelId: string,
  apiKey: string,
  baseUrl: string
): Promise<string> {
  const data = await ipcPost(
    `${baseUrl}/chat/completions`,
    { Authorization: `Bearer ${apiKey}` },
    {
      model: modelId,
      messages: messages.map((m) => ({ role: m.role, content: m.content })),
      max_tokens: 2048,
      temperature: 0.4
    }
  ) as Record<string, unknown>

  const text = (data?.choices as Array<{ message: { content: string } }>)?.[0]?.message?.content
  if (text == null) throw new Error('Response missing choices[0].message.content — check model ID and API key.')
  return text
}

async function callAnthropic(
  messages: ProviderChatMessage[],
  modelId: string,
  apiKey: string
): Promise<string> {
  const systemMsg = messages.find((m) => m.role === 'system')?.content ?? ''
  const convoMsgs = messages
    .filter((m) => m.role !== 'system')
    .map((m) => ({ role: m.role as 'user' | 'assistant', content: m.content }))

  const data = await ipcPost(
    'https://api.anthropic.com/v1/messages',
    {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01'
    },
    {
      model: modelId,
      max_tokens: 2048,
      system: systemMsg,
      messages: convoMsgs
    }
  ) as Record<string, unknown>

  const text = (data?.content as Array<{ text: string }>)?.[0]?.text
  if (text == null) throw new Error('Anthropic response missing content[0].text — check model ID and API key.')
  return text
}

async function callGoogle(
  messages: ProviderChatMessage[],
  modelId: string,
  apiKey: string
): Promise<string> {
  const systemMsg = messages.find((m) => m.role === 'system')?.content ?? ''
  const convoMsgs = messages
    .filter((m) => m.role !== 'system')
    .map((m) => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }]
    }))

  const body: Record<string, unknown> = {
    contents: convoMsgs,
    generationConfig: { maxOutputTokens: 2048, temperature: 0.4 }
  }
  if (systemMsg) {
    body.system_instruction = { parts: [{ text: systemMsg }] }
  }

  const data = await ipcPost(
    `https://generativelanguage.googleapis.com/v1beta/models/${modelId}:generateContent?key=${apiKey}`,
    {},
    body
  ) as Record<string, unknown>

  const text = (
    data?.candidates as Array<{ content: { parts: Array<{ text: string }> } }>
  )?.[0]?.content?.parts?.[0]?.text
  if (text == null) throw new Error('Google response missing candidates[0].content.parts[0].text — check model ID and API key.')
  return text
}

// ─── Response parser ──────────────────────────────────────────────────────────

export function parseAIResponse(raw: string): ParsedAIResponse {
  const actionMatch = raw.match(/```excel-actions\n([\s\S]*?)```/)
  if (!actionMatch) {
    return { message: raw.trim(), actions: null }
  }

  const message = raw.replace(/```excel-actions\n[\s\S]*?```/g, '').trim()
  let actions: Record<string, unknown>[] | null = null

  try {
    const parsed = JSON.parse(actionMatch[1].trim())
    actions = Array.isArray(parsed) ? parsed : [parsed]
  } catch {
    // malformed JSON — treat whole response as plain text
  }

  return {
    message: message || 'Here are the actions I prepared for your spreadsheet.',
    actions
  }
}

// ─── Public API ───────────────────────────────────────────────────────────────

export const aiProviderService = {
  async chat(
    messages: ProviderChatMessage[],
    providerId: ProviderID,
    modelId: string,
    apiKey: string,
    customBaseUrl?: string
  ): Promise<string> {
    const def = PROVIDER_MAP[providerId]
    const baseUrl = customBaseUrl || def.baseUrl

    switch (def.apiFormat) {
      case 'anthropic':
        return callAnthropic(messages, modelId, apiKey)
      case 'google':
        return callGoogle(messages, modelId, apiKey)
      default:
        return callOpenAI(messages, modelId, apiKey, baseUrl)
    }
  },

  async testConnection(
    providerId: ProviderID,
    modelId: string,
    apiKey: string,
    customBaseUrl?: string
  ): Promise<TestResult> {
    const start = Date.now()

    try {
      const text = await aiProviderService.chat(
        [{ role: 'user', content: 'Reply with only the word: connected' }],
        providerId,
        modelId,
        apiKey,
        customBaseUrl
      )

      return {
        success: !!text.trim(),
        latencyMs: Date.now() - start,
        modelUsed: modelId,
        error: text.trim() ? undefined : 'Empty response from model'
      }
    } catch (err: unknown) {
      return {
        success: false,
        latencyMs: Date.now() - start,
        error: err instanceof Error ? err.message : String(err)
      }
    }
  }
}
