import { ref, onUnmounted } from 'vue'
import type { WebSocketStateEvent } from '@/types'
import { useExcelStore } from '@/stores/excelStore'

export function useWebSocket() {
  const excelStore = useExcelStore()
  const socket = ref<WebSocket | null>(null)
  const connected = ref(false)
  let reconnectTimer: ReturnType<typeof setTimeout> | null = null

  function connect(): void {
    if (socket.value?.readyState === WebSocket.OPEN) return

    try {
      socket.value = new WebSocket('ws://127.0.0.1:8000/ws/state')

      socket.value.onopen = () => {
        connected.value = true
        if (reconnectTimer) {
          clearTimeout(reconnectTimer)
          reconnectTimer = null
        }
      }

      socket.value.onmessage = (event: MessageEvent) => {
        try {
          const data = JSON.parse(event.data) as WebSocketStateEvent
          if (data.event === 'state_changed') {
            excelStore.applyWebSocketState(data.state)
          }
        } catch {
          
        }
      }

      socket.value.onclose = () => {
        connected.value = false
        scheduleReconnect()
      }

      socket.value.onerror = () => {
        connected.value = false
      }
    } catch {
      scheduleReconnect()
    }
  }

  function disconnect(): void {
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    socket.value?.close()
    socket.value = null
    connected.value = false
  }

  function scheduleReconnect(): void {
    if (reconnectTimer) return
    reconnectTimer = setTimeout(() => {
      reconnectTimer = null
      connect()
    }, 3000)
  }

  onUnmounted(() => disconnect())

  return { connect, disconnect, connected }
}

