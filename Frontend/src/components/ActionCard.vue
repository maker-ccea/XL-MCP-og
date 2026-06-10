<script setup lang="ts">
import { computed } from 'vue'
import { CheckCircle2, XCircle, ChevronDown, ChevronRight } from '@lucide/vue'
import { ref } from 'vue'
import type { ActionResult, ActionPreview } from '@/types'

interface Props {
  result?: ActionResult
  preview?: ActionPreview
  mode?: 'result' | 'preview'
}

const props = withDefaults(defineProps<Props>(), { mode: 'result' })

const expanded = ref(false)

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
    <button
      class="w-full flex items-center gap-2 px-3 py-2 text-left"
      @click="expanded = !expanded"
    >
      <CheckCircle2 v-if="success" :size="14" class="text-emerald-600 shrink-0" />
      <XCircle v-else :size="14" class="text-red-500 shrink-0" />
      <span :class="['text-card-title flex-1', success ? 'text-emerald-800' : 'text-red-800']">
        {{ actionName }}
      </span>
      <component :is="expanded ? ChevronDown : ChevronRight" :size="13" :class="success ? 'text-emerald-500' : 'text-red-400'" />
    </button>

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

