import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { WorkbookContext, HealthResponse } from '@/types'
import { excelService } from '@/services/excelService'

export const useExcelStore = defineStore('excel', () => {
  const workbookName = ref<string | null>(null)
  const activeSheet = ref<string | null>(null)
  const selectedRange = ref<string | null>(null)
  const availableSheets = ref<string[]>([])
  const excelRunning = ref(false)
  const backendHealthy = ref(false)
  const connectionError = ref<string | null>(null)
  const lastChecked = ref<Date | null>(null)

  const isConnected = computed(() => backendHealthy.value && excelRunning.value)
  const hasWorkbook = computed(() => workbookName.value !== null)

  async function checkHealth(): Promise<HealthResponse> {
    try {
      const health = await excelService.getHealth()
      backendHealthy.value = health.status === 'healthy'
      excelRunning.value = health.excel_running
      connectionError.value = null
      lastChecked.value = new Date()
      return health
    } catch (err) {
      backendHealthy.value = false
      excelRunning.value = false
      connectionError.value = 'Cannot reach backend server'
      throw err
    }
  }

  async function refreshState(): Promise<void> {
    try {
      const ctx = await excelService.getState()
      applyContext(ctx)
    } catch {
      // Excel might not have a workbook open — ignore
    }
  }

  function applyContext(ctx: WorkbookContext): void {
    workbookName.value = ctx.workbook_name
    activeSheet.value = ctx.sheet_name
    selectedRange.value = ctx.selected_range
    availableSheets.value = ctx.available_sheets
  }

  function applyWebSocketState(state: WorkbookContext): void {
    applyContext(state)
  }

  return {
    workbookName,
    activeSheet,
    selectedRange,
    availableSheets,
    excelRunning,
    backendHealthy,
    connectionError,
    lastChecked,
    isConnected,
    hasWorkbook,
    checkHealth,
    refreshState,
    applyWebSocketState
  }
})

