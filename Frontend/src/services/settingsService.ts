import type { AppSettings } from '@/types'

const STORAGE_KEY = 'xl_mcp_settings'

const defaults: AppSettings = {
  profile: {
    displayName: '',
    role: '',
    bio: '',
    avatarColor: 'zinc'
  },
  theme: 'light',
  model: 'xl-mcp-pro',
  language: 'auto',
  actionPreview: true,
  autoSuggest: true,
  formulaExplanations: true,
  streamingResponses: true,
  activeSheetContext: true,
  workbookNameContext: true,
  maxContextRows: 500,
  apiKey: ''
}

export const settingsService = {
  load(): AppSettings {
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (!raw) return { ...defaults, profile: { ...defaults.profile } }
      const parsed = JSON.parse(raw)
      return {
        ...defaults,
        ...parsed,
        profile: { ...defaults.profile, ...parsed.profile }
      }
    } catch {
      return { ...defaults, profile: { ...defaults.profile } }
    }
  },

  save(settings: AppSettings): void {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
  },

  reset(): AppSettings {
    localStorage.removeItem(STORAGE_KEY)
    return { ...defaults, profile: { ...defaults.profile } }
  }
}
