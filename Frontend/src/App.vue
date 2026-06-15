<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { useSettingsStore } from '@/stores/settingsStore'
import CommandPalette from '@/components/CommandPalette.vue'
import HelpTour from '@/components/HelpTour.vue'

const settingsStore = useSettingsStore()
onMounted(() => settingsStore.init())
</script>

<template>
  <RouterView />
  <CommandPalette />
  <HelpTour />
</template>

