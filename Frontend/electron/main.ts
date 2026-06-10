import { app, BrowserWindow, shell, ipcMain } from 'electron'
import { join } from 'path'
import { spawn, ChildProcess } from 'child_process'
import https from 'node:https'
import http from 'node:http'

let mainWindow: BrowserWindow | null = null
let backendProcess: ChildProcess | null = null

const isDev = !app.isPackaged

// ─── AI request proxy (bypasses renderer CORS) ────────────────────────────────

interface AIRequestParams {
  url: string
  method: string
  headers: Record<string, string>
  body: string
}

interface AIRequestResult {
  ok: boolean
  status: number
  data: unknown
  error?: string
}

function makeNodeRequest(params: AIRequestParams): Promise<AIRequestResult> {
  return new Promise((resolve) => {
    let urlObj: URL
    try {
      urlObj = new URL(params.url)
    } catch {
      resolve({ ok: false, status: 0, data: null, error: `Invalid URL: ${params.url}` })
      return
    }

    const isHttps = urlObj.protocol === 'https:'
    const transport = isHttps ? https : http
    const bodyBuffer = Buffer.from(params.body, 'utf-8')

    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port ? Number(urlObj.port) : isHttps ? 443 : 80,
      path: urlObj.pathname + urlObj.search,
      method: params.method,
      headers: {
        ...params.headers,
        'Content-Length': bodyBuffer.byteLength
      }
    }

    const req = transport.request(options, (res) => {
      const chunks: Buffer[] = []
      res.on('data', (chunk: Buffer) => chunks.push(chunk))
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf-8')
        const status = res.statusCode ?? 0

        try {
          const parsed = JSON.parse(raw) as Record<string, unknown>

          if (status >= 400) {
            // Extract the most useful message across all provider error formats:
            // OpenAI / Mistral / Groq / OpenRouter: { error: { message } }
            // Anthropic:  { error: { type, message } }
            // Google:     { error: { code, message, status } }
            // Cohere:     { message }
            // Together:   { error: { message } } or { message }
            const errBlock = parsed?.error as Record<string, unknown> | undefined
            const msg: string =
              (typeof errBlock?.message === 'string' ? errBlock.message : '') ||
              (typeof parsed?.message === 'string' ? parsed.message : '') ||
              (typeof parsed?.detail === 'string' ? parsed.detail : '') ||
              ''

            const label = msg || `HTTP ${status}`
            resolve({ ok: false, status, data: parsed, error: `[${status}] ${label}` })
          } else {
            resolve({ ok: true, status, data: parsed })
          }
        } catch {
          // Non-JSON body (HTML error page, plain text, etc.)
          resolve({
            ok: false,
            status,
            data: null,
            error: `[${status}] ${raw.slice(0, 300).trim() || 'Empty response'}`
          })
        }
      })
    })

    req.setTimeout(65000, () => {
      req.destroy()
      resolve({ ok: false, status: 0, data: null, error: 'Request timed out after 60s' })
    })

    req.on('error', (err: Error) => {
      resolve({ ok: false, status: 0, data: null, error: err.message })
    })

    req.write(bodyBuffer)
    req.end()
  })
}

// ─── Backend startup ──────────────────────────────────────────────────────────

function startBackendServer(): void {
  if (!isDev) return

  try {
    const backendPath = join(__dirname, '../../../backend')
    backendProcess = spawn('python', ['-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'], {
      cwd: backendPath,
      stdio: 'pipe'
    })

    backendProcess.stdout?.on('data', (data: Buffer) => {
      console.log('[Backend]', data.toString())
    })

    backendProcess.stderr?.on('data', (data: Buffer) => {
      console.error('[Backend ERR]', data.toString())
    })

    backendProcess.on('exit', (code) => {
      console.log('[Backend] process exited with code', code)
    })
  } catch (err) {
    console.error('Failed to start backend:', err)
  }
}

// ─── Window ───────────────────────────────────────────────────────────────────

function createWindow(): void {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 1024,
    minHeight: 640,
    backgroundColor: '#f7f9fc',
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#f7f9fc',
      symbolColor: '#191c1e',
      height: 28
    },
    webPreferences: {
      preload: join(__dirname, '../preload/index.mjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    },
    show: false
  })

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show()
  })

  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools({ mode: 'detach' })
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

// ─── IPC handlers ─────────────────────────────────────────────────────────────

ipcMain.handle('get-app-version', () => app.getVersion())

ipcMain.handle('ai:request', (_event, params: AIRequestParams): Promise<AIRequestResult> => {
  return makeNodeRequest(params)
})

// ─── Lifecycle ────────────────────────────────────────────────────────────────

app.whenReady().then(() => {
  startBackendServer()
  createWindow()

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  backendProcess?.kill()
  if (process.platform !== 'darwin') app.quit()
})
