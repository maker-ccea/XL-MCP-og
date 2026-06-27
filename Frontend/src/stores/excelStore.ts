import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { WorkbookContext, HealthResponse, SelectionData } from '@/types'
import { excelService } from '@/services/excelService'

export const useExcelStore = defineStore('excel', () => {
  const workbookName = ref<string | null>(null)
  const activeSheet = ref<string | null>(null)
  const selectedRange = ref<string | null>(null)
  const usedRange = ref<string | null>(null)
  const availableSheets = ref<string[]>([])
  const selectionData = ref<SelectionData | null>(null)
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
      
    }
  }

  function applyContext(ctx: WorkbookContext): void {
    workbookName.value = ctx.workbook_name
    activeSheet.value = ctx.sheet_name
    selectedRange.value = ctx.selected_range
    usedRange.value = ctx.used_range
    availableSheets.value = ctx.available_sheets
    selectionData.value = ctx.selection_data || null
  }

  function applyWebSocketState(state: WorkbookContext): void {
    applyContext(state)
  }

  return {
    workbookName,
    activeSheet,
    selectedRange,
    usedRange,
    availableSheets,
    selectionData,
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

