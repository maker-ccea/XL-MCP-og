<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { FileSpreadsheet, Sheet, History, Settings, X, Wifi, WifiOff } from '@lucide/vue'
import { useExcelStore } from '@/stores/excelStore'
import { useProvidersStore } from '@/stores/providersStore'
import ProviderIcon from './ProviderIcon.vue'

defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: [] }>()

const router = useRouter()
const route = useRoute()
const excelStore = useExcelStore()
const providersStore = useProvidersStore()

function navigate(to: string): void {
  router.push(to)
  emit('close')
}

const navItems = [
  { label: 'Workspace', icon: FileSpreadsheet, to: '/' },
  { label: 'History', icon: History, to: '/history' },
  { label: 'Settings', icon: Settings, to: '/settings' }
]
</script>

<template>
  
  <Transition name="fade">
    <div v-if="open" class="fixed inset-0 z-40 bg-black/20 backdrop-blur-[1px]" @click="emit('close')" />
  </Transition>

  
  <Transition name="slide">
    <aside
      v-if="open"
      class="fixed left-0 top-0 bottom-0 z-50 w-[260px] bg-surface border-r border-outline-variant/30 flex flex-col shadow-xl"
    >
      
      <div class="flex items-center justify-between px-5 py-4 border-b border-outline-variant/20">
        <span class="text-[15px] font-semibold text-on-surface tracking-tight">XL-MCP</span>
        <button class="p-1.5 rounded-md hover:bg-surface-container-high text-on-surface-variant transition-colors" @click="emit('close')">
          <X :size="16" />
        </button>
      </div>

      
      <div class="px-5 py-3 border-b border-outline-variant/10">
        <div class="flex items-center gap-2 mb-1">
          <component :is="excelStore.isConnected ? Wifi : WifiOff" :size="13" :class="excelStore.isConnected ? 'text-emerald-500' : 'text-on-surface-variant/50'" />
          <span class="text-label-caps text-label-caps text-on-surface-variant/60 uppercase">
            {{ excelStore.isConnected ? 'Connected' : 'Disconnected' }}
          </span>
        </div>
        <div v-if="excelStore.hasWorkbook" class="space-y-0.5 pl-[21px]">
          <p class="text-card-title text-on-surface truncate" :title="excelStore.workbookName ?? ''">
            {{ excelStore.workbookName }}
          </p>
          <p class="text-card-body text-on-surface-variant">Active: {{ excelStore.activeSheet ?? '—' }}</p>
          <p v-if="excelStore.selectedRange" class="text-card-body text-on-surface-variant/70">
            Selection: {{ excelStore.selectedRange }}
          </p>
        </div>
        <p v-else class="text-card-body text-on-surface-variant/60 pl-[21px]">No workbook open</p>
      </div>

      
      <div v-if="excelStore.availableSheets.length > 0" class="px-5 py-3 border-b border-outline-variant/10">
        <p class="text-label-caps text-label-caps text-on-surface-variant/60 uppercase mb-2">Sheets</p>
        <ul class="space-y-0.5">
          <li
            v-for="sheet in excelStore.availableSheets"
            :key="sheet"
            :class="[
              'flex items-center gap-2 px-2 py-1.5 rounded-lg text-card-title cursor-pointer transition-colors',
              sheet === excelStore.activeSheet
                ? 'bg-surface-container-highest text-on-surface font-medium'
                : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
            ]"
          >
            <Sheet :size="14" class="shrink-0" />
            <span class="truncate">{{ sheet }}</span>
          </li>
        </ul>
      </div>

      
      <nav class="px-4 py-4 flex-1">
        <p class="text-label-caps text-label-caps text-on-surface-variant/60 uppercase mb-2 px-2">Navigation</p>
        <ul class="space-y-0.5">
          <li
            v-for="item in navItems"
            :key="item.to"
            :class="[
              'flex items-center gap-2.5 px-2 py-2 rounded-lg text-card-title cursor-pointer transition-colors',
              route.path === item.to
                ? 'bg-surface-container-highest text-on-surface font-medium shadow-sm'
                : 'text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
            ]"
            @click="navigate(item.to)"
          >
            <component :is="item.icon" :size="15" class="shrink-0" />
            {{ item.label }}
          </li>
        </ul>
      </nav>

      
      <div class="px-4 py-3 border-t border-outline-variant/10">
        <p class="text-label-caps text-label-caps text-on-surface-variant/60 uppercase mb-2 px-1">AI Provider</p>
        <div v-if="providersStore.active && providersStore.activeProviderDef"
          class="flex items-center gap-2 px-2 py-1.5 rounded-lg bg-surface-container-high/50 cursor-pointer hover:bg-surface-container-high transition-colors"
          @click="navigate('/settings')"
        >
          <div :class="['w-6 h-6 rounded-md flex items-center justify-center shrink-0', providersStore.activeProviderDef.color, providersStore.activeProviderDef.textColor]">
            <ProviderIcon :id="providersStore.active.providerId" :size="13" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-card-title text-on-surface font-medium truncate">{{ providersStore.activeProviderDef.name }}</p>
            <p class="text-[10px] text-on-surface-variant/60 truncate">{{ providersStore.active.modelId.split('/').at(-1) }}</p>
          </div>
        </div>
        <div v-else
          class="flex items-center gap-2 px-2 py-1.5 text-card-body text-on-surface-variant/60 cursor-pointer hover:text-on-surface transition-colors rounded-lg"
          @click="navigate('/settings')"
        >
          <Settings :size="13" class="shrink-0" />
          Configure provider
        </div>
      </div>

      
      <div class="px-5 py-3 border-t border-outline-variant/20">
        <p class="font-mono text-mono-small text-outline/50 tracking-wider">VERSION 1.0.0</p>
      </div>
    </aside>
  </Transition>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-enter-active, .slide-leave-active { transition: transform 0.25s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }
</style>

