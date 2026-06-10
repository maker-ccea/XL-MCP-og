import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { AppSettings, Theme, AIModel } from '@/types'
import { settingsService } from '@/services/settingsService'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<AppSettings>(settingsService.load())

  function applyTheme(theme: Theme): void {
    const root = document.documentElement
    if (theme === 'dark') {
      root.classList.add('dark')
    } else if (theme === 'light') {
      root.classList.remove('dark')
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      root.classList.toggle('dark', prefersDark)
    }
  }

  function save(): void {
    settingsService.save(settings.value)
    applyTheme(settings.value.theme)
  }

  function reset(): void {
    settings.value = settingsService.reset()
    applyTheme(settings.value.theme)
  }

  function init(): void {
    applyTheme(settings.value.theme)
  }

  return { settings, save, reset, init }
})

