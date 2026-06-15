import { onMounted, onUnmounted } from 'vue'
import { useExcelStore } from '@/stores/excelStore'
import { useWebSocket } from './useWebSocket'

export function useExcel() {
  const excelStore = useExcelStore()
  const { connect, disconnect, connected } = useWebSocket()
  let pollInterval: ReturnType<typeof setInterval> | null = null

  async function init(): Promise<void> {
    try {
      await excelStore.checkHealth()
      await excelStore.refreshState()
      connect()
    } catch {
      
    }

    pollInterval = setInterval(async () => {
      try {
        await excelStore.checkHealth()
        if (excelStore.backendHealthy) {
          await excelStore.refreshState()
        }
      } catch {
        
      }
    }, 10_000)
  }

  function cleanup(): void {
    if (pollInterval) {
      clearInterval(pollInterval)
      pollInterval = null
    }
    disconnect()
  }

  onMounted(init)
  onUnmounted(cleanup)

  return { excelStore, connected }
}

