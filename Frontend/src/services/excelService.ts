import axios from 'axios'
import type { WorkbookContext, HealthResponse, HistoryEntry } from '@/types'

const BASE_URL = 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

export const excelService = {
  async getHealth(): Promise<HealthResponse> {
    const { data } = await api.get<HealthResponse>('/health')
    return data
  },

  async getState(): Promise<WorkbookContext> {
    const { data } = await api.get<WorkbookContext>('/state')
    return data
  },

  async getHistory(): Promise<HistoryEntry[]> {
    const { data } = await api.get<HistoryEntry[]>('/history')
    return data
  },

  async undoAction(actionId: string): Promise<any> {
    const { data } = await api.post(`/undo/${actionId}`)
    return data
  },

  createWebSocket(): WebSocket {
    return new WebSocket('ws://127.0.0.1:8000/ws/state')
  }
}

