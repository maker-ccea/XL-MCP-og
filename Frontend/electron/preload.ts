import { contextBridge, ipcRenderer } from 'electron'

interface AIRequestOptions {
  url: string
  method?: string
  headers: Record<string, string>
  body: unknown
}

interface AIRequestResult {
  ok: boolean
  status: number
  data: unknown
  error?: string
}

contextBridge.exposeInMainWorld('electronAPI', {
  getAppVersion: (): Promise<string> =>
    ipcRenderer.invoke('get-app-version'),

  // Proxy AI API calls through Node.js main process to bypass CORS
  aiRequest: (opts: AIRequestOptions): Promise<AIRequestResult> =>
    ipcRenderer.invoke('ai:request', {
      url: opts.url,
      method: opts.method ?? 'POST',
      headers: { 'Content-Type': 'application/json', ...opts.headers },
      body: JSON.stringify(opts.body)
    }),

  onBackendStatus: (callback: (status: string) => void) => {
    ipcRenderer.on('backend-status', (_event, status) => callback(status))
  },

  removeAllListeners: (channel: string) => {
    ipcRenderer.removeAllListeners(channel)
  }
})
