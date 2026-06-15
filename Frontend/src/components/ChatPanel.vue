<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue'
import { Plus, Timer, Bot, ChevronDown, ArrowUp, Sparkles, Table, DollarSign, Target, Mic, MicOff, X } from '@lucide/vue'
import { useChatStore } from '@/stores/chatStore'
import { useSettingsStore } from '@/stores/settingsStore'
import { useProvidersStore } from '@/stores/providersStore'
import { useChat } from '@/composables/useChat'
import { useAudioRecorder } from '@/composables/useAudioRecorder'
import ChatMessage from './ChatMessage.vue'
import ProviderIcon from './ProviderIcon.vue'
import DataGridPreview from './DataGridPreview.vue'
import { useRouter } from 'vue-router'

const chatStore = useChatStore()
const settingsStore = useSettingsStore()
const providersStore = useProvidersStore()
const router = useRouter()
const { inputText, imageUrl, submit, handleKeydown } = useChat()

const { isListening, supported: speechSupported, toggleListening } = useAudioRecorder((text) => {
  inputText.value = (inputText.value + ' ' + text).trim()
})

const activeLabel = computed(() => {
  if (providersStore.activeProviderDef) {
    const def = providersStore.activeProviderDef
    const modelName = providersStore.active?.modelId.split('/').at(-1) ?? ''
    return `${def.name} · ${modelName}`
  }
  return 'XL-MCP Backend'
})

const scrollContainer = ref<HTMLElement | null>(null)
const textarea = ref<HTMLTextAreaElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    processImageFile(file)
  }
}

function processImageFile(file: File) {
  if (!file.type.startsWith('image/')) return
  const reader = new FileReader()
  reader.onload = (e) => {
    imageUrl.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

function handlePaste(event: ClipboardEvent) {
  const items = event.clipboardData?.items
  if (!items) return
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile()
      if (file) {
        processImageFile(file)
        event.preventDefault()
        break
      }
    }
  }
}

const greetingPrefix = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
})

const displayName = computed(() => settingsStore.settings.profile.displayName.trim())
const greeting = computed(() =>
  displayName.value ? `${greetingPrefix.value}, ` : `${greetingPrefix.value}`
)

const quickActions = [
  {
    icon: Table,
    title: "How's my spreadsheet?",
    description: "Get a quick overview of your workbook's data, structure, and key stats.",
    button: 'View report',
    prompt: "Give me a comprehensive overview of my current spreadsheet's structure, data, and key statistics."
  },
  {
    icon: DollarSign,
    title: 'Any spend issues?',
    description: 'Identify sudden spikes or dips in data and get suggestions to fix them.',
    button: 'Analyze data',
    prompt: 'Analyze my spreadsheet data for any anomalies, sudden spikes, or dips and suggest fixes.'
  },
  {
    icon: Target,
    title: 'Which formula works best?',
    description: 'See formula suggestions based on your data structure and goals.',
    button: 'View insights',
    prompt: 'Suggest the best formulas for my current spreadsheet based on the data structure.'
  }
]

function useQuickAction(prompt: string): void {
  inputText.value = prompt
  submit()
}

function autoResizeTextarea(): void {
  if (!textarea.value) return
  textarea.value.style.height = 'auto'
  textarea.value.style.height = Math.min(textarea.value.scrollHeight, 120) + 'px'
}

async function scrollToBottom(): Promise<void> {
  await nextTick()
  if (scrollContainer.value) {
    scrollContainer.value.scrollTop = scrollContainer.value.scrollHeight
  }
}

watch(() => chatStore.messages.length, scrollToBottom)
watch(() => chatStore.messages.at(-1)?.content, scrollToBottom)
</script>

