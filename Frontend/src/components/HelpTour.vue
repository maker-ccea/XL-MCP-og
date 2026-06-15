<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Sparkles, Terminal, ShieldAlert, Award, ChevronRight, X, Play } from '@lucide/vue'

const active = ref(false)
const currentStep = ref(0)

const steps = [
  {
    title: 'Welcome to XL-MCP!',
    description: 'XL-MCP is your premium AI Copilot for Excel. Let’s get you acquainted with the workspace in just a few steps.',
    icon: Sparkles,
    highlight: ''
  },
  {
    title: 'AI Command Input',
    description: 'Use the text field at the bottom to type instructions like "Format the first row as headers" or "Sum values in A1:A20". You can also click the microphone icon to narrate commands!',
    icon: Terminal,
    highlight: 'chat-input'
  },
  {
    title: 'Draggable Action Previews',
    description: 'Before any actions run in Excel, you will see a preview card. You can drag and reorder action blocks to modify the execution sequence, or reject the plan entirely.',
    icon: ShieldAlert,
    highlight: 'action-preview'
  },
  {
    title: 'Seamless Custom Integrations',
    description: 'Go to Settings → Integrations to hook up your own custom OpenAI, Anthropic, or local Ollama configurations. Tailor the brain powering your intelligence.',
    icon: Award,
    highlight: 'settings-integrations'
  }
]

function nextStep() {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  } else {
    completeTour()
  }
}

function completeTour() {
  active.value = false
  localStorage.setItem('xl_mcp_help_tour_seen', 'true')
}

function startTour() {
  currentStep.value = 0
  active.value = true
}

onMounted(() => {
  const seen = localStorage.getItem('xl_mcp_help_tour_seen')
  if (!seen) {
    
    setTimeout(() => {
      active.value = true
    }, 1500)
  }

  window.addEventListener('trigger-help-tour', startTour)
})

onUnmounted(() => {
  window.removeEventListener('trigger-help-tour', startTour)
})
</script>

<template>
  <Transition name="fade">
    <div v-if="active" class="fixed inset-0 z-[110] flex items-center justify-center p-6 bg-black/55 backdrop-blur-[3px]">
      
      <div class="relative w-full max-w-[440px] bg-surface border border-outline-variant/30 rounded-2xl shadow-2xl overflow-hidden p-6 flex flex-col items-center text-center">
        
        <button
          class="absolute top-4 right-4 p-1 rounded-lg hover:bg-surface-container-high text-on-surface-variant transition-colors"
          @click="completeTour"
        >
          <X :size="16" />
        </button>

        
        <div class="w-14 h-14 rounded-full bg-primary/10 border border-primary/20 text-primary flex items-center justify-center mb-5">
          <component :is="steps[currentStep].icon" :size="24" />
        </div>

        
        <div class="flex items-center gap-1 mb-3">
          <span
            v-for="(step, idx) in steps"
            :key="idx"
            :class="['h-1.5 rounded-full transition-all duration-300',
              idx === currentStep ? 'w-4 bg-primary' : 'w-1.5 bg-outline-variant/50'
            ]"
          />
        </div>

        
        <h2 class="text-[17px] font-bold text-on-surface mb-2 font-display-welcome leading-tight">
          {{ steps[currentStep].title }}
        </h2>

        
        <p class="text-[12.5px] text-on-surface-variant leading-relaxed mb-6 px-2 min-h-[60px] flex items-center justify-center">
          {{ steps[currentStep].description }}
        </p>

        
        <div class="w-full flex items-center justify-between border-t border-outline-variant/20 pt-4 mt-auto">
          <button
            class="text-[12px] font-medium text-on-surface-variant hover:text-on-surface transition-colors"
            @click="completeTour"
          >
            Skip Tour
          </button>

          <button
            class="flex items-center gap-1.5 px-4 py-1.5 bg-primary text-on-primary rounded-lg text-[12px] font-semibold hover:opacity-90 active:scale-95 transition-all shadow-sm"
            @click="nextStep"
          >
            <span>{{ currentStep === steps.length - 1 ? 'Finish' : 'Next' }}</span>
            <ChevronRight :size="14" />
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: scale(0.96); }
</style>
