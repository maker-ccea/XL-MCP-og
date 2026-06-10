<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ErrorState from '@/components/ErrorState.vue'
import { useExcelStore } from '@/stores/excelStore'

const route = useRoute()
const router = useRouter()
const excelStore = useExcelStore()
const retrying = ref(false)

const errorType = (route.query.type as 'backend' | 'excel' | 'connection' | 'general') ?? 'general'

const errorMessages = {
  backend: {
    title: 'Backend Server Unreachable',
    message: 'XL-MCP cannot connect to the Python backend server.'
  },
  excel: {
    title: 'Excel Not Running',
    message: 'Microsoft Excel is not open. Please launch Excel and try again.'
  },
  connection: {
    title: 'Connection Lost',
    message: 'The connection to the backend was interrupted.'
  },
  general: {
    title: 'Something Went Wrong',
    message: 'An unexpected error occurred.'
  }
}

const { title, message } = errorMessages[errorType]

async function retry(): Promise<void> {
  retrying.value = true
  try {
    await excelStore.checkHealth()
    if (excelStore.backendHealthy) {
      router.push('/')
    }
  } catch {
    // still failing
  } finally {
    retrying.value = false
  }
}
</script>

<template>
  <div class="bg-background font-body-main text-on-surface antialiased h-screen flex flex-col overflow-hidden">
    <div class="flex-1 flex">
      <ErrorState
        :type="errorType"
        :title="title"
        :message="message"
        :retrying="retrying"
        @retry="retry"
      />
    </div>
  </div>
</template>