<template>
  <div class="bg-surface rounded-2xl flex-1 flex flex-col relative overflow-hidden shadow-sm">
    
    <div ref="scrollContainer" class="flex-1 overflow-y-auto flex flex-col items-center pt-16 pb-36">
      
      <Transition name="fade-up">
        <div v-if="!chatStore.hasMessages" class="flex flex-col items-center text-center max-w-[800px] px-4 w-full">
          
          <div class="w-[52px] h-[52px] rounded-full bg-background border border-custom-border-light flex items-center justify-center mb-6">
            <Sparkles :size="24" class="text-secondary" />
          </div>
          
          <h1 class="font-display-welcome text-display-welcome text-on-surface mb-2">
            {{ greeting }}<span class="text-on-surface-variant">{{ displayName || 'there' }}</span>
          </h1>
          <p class="font-body-main text-body-main text-on-surface-variant mb-12">
            Hey there! What can I do for your spreadsheet today?
          </p>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-[620px]">
            <div
              v-for="card in quickActions"
              :key="card.title"
              class="bg-surface-container-low border border-outline-variant rounded-xl p-[18px_16px_14px] flex flex-col hover:border-custom-border-light transition-colors group cursor-pointer"
              @click="useQuickAction(card.prompt)"
            >
              <div class="mb-3">
                <component :is="card.icon" :size="20" class="text-secondary" />
              </div>
              <h3 class="font-card-title text-card-title text-on-surface mb-1">{{ card.title }}</h3>
              <p class="font-card-body text-card-body text-on-surface-variant flex-1 mb-4">
                {{ card.description }}
              </p>
              <button class="w-full bg-surface border border-custom-border-light rounded-lg py-2 font-card-title text-card-title text-on-surface hover:bg-surface-container-high transition-colors text-center">
                {{ card.button }}
              </button>
            </div>
          </div>
        </div>
      </Transition>

      
      <div v-if="chatStore.hasMessages" class="w-full max-w-[800px] px-6">
        <ChatMessage
          v-for="message in chatStore.messages"
          :key="message.id"
          :message="message"
        />
      </div>
    </div>

    
    <div class="absolute bottom-0 left-0 right-0 border-t border-custom-border-divider bg-surface/95 backdrop-blur-sm p-[16px_20px_20px]">
      <DataGridPreview />
      
      
      <div v-if="imageUrl" class="max-w-[800px] mx-auto mb-3 flex items-center gap-2">
        <div class="relative w-16 h-16 rounded-xl border border-outline-variant/30 overflow-hidden group shadow-sm bg-surface-container-low">
          <img :src="imageUrl" class="w-full h-full object-cover" />
          <button
            @click="imageUrl = ''"
            class="absolute top-1 right-1 bg-black/60 hover:bg-black/80 text-white rounded-full p-1 transition-colors shadow"
          >
            <X :size="10" />
          </button>
        </div>
      </div>

      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFileChange"
      />

      <div class="max-w-[800px] mx-auto flex items-end bg-surface border border-custom-border-light rounded-full p-2 pl-3 shadow-[0_2px_4px_rgba(0,0,0,0.02)] focus-within:border-on-surface/50 transition-colors">
        
        <button
          @click="triggerFileInput"
          class="w-[28px] h-[28px] rounded-full bg-background flex items-center justify-center hover:bg-surface-container-high transition-colors shrink-0 text-on-surface-variant self-end mb-0.5"
        >
          <Plus :size="18" />
        </button>
        
        <button class="w-[28px] h-[28px] rounded-full flex items-center justify-center hover:bg-surface-variant transition-colors shrink-0 ml-1 text-on-surface-variant self-end mb-0.5">
          <Timer :size="18" />
        </button>
        
        <button
          v-if="speechSupported"
          @click="toggleListening"
          class="w-[28px] h-[28px] rounded-full flex items-center justify-center transition-all shrink-0 ml-1 self-end mb-0.5"
          :class="isListening ? 'bg-red-100 text-red-600 animate-pulse' : 'hover:bg-surface-variant text-on-surface-variant'"
          :title="isListening ? 'Listening... Click to stop' : 'Speech-to-Text command input'"
        >
          <Mic v-if="!isListening" :size="17" />
          <MicOff v-else :size="17" />
        </button>
        
        <button
          class="flex items-center gap-1.5 h-[28px] px-2 rounded-full hover:bg-surface-variant transition-colors shrink-0 ml-1 self-end mb-0.5"
          :class="providersStore.active ? 'text-primary' : 'text-on-surface-variant'"
          @click="router.push('/settings')"
        >
          
          <ProviderIcon
            v-if="providersStore.active"
            :id="providersStore.active.providerId"
            :size="16"
          />
          <Bot v-else :size="16" />
          <span class="text-[13px] font-medium max-w-[180px] truncate">{{ activeLabel }}</span>
          <ChevronDown :size="14" />
        </button>
        
        <div class="w-[1px] h-5 bg-outline-variant mx-3 shrink-0 self-end mb-1" />
        
        <textarea
          ref="textarea"
          v-model="inputText"
          rows="1"
          placeholder="Write a message here..."
          :disabled="chatStore.loading"
          class="flex-1 bg-transparent border-none focus:ring-0 p-0 font-body-main text-body-main placeholder:text-[#B4B2A9] text-on-surface min-w-0 resize-none overflow-hidden leading-relaxed py-1 disabled:opacity-50"
          style="field-sizing: content"
          @keydown="handleKeydown"
          @input="autoResizeTextarea"
          @paste="handlePaste"
        />
        
        <button
          :disabled="(!inputText.trim() && !imageUrl) || chatStore.loading"
          class="w-[30px] h-[30px] rounded-full bg-primary flex items-center justify-center hover:opacity-90 transition-opacity shrink-0 ml-2 disabled:opacity-40 self-end mb-0.5"
          @click="submit"
        >
          <ArrowUp :size="16" class="text-on-primary" stroke-width="2.5" />
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-up-enter-active { transition: all 0.4s ease; }
.fade-up-enter-from { opacity: 0; transform: translateY(16px); }
</style>

