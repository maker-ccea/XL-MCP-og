<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSettingsStore } from '@/stores/settingsStore'
import { useChatStore } from '@/stores/chatStore'
import { useExcelStore } from '@/stores/excelStore'
import { Search, Terminal, Palette, Trash2, Settings, History, RefreshCw, Sparkles, HelpCircle } from '@lucide/vue'

const open = ref(false)
const search = ref('')
const selectedIndex = ref(0)

const router = useRouter()
const settingsStore = useSettingsStore()
const chatStore = useChatStore()
const excelStore = useExcelStore()

interface CommandItem {
  icon: any
  title: string
  subtitle: string
  action: () => void
}

const commands: CommandItem[] = [
  {
    icon: HelpCircle,
    title: 'Start Onboarding Help Tour',
    subtitle: 'Learn how to use the XL-MCP workspace',
    action: () => {
      
      window.dispatchEvent(new CustomEvent('trigger-help-tour'))
    }
  },
  {
    icon: Palette,
    title: 'Switch to Nord Theme',
    subtitle: 'Cool arctic pastel color scheme',
    action: () => {
      settingsStore.settings.theme = 'nord'
      settingsStore.save()
    }
  },
  {
    icon: Palette,
    title: 'Switch to Cyberpunk Theme',
    subtitle: 'Vibrant neon dark mode',
    action: () => {
      settingsStore.settings.theme = 'cyberpunk'
      settingsStore.save()
    }
  },
  {
    icon: Palette,
    title: 'Switch to Forest Green Theme',
    subtitle: 'Calming natural light mode',
    action: () => {
      settingsStore.settings.theme = 'forest-green'
      settingsStore.save()
    }
  },
  {
    icon: Palette,
    title: 'Switch to Dark Theme',
    subtitle: 'Premium classic slate dark mode',
    action: () => {
      settingsStore.settings.theme = 'dark'
      settingsStore.save()
    }
  },
  {
    icon: Palette,
    title: 'Switch to Light Theme',
    subtitle: 'Clean white workspace',
    action: () => {
      settingsStore.settings.theme = 'light'
      settingsStore.save()
    }
  },
  {
    icon: Trash2,
    title: 'Clear Chat History',
    subtitle: 'Reset the current conversation thread',
    action: () => {
      chatStore.clearHistory()
    }
  },
  {
    icon: Settings,
    title: 'Go to Settings',
    subtitle: 'Manage profile, keys, and providers',
    action: () => {
      router.push('/settings')
    }
  },
  {
    icon: History,
    title: 'View Action History',
    subtitle: 'See log of recently executed actions',
    action: () => {
      router.push('/history')
    }
  },
  {
    icon: RefreshCw,
    title: 'Reconnect Excel',
    subtitle: 'Trigger backend refresh of Excel instance',
    action: () => {
      excelStore.checkHealth()
    }
  }
]

const filteredCommands = computed(() => {
  if (!search.value) return commands
  const query = search.value.toLowerCase()
  return commands.filter(
    (c) => c.title.toLowerCase().includes(query) || c.subtitle.toLowerCase().includes(query)
  )
})

function handleKeydown(e: KeyboardEvent) {
  const shortcut = settingsStore.settings.shortcuts?.commandPalette || 'Control+k'
  const keys = shortcut.split('+')
  const ctrlRequired = keys.includes('Control')
  const shiftRequired = keys.includes('Shift')
  const altRequired = keys.includes('Alt')
  const targetKey = keys.at(-1)?.toLowerCase()

  const matchCtrl = ctrlRequired ? (e.ctrlKey || e.metaKey) : !(e.ctrlKey || e.metaKey)
  const matchShift = shiftRequired ? e.shiftKey : !e.shiftKey
  const matchAlt = altRequired ? e.altKey : !e.altKey
  const matchKey = e.key.toLowerCase() === targetKey

  if (matchCtrl && matchShift && matchAlt && matchKey) {
    e.preventDefault()
    open.value = !open.value
    search.value = ''
    selectedIndex.value = 0
    return
  }

  if (!open.value) return

  if (e.key === 'Escape') {
    open.value = false
  } else if (e.key === 'ArrowDown') {
    e.preventDefault()
    selectedIndex.value = (selectedIndex.value + 1) % filteredCommands.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    selectedIndex.value = (selectedIndex.value - 1 + filteredCommands.value.length) % filteredCommands.value.length
  } else if (e.key === 'Enter') {
    e.preventDefault()
    runSelected()
  }
}

function runSelected() {
  const cmd = filteredCommands.value[selectedIndex.value]
  if (cmd) {
    cmd.action()
    open.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <Transition name="fade">
    <div v-if="open" class="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] p-4">
      
      <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="open = false" />

      
      <div class="relative z-10 w-full max-w-[550px] bg-surface border border-outline-variant/30 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[380px]">
        
        <div class="flex items-center gap-3 px-4 py-3.5 border-b border-outline-variant/20 bg-surface-container-low/40">
          <Search :size="18" class="text-on-surface-variant/60" />
          <input
            v-model="search"
            type="text"
            placeholder="Type a command or search..."
            class="flex-1 bg-transparent border-none outline-none text-[13px] text-on-surface placeholder:text-on-surface-variant/40"
            ref="input"
            autofocus
            @input="selectedIndex = 0"
          />
          <span class="text-[10px] bg-surface-container-high border border-outline-variant/30 rounded px-1.5 py-0.5 text-on-surface-variant font-mono">
            ESC
          </span>
        </div>

        
        <div class="flex-1 overflow-y-auto p-2">
          <div v-if="filteredCommands.length === 0" class="py-12 text-center text-on-surface-variant/60 text-[12px] flex flex-col items-center gap-2">
            <Terminal :size="20" class="text-on-surface-variant/40" />
            No commands matched your query.
          </div>
          <div
            v-else
            v-for="(cmd, idx) in filteredCommands"
            :key="cmd.title"
            @mouseenter="selectedIndex = idx"
            @click="runSelected"
            :class="['flex items-center gap-3 px-3.5 py-2.5 rounded-xl cursor-pointer transition-colors',
              selectedIndex === idx
                ? 'bg-surface-container-highest text-on-surface'
                : 'text-on-surface-variant'
            ]"
          >
            <div :class="['w-8 h-8 rounded-lg flex items-center justify-center border transition-colors shrink-0',
              selectedIndex === idx
                ? 'bg-primary/10 border-primary/20 text-primary'
                : 'bg-surface-container border-outline-variant/20 text-on-surface-variant/70'
            ]">
              <component :is="cmd.icon" :size="16" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-[12.5px] font-semibold truncate">{{ cmd.title }}</p>
              <p class="text-[10.5px] text-on-surface-variant/60 truncate mt-0.5">{{ cmd.subtitle }}</p>
            </div>
            <span v-if="selectedIndex === idx" class="text-[10px] font-medium text-primary/75 tracking-wider font-mono">
              ENTER
            </span>
          </div>
        </div>

        
        <div class="px-4 py-2 border-t border-outline-variant/20 bg-surface-container-low/40 flex justify-between text-[10px] text-on-surface-variant/50 select-none">
          <div class="flex items-center gap-2">
            <span>↑↓ to navigate</span>
            <span>·</span>
            <span>↵ to select</span>
          </div>
          <span>Command Palette</span>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: all 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
