import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { AppSettings, Theme, AIModel } from '@/types'
import { settingsService } from '@/services/settingsService'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<AppSettings>(settingsService.load())

  function applyTheme(theme: Theme): void {
    const root = document.documentElement
    root.classList.remove('dark', 'theme-nord', 'theme-cyberpunk', 'theme-forest')
    
    if (theme === 'dark') {
      root.classList.add('dark')
    } else if (theme === 'nord') {
      root.classList.add('theme-nord', 'dark')
    } else if (theme === 'cyberpunk') {
      root.classList.add('theme-cyberpunk', 'dark')
    } else if (theme === 'forest-green') {
      root.classList.add('theme-forest')
    } else if (theme === 'light') {
      
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

