<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import WorkspaceLayout from '@/layouts/WorkspaceLayout.vue'
import ChatPanel from '@/components/ChatPanel.vue'
import ActionPreviewModal from '@/components/ActionPreviewModal.vue'
import LoadingScreen from '@/components/LoadingScreen.vue'
import { useChatStore } from '@/stores/chatStore'
import { useExcelStore } from '@/stores/excelStore'
import { useExcel } from '@/composables/useExcel'
import type { ActionPreview } from '@/types'

const chatStore = useChatStore()
const excelStore = useExcelStore()

// Init Excel polling and WebSocket
const { connected } = useExcel()

// Splash screen state
type SplashStatus = 'checking' | 'connected' | 'failed' | 'not_running'
const splashVisible = ref(true)
const backendStatus = ref<'checking' | 'connected' | 'failed'>('checking')
const excelStatus = ref<SplashStatus>('checking')

onMounted(async () => {
  try {
    await excelStore.checkHealth()
    backendStatus.value = excelStore.backendHealthy ? 'connected' : 'failed'
    excelStatus.value = excelStore.excelRunning ? 'connected' : 'not_running'
  } catch {
    backendStatus.value = 'failed'
    excelStatus.value = 'failed'
  } finally {
    // Brief pause so user can see the status, then show workspace
    setTimeout(() => { splashVisible.value = false }, 1200)
  }
})

function handleApprove(actions: ActionPreview['action'][]): void {
  chatStore.executeApprovedPlan(actions)
}

function handleReject(): void {
  chatStore.rejectPlan()
}
</script>

<template>
  <!-- Splash Screen -->
  <Transition name="splash">
    <LoadingScreen
      v-if="splashVisible"
      :backend-status="backendStatus"
      :excel-status="excelStatus"
    />
  </Transition>

  <!-- Main Workspace -->
  <WorkspaceLayout v-if="!splashVisible">
    <ChatPanel />
  </WorkspaceLayout>

  <!-- Action Preview Modal -->
  <ActionPreviewModal
    v-if="!splashVisible"
    :open="chatStore.showActionModal"
    :plan="chatStore.pendingPlan ?? []"
    :all-valid="chatStore.pendingPlan?.every((p) => p.is_valid) ?? false"
    :original-message="chatStore.pendingMessage"
    @approve="handleApprove"
    @reject="handleReject"
  />
</template>

<style scoped>
.splash-leave-active { transition: opacity 0.4s ease; }
.splash-leave-to { opacity: 0; }
</style>

