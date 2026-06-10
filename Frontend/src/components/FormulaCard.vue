<script setup lang="ts">
import { ref, computed } from 'vue'
import { Copy, Check, Play, ChevronDown, ChevronUp, Sparkles } from '@lucide/vue'

interface Props {
  formula: string
  explanation?: string
  targetCell?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{ apply: [formula: string, cell: string] }>()

const copied = ref(false)
const showExplanation = ref(false)

async function copyFormula(): Promise<void> {
  await navigator.clipboard.writeText(props.formula)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}

function applyFormula(): void {
  emit('apply', props.formula, props.targetCell ?? 'A1')
}
</script>

<template>
  <div class="rounded-xl border border-outline-variant/40 bg-surface overflow-hidden shadow-sm">
    <!-- Header -->
    <div class="flex items-center gap-2 px-4 py-3 border-b border-outline-variant/20 bg-surface-container-low/50">
      <Sparkles :size="14" class="text-secondary" />
      <span class="text-card-title text-on-surface font-medium">Formula Suggestion</span>
      <span v-if="targetCell" class="text-card-body text-on-surface-variant ml-auto">→ {{ targetCell }}</span>
    </div>

    <!-- Formula display -->
    <div class="px-4 py-3">
      <pre class="text-[13px] font-mono text-primary bg-surface-container-low rounded-lg px-3 py-2 overflow-x-auto">{{ formula }}</pre>
    </div>

    <!-- Explanation toggle -->
    <div v-if="explanation" class="border-t border-outline-variant/10">
      <button
        class="w-full flex items-center justify-between px-4 py-2.5 text-card-body text-on-surface-variant hover:bg-surface-container-low/50 transition-colors"
        @click="showExplanation = !showExplanation"
      >
        <span>How it works</span>
        <component :is="showExplanation ? ChevronUp : ChevronDown" :size="14" />
      </button>
      <Transition name="expand">
        <div v-if="showExplanation" class="px-4 pb-3">
          <p class="text-card-body text-on-surface-variant leading-relaxed">{{ explanation }}</p>
        </div>
      </Transition>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-2 px-4 py-3 border-t border-outline-variant/10">
      <button
        class="flex items-center gap-1.5 px-3 py-1.5 text-card-title text-on-surface-variant border border-outline-variant/40 rounded-lg hover:bg-surface-container-high transition-colors"
        @click="copyFormula"
      >
        <component :is="copied ? Check : Copy" :size="13" />
        {{ copied ? 'Copied!' : 'Copy' }}
      </button>
      <button
        class="flex items-center gap-1.5 px-3 py-1.5 text-card-title bg-primary text-on-primary rounded-lg hover:opacity-90 transition-opacity ml-auto"
        @click="applyFormula"
      >
        <Play :size="13" />
        Apply to Excel
      </button>
    </div>
  </div>
</template>

<style scoped>
.expand-enter-active, .expand-leave-active { transition: all 0.15s ease; }
.expand-enter-from, .expand-leave-to { opacity: 0; max-height: 0; overflow: hidden; }
.expand-enter-to, .expand-leave-from { opacity: 1; max-height: 200px; }
</style>

