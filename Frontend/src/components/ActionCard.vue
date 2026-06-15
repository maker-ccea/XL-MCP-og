<script setup lang="ts">
import { computed, ref } from 'vue'
import { CheckCircle2, XCircle, ChevronDown, ChevronRight, RotateCcw } from '@lucide/vue'
import type { ActionResult, ActionPreview } from '@/types'
import { excelService } from '@/services/excelService'
import { useExcelStore } from '@/stores/excelStore'

interface Props {
  result?: ActionResult
  preview?: ActionPreview
  mode?: 'result' | 'preview'
}

const props = withDefaults(defineProps<Props>(), { mode: 'result' })

const expanded = ref(false)
const undone = ref(false)
const undoing = ref(false)
const excelStore = useExcelStore()

const canUndo = computed(() => {
  return props.mode === 'result' && 
         success.value && 
         props.result?.action_id && 
         !undone.value && 
         ['write_cell', 'write_range', 'clear_cells', 'apply_formula', 'fill_formula', 'remove_formula', 'set_bold', 'set_italic', 'set_font_size', 'set_font_color', 'set_background_color'].includes(props.result.action_type)
})

async function performUndo(e: Event) {
  e.stopPropagation()
  if (!props.result?.action_id || undoing.value) return
  undoing.value = true
  try {
    await excelService.undoAction(props.result.action_id)
    undone.value = true
    await excelStore.refreshState()
  } catch (err) {
    console.error('Failed to undo action:', err)
  } finally {
    undoing.value = false
  }
}

function formatActionName(action: string): string {
  return action.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

const actionName = computed(() => {
  if (props.mode === 'result' && props.result) return formatActionName(props.result.action_type)
  if (props.mode === 'preview' && props.preview) return formatActionName(props.preview.action.action)
  return 'Action'
})

const success = computed(() => {
  if (props.mode === 'result') return props.result?.success ?? false
  return props.preview?.is_valid ?? false
})

const detail = computed(() => {
  if (props.mode === 'result') {
    if (props.result?.error) return props.result.error
    if (props.result?.data) return JSON.stringify(props.result.data, null, 2)
    return null
  }
  if (props.mode === 'preview') {
    if (props.preview?.error_message) return props.preview.error_message
    const action = props.preview?.action
    if (action) {
      const { action: _a, ...rest } = action
      return Object.keys(rest).length > 0 ? JSON.stringify(rest, null, 2) : null
    }
  }
  return null
})
</script>

<template>
  <div
    :class="[
      'rounded-lg border text-card-body overflow-hidden transition-colors',
      success
        ? 'border-emerald-200 bg-emerald-50'
        : 'border-red-200 bg-red-50'
    ]"
  >
    <div class="w-full flex items-center justify-between px-3 py-2">
      <div
        class="flex items-center gap-2 cursor-pointer flex-1"
        @click="expanded = !expanded"
      >
        <CheckCircle2 v-if="success" :size="14" class="text-emerald-600 shrink-0" />
        <XCircle v-else :size="14" class="text-red-500 shrink-0" />
        <span :class="['text-card-title', success ? 'text-emerald-800' : 'text-red-800']">
          {{ actionName }}
        </span>
        <span v-if="undone" class="text-[10px] bg-emerald-200 text-emerald-800 px-1.5 py-0.5 rounded font-medium ml-2">Undone</span>
        <component :is="expanded ? ChevronDown : ChevronRight" :size="13" :class="[success ? 'text-emerald-500' : 'text-red-400', 'ml-1']" />
      </div>

      
      <button
        v-if="canUndo"
        :disabled="undoing"
        @click="performUndo"
        class="p-1 px-2 rounded hover:bg-emerald-200 text-emerald-700 disabled:opacity-40 transition-all flex items-center gap-1 text-[11px] font-medium"
        title="Undo this action in Excel"
      >
        <RotateCcw :size="11" :class="undoing ? 'animate-spin' : ''" />
        Undo
      </button>
    </div>

    <Transition name="expand">
      <div v-if="expanded && detail" class="px-3 pb-2.5 pt-0">
        <pre :class="['text-[11px] font-mono rounded-md px-3 py-2 overflow-x-auto', success ? 'bg-emerald-100 text-emerald-900' : 'bg-red-100 text-red-900']">{{ detail }}</pre>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.expand-enter-active, .expand-leave-active { transition: all 0.15s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; }
.expand-enter-to, .expand-leave-from { opacity: 1; max-height: 200px; }
</style>

