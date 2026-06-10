import axios from 'axios'
import type { ChatRequest, ChatResponse, ExecuteRequest, ExecuteResponse } from '@/types'

const BASE_URL = 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' }
})

export const chatService = {
  async sendMessage(message: string): Promise<ChatResponse> {
    const payload: ChatRequest = { message }
    const { data } = await api.post<ChatResponse>('/chat', payload)
    return data
  },

  async executeActions(actions: ExecuteRequest['actions']): Promise<ExecuteResponse> {
    const payload: ExecuteRequest = { actions }
    const { data } = await api.post<ExecuteResponse>('/execute', payload)
    return data
  }
}

