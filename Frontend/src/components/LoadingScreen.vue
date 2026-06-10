<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Sparkles, Loader2 } from '@lucide/vue'

interface Props {
  backendStatus: 'checking' | 'connected' | 'failed'
  excelStatus: 'checking' | 'connected' | 'not_running' | 'failed'
}

const props = defineProps<Props>()

const dots = ref('.')
let dotInterval: ReturnType<typeof setInterval>

onMounted(() => {
  dotInterval = setInterval(() => {
    dots.value = dots.value.length >= 3 ? '.' : dots.value + '.'
  }, 400)
  return () => clearInterval(dotInterval)
})

function statusIcon(status: string): string {
  if (status === 'connected') return '✓'
  if (status === 'failed' || status === 'not_running') return '✗'
  return '...'
}

function statusColor(status: string): string {
  if (status === 'connected') return 'text-emerald-600'
  if (status === 'failed' || status === 'not_running') return 'text-red-500'
  return 'text-on-surface-variant'
}
</script>

<template>
  <div class="h-screen w-screen bg-background flex flex-col items-center justify-center gap-8">
    <!-- Logo -->
    <div class="flex flex-col items-center gap-4">
      <div class="w-16 h-16 rounded-full bg-surface border border-custom-border-light flex items-center justify-center shadow-sm">
        <Sparkles :size="28" class="text-secondary" />
      </div>
      <div>
        <h1 class="text-display-welcome font-display-welcome text-on-surface text-center">XL-MCP</h1>
        <p class="text-card-body text-on-surface-variant text-center mt-1">AI Workspace for Excel</p>
      </div>
    </div>

    <!-- Status checks -->
    <div class="w-[280px] space-y-2">
      <div class="flex items-center justify-between px-4 py-2.5 bg-surface rounded-xl border border-outline-variant/40">
        <span class="text-card-title text-on-surface">Backend server</span>
        <div class="flex items-center gap-2">
          <Loader2 v-if="backendStatus === 'checking'" :size="14" class="text-on-surface-variant animate-spin" />
          <span v-else :class="['text-card-title font-medium', statusColor(backendStatus)]">
            {{ statusIcon(backendStatus) }}
          </span>
          <span :class="['text-card-body', statusColor(backendStatus)]">
            {{ backendStatus === 'checking' ? 'Connecting' : backendStatus === 'connected' ? 'Online' : 'Offline' }}
          </span>
        </div>
      </div>

      <div class="flex items-center justify-between px-4 py-2.5 bg-surface rounded-xl border border-outline-variant/40">
        <span class="text-card-title text-on-surface">Microsoft Excel</span>
        <div class="flex items-center gap-2">
          <Loader2 v-if="excelStatus === 'checking'" :size="14" class="text-on-surface-variant animate-spin" />
          <span v-else :class="['text-card-title font-medium', statusColor(excelStatus)]">
            {{ statusIcon(excelStatus) }}
          </span>
          <span :class="['text-card-body', statusColor(excelStatus)]">
            {{ excelStatus === 'checking' ? 'Detecting' : excelStatus === 'connected' ? 'Running' : 'Not open' }}
          </span>
        </div>
      </div>
    </div>

    <p class="text-card-body text-on-surface-variant/60">Starting up{{ dots }}</p>
  </div>
</template>

