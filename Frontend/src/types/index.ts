

export interface SelectionData {
  headers: string[]
  row_labels: string[]
  values: any[][]
  total_rows: number
  total_cols: number
}

export interface WorkbookContext {
  workbook_name: string | null
  sheet_name: string | null
  selected_range: string | null
  used_range: string | null
  available_sheets: string[]
  selection_data?: SelectionData | null
}

export interface HealthResponse {
  status: string
  excel_running: boolean
}

export interface ChatRequest {
  message: string
}

export interface ExcelAction {
  action: string
  [key: string]: unknown
}

export interface ActionPreview {
  action: ExcelAction
  is_valid: boolean
  error_message: string | null
}

export interface ChatResponse {
  message: string
  plan: ActionPreview[]
  all_valid: boolean
}

export interface ExecuteRequest {
  actions: ExcelAction[]
}

export interface ActionResult {
  action_type: string
  success: boolean
  error: string | null
  data: unknown | null
}

export interface ExecuteResponse {
  results: ActionResult[]
  success_count: number
  failure_count: number
}

export interface HistoryEntry {
  id: string
  timestamp: string
  message: string
  actions: ExcelAction[]
  results: ActionResult[]
  status: 'success' | 'partial' | 'failed'
}



export type MessageRole = 'user' | 'assistant' | 'system'
export type MessageStatus = 'sending' | 'streaming' | 'done' | 'error'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  status: MessageStatus
  timestamp: Date
  plan?: ActionPreview[]
  results?: ActionResult[]
  allValid?: boolean
  imageUrl?: string
}

export type Theme = 'light' | 'dark' | 'system' | 'nord' | 'cyberpunk' | 'forest-green'
export type AIModel = 'xl-mcp-pro' | 'xl-mcp-lite' | 'gpt-4'
export type AvatarColor = 'zinc' | 'rose' | 'amber' | 'emerald' | 'sky' | 'violet' | 'orange'

export interface LocalProfile {
  displayName: string
  role: string
  bio: string
  avatarColor: AvatarColor
}

export interface KeyboardShortcuts {
  toggleSidebar: string
  clearChat: string
  commandPalette: string
  toggleExcel: string
}

export interface AppSettings {
  profile: LocalProfile
  theme: Theme
  model: AIModel
  language: string
  actionPreview: boolean
  autoSuggest: boolean
  formulaExplanations: boolean
  streamingResponses: boolean
  activeSheetContext: boolean
  workbookNameContext: boolean
  maxContextRows: number
  apiKey: string
  shortcuts: KeyboardShortcuts
}


export type { ProviderID } from '@/config/providers'

export interface WebSocketStateEvent {
  event: 'state_changed'
  state: WorkbookContext
}



export interface AIRequestOptions {
  url: string
  method?: string
  headers: Record<string, string>
  body: unknown
}

export interface AIRequestResult {
  ok: boolean
  status: number
  data: unknown
  error?: string
}

export interface ElectronAPI {
  getAppVersion: () => Promise<string>
  aiRequest: (opts: AIRequestOptions) => Promise<AIRequestResult>
  onBackendStatus: (callback: (status: string) => void) => void
  removeAllListeners: (channel: string) => void
}

declare global {
  interface Window {
    electronAPI: ElectronAPI
  }
}

