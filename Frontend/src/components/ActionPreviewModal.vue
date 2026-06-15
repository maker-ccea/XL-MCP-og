<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { X, Play, Ban, AlertTriangle, CheckCircle2, GripVertical } from '@lucide/vue'
import type { ActionPreview } from '@/types'
import ActionCard from './ActionCard.vue'

interface Props {
  open: boolean
  plan: ActionPreview[]
  allValid: boolean
  originalMessage?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  approve: [actions: ActionPreview['action'][]]
  reject: []
}>()

const localPlan = ref<ActionPreview[]>([])
const draggedIdx = ref<number | null>(null)

watch(() => props.plan, (newPlan) => {
  localPlan.value = [...newPlan]
}, { immediate: true })

const validCount = computed(() => localPlan.value.filter((p) => p.is_valid).length)
const invalidCount = computed(() => localPlan.value.filter((p) => !p.is_valid).length)

function handleApprove(): void {
  const actions = localPlan.value.filter((p) => p.is_valid).map((p) => p.action)
  emit('approve', actions)
}

function onDragStart(idx: number) {
  draggedIdx.value = idx
}

function onDragOver(event: DragEvent, idx: number) {
  event.preventDefault()
}

function onDrop(idx: number) {
  if (draggedIdx.value === null || draggedIdx.value === idx) return
  
  const planCopy = [...localPlan.value]
  const [removed] = planCopy.splice(draggedIdx.value, 1)
  planCopy.splice(idx, 0, removed)
  localPlan.value = planCopy
  
  draggedIdx.value = null
}

function formatActionName(action: string): string {
  return action.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}
</script>

<template>
  <Transition name="modal">
    <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-6">
      
      <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" @click="emit('reject')" />

      
      <div class="relative z-10 w-full max-w-[540px] bg-surface rounded-2xl shadow-2xl border border-outline-variant/30 overflow-hidden">
        
        <div class="flex items-center justify-between px-6 py-4 border-b border-outline-variant/20">
          <div>
            <h2 class="text-[15px] font-semibold text-on-surface">Action Preview</h2>
            <p class="text-card-body text-on-surface-variant mt-0.5">
              {{ plan.length }} action{{ plan.length !== 1 ? 's' : '' }} planned
              <span v-if="!allValid" class="text-amber-600"> · {{ invalidCount }} invalid</span>
            </p>
          </div>
          <button class="p-1.5 rounded-lg hover:bg-surface-container-high text-on-surface-variant transition-colors" @click="emit('reject')">
            <X :size="16" />
          </button>
        </div>

        
        <div v-if="originalMessage" class="mx-6 mt-4 px-4 py-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
          <p class="text-label-caps text-label-caps text-on-surface-variant/60 uppercase mb-1">Your request</p>
          <p class="text-card-title text-on-surface italic">"{{ originalMessage }}"</p>
        </div>

        
        <div
          v-if="!allValid"
          class="mx-6 mt-3 flex items-center gap-2 px-4 py-2.5 bg-amber-50 border border-amber-200 rounded-xl"
        >
          <AlertTriangle :size="15" class="text-amber-600 shrink-0" />
          <p class="text-card-body text-amber-800">
            {{ invalidCount }} action{{ invalidCount !== 1 ? 's' : '' }} failed validation and will be skipped.
          </p>
        </div>
        <div
          v-else
          class="mx-6 mt-3 flex items-center gap-2 px-4 py-2.5 bg-emerald-50 border border-emerald-200 rounded-xl"
        >
          <CheckCircle2 :size="15" class="text-emerald-600 shrink-0" />
          <p class="text-card-body text-emerald-800">All actions validated and ready to execute.</p>
        </div>

        
        <div class="px-6 py-4 space-y-2 max-h-[280px] overflow-y-auto">
          <div
            v-for="(preview, idx) in localPlan"
            :key="idx"
            draggable="true"
            @dragstart="onDragStart(idx)"
            @dragover="onDragOver($event, idx)"
            @drop="onDrop(idx)"
            class="flex items-center gap-2 transition-all p-1 rounded-lg border border-transparent hover:border-outline-variant/20 hover:bg-surface-container-low/30"
            :class="draggedIdx === idx ? 'opacity-40 scale-[0.98]' : ''"
          >
            
            <div class="cursor-grab active:cursor-grabbing text-on-surface-variant/40 hover:text-on-surface-variant/85 transition-colors shrink-0">
              <GripVertical :size="16" />
            </div>
            
            <ActionCard
              mode="preview"
              :preview="preview"
              class="flex-1"
            />
          </div>
        </div>

        
        <div class="flex items-center justify-between px-6 py-4 border-t border-outline-variant/20 bg-surface-container-low/40">
          <p class="text-card-body text-on-surface-variant/60">Changes will be applied to Excel immediately.</p>
          <div class="flex items-center gap-2">
            <button
              class="flex items-center gap-1.5 px-3 py-1.5 text-card-title text-on-surface-variant border border-outline-variant/40 rounded-lg hover:bg-surface-container-high transition-colors"
              @click="emit('reject')"
            >
              <Ban :size="13" />
              Reject
            </button>
            <button
              :disabled="validCount === 0"
              class="flex items-center gap-1.5 px-3 py-1.5 text-card-title bg-primary text-on-primary rounded-lg hover:opacity-90 transition-opacity disabled:opacity-40"
              @click="handleApprove"
            >
              <Play :size="13" />
              Approve{{ validCount < plan.length ? ` (${validCount})` : '' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: all 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; transform: scale(0.97); }
</style>

