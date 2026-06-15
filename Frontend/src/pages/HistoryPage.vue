<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ArrowLeft, Clock, CheckCircle2, XCircle, AlertCircle, RefreshCw } from '@lucide/vue'
import { useRouter } from 'vue-router'
import { excelService } from '@/services/excelService'
import type { HistoryEntry } from '@/types'

const router = useRouter()
const history = ref<HistoryEntry[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

async function loadHistory(): Promise<void> {
  loading.value = true
  error.value = null
  try {
    history.value = await excelService.getHistory()
  } catch {
    error.value = 'Could not load history. Make sure the backend is running.'
  } finally {
    loading.value = false
  }
}

onMounted(loadHistory)

function formatTime(ts: string): string {
  return new Date(ts).toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function statusConfig(status: HistoryEntry['status']) {
  return {
    success: { icon: CheckCircle2, color: 'text-emerald-600', bg: 'bg-emerald-50', label: 'Success' },
    partial: { icon: AlertCircle, color: 'text-amber-600', bg: 'bg-amber-50', label: 'Partial' },
    failed: { icon: XCircle, color: 'text-red-500', bg: 'bg-red-50', label: 'Failed' }
  }[status]
}
</script>

<template>
  <div class="bg-background font-body-main text-on-surface antialiased h-screen flex flex-col overflow-hidden">
    
    <header class="flex items-center gap-4 px-8 h-16 shrink-0 border-b border-outline-variant/20">
      <button
        class="flex items-center gap-1.5 text-card-title text-on-surface-variant hover:text-on-surface transition-colors"
        @click="router.push('/')"
      >
        <ArrowLeft :size="16" />
        Back to Workspace
      </button>
      <div class="w-[1px] h-4 bg-outline-variant" />
      <h1 class="text-[18px] font-semibold text-on-surface">Action History</h1>
      <button
        class="ml-auto p-2 text-on-surface-variant hover:bg-surface-variant rounded-md transition-colors"
        :class="{ 'animate-spin': loading }"
        @click="loadHistory"
      >
        <RefreshCw :size="16" />
      </button>
    </header>

    
    <main class="flex-1 overflow-y-auto px-8 py-6">
      <div class="max-w-[760px] mx-auto">
        
        <div v-if="loading" class="flex items-center justify-center py-20 text-on-surface-variant">
          <RefreshCw :size="20" class="animate-spin mr-3" />
          Loading history...
        </div>

        
        <div v-else-if="error" class="flex flex-col items-center justify-center py-20 gap-4 text-center">
          <AlertCircle :size="32" class="text-on-surface-variant/40" />
          <p class="text-card-body text-on-surface-variant">{{ error }}</p>
          <button class="px-4 py-2 text-card-title bg-primary text-on-primary rounded-lg hover:opacity-90" @click="loadHistory">
            Retry
          </button>
        </div>

        
        <div v-else-if="history.length === 0" class="flex flex-col items-center justify-center py-20 gap-3 text-center">
          <Clock :size="36" class="text-on-surface-variant/30" />
          <p class="text-[15px] font-medium text-on-surface">No history yet</p>
          <p class="text-card-body text-on-surface-variant">Actions you perform on Excel will appear here.</p>
        </div>

        
        <div v-else class="space-y-3">
          <div
            v-for="entry in history"
            :key="entry.id"
            class="bg-surface rounded-xl border border-outline-variant/30 overflow-hidden hover:border-custom-border-light transition-colors"
          >
            
            <div class="flex items-center gap-3 px-5 py-4">
              <div :class="['w-7 h-7 rounded-full flex items-center justify-center shrink-0', statusConfig(entry.status).bg]">
                <component :is="statusConfig(entry.status).icon" :size="15" :class="statusConfig(entry.status).color" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-card-title text-on-surface truncate">{{ entry.message }}</p>
                <p class="text-card-body text-on-surface-variant">{{ formatTime(entry.timestamp) }}</p>
              </div>
              <span :class="['text-label-caps text-label-caps uppercase px-2 py-0.5 rounded-full', statusConfig(entry.status).bg, statusConfig(entry.status).color]">
                {{ statusConfig(entry.status).label }}
              </span>
            </div>

            
            <div v-if="entry.actions.length > 0" class="px-5 pb-4 flex flex-wrap gap-1.5">
              <span
                v-for="(action, idx) in entry.actions"
                :key="idx"
                class="text-[11px] font-medium px-2 py-0.5 bg-surface-container-low border border-outline-variant/30 rounded-full text-on-surface-variant"
              >
                {{ action.action.replace(/_/g, ' ') }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

