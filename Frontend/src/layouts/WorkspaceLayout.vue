<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Plus, PanelLeft, Share, Settings } from '@lucide/vue'
import WorkbookSidebar from '@/components/WorkbookSidebar.vue'
import { useChatStore } from '@/stores/chatStore'

const router = useRouter()
const chatStore = useChatStore()
const sidebarOpen = ref(false)
</script>

<template>
  <div class="bg-background font-body-main text-on-surface antialiased h-screen flex flex-col overflow-hidden">
    <!-- Top Nav Bar -->
    <header class="flex justify-between items-center px-8 h-16 w-full shrink-0 z-10 drag-region">
      <!-- Left -->
      <div class="flex items-center gap-4 no-drag">
        <button
          class="p-2 text-on-surface-variant hover:bg-surface-variant rounded-md transition-colors flex items-center justify-center"
          @click="sidebarOpen = true"
        >
          <Search :size="20" />
        </button>
        <button
          class="flex items-center gap-2 px-3 py-1.5 text-on-surface border border-transparent hover:bg-surface-variant rounded-md transition-colors font-card-title text-card-title"
          @click="chatStore.clearConversation()"
        >
          <Plus :size="18" />
          New Chat
        </button>
      </div>

      <!-- Center title -->
      <div class="font-display-welcome text-display-welcome font-semibold text-primary absolute left-1/2 -translate-x-1/2 pointer-events-none">
        Workspace
      </div>

      <!-- Right -->
      <div class="flex items-center gap-4 no-drag">
        <button
          class="p-2 text-on-surface-variant hover:bg-surface-variant rounded-md transition-colors flex items-center justify-center"
          @click="sidebarOpen = true"
        >
          <PanelLeft :size="20" />
        </button>
        <button
          class="flex items-center gap-2 px-3 py-1.5 text-on-surface border border-outline-variant hover:bg-surface-container-high rounded-md transition-colors font-card-title text-card-title"
        >
          <Share :size="18" />
          Share
        </button>
        <button
          class="p-2 text-on-surface-variant hover:bg-surface-variant rounded-md transition-colors flex items-center justify-center"
          @click="router.push('/settings')"
        >
          <Settings :size="20" />
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 px-8 pb-8 flex flex-col min-h-0">
      <slot />
    </main>

    <!-- Sidebar -->
    <WorkbookSidebar :open="sidebarOpen" @close="sidebarOpen = false" />
  </div>
</template>

