<script setup lang="ts">
import { AlertTriangle, RefreshCw, ArrowLeft } from '@lucide/vue'
import { useRouter } from 'vue-router'

interface Props {
  title?: string
  message?: string
  type?: 'backend' | 'excel' | 'connection' | 'general'
  retrying?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Something went wrong',
  message: 'An unexpected error occurred.',
  type: 'general',
  retrying: false
})

const emit = defineEmits<{
  retry: []
}>()

const router = useRouter()

const typeConfig = {
  backend: {
    label: 'Backend Error',
    hint: 'Make sure the Python backend is running on port 8000.',
    command: 'uvicorn main:app --host 127.0.0.1 --port 8000'
  },
  excel: {
    label: 'Excel Not Found',
    hint: 'Open Microsoft Excel before using XL-MCP.',
    command: null
  },
  connection: {
    label: 'Connection Error',
    hint: 'Check that the backend server is running and accessible.',
    command: null
  },
  general: {
    label: 'Error',
    hint: null,
    command: null
  }
}

const config = typeConfig[props.type]
</script>

<template>
  <div class="flex flex-col items-center justify-center h-full gap-6 px-8 text-center">
    <div class="w-12 h-12 rounded-full bg-error-container flex items-center justify-center">
      <AlertTriangle :size="22" class="text-on-error-container" />
    </div>

    <div class="space-y-2 max-w-sm">
      <p class="text-label-caps text-label-caps text-error uppercase tracking-wider">{{ config.label }}</p>
      <h2 class="text-[18px] font-semibold text-on-surface">{{ title }}</h2>
      <p class="text-card-body text-on-surface-variant leading-relaxed">{{ message }}</p>
      <p v-if="config.hint" class="text-card-body text-on-surface-variant/70">{{ config.hint }}</p>
    </div>

    <div v-if="config.command" class="w-full max-w-sm">
      <p class="text-label-caps text-label-caps text-on-surface-variant mb-2 uppercase">Run in terminal</p>
      <pre class="bg-primary-container text-inverse-on-surface text-[11px] font-mono rounded-xl px-4 py-3 text-left overflow-x-auto">{{ config.command }}</pre>
    </div>

    <div class="flex items-center gap-3">
      <button
        class="flex items-center gap-2 px-4 py-2 text-card-title text-on-surface-variant border border-outline-variant/40 rounded-lg hover:bg-surface-container-high transition-colors"
        @click="router.push('/')"
      >
        <ArrowLeft :size="14" />
        Back
      </button>
      <button
        :disabled="retrying"
        class="flex items-center gap-2 px-4 py-2 text-card-title bg-primary text-on-primary rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
        @click="emit('retry')"
      >
        <RefreshCw :size="14" :class="{ 'animate-spin': retrying }" />
        {{ retrying ? 'Retrying...' : 'Retry' }}
      </button>
    </div>
  </div>
</template>

