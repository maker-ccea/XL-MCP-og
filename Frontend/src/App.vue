<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useSettingsStore } from '@/stores/settingsStore'

const settingsStore = useSettingsStore()
onMounted(() => settingsStore.init())
</script>

<template>
  <RouterView />
</template>

