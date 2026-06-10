import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ProviderID } from '@/config/providers'
import { PROVIDER_MAP, PROVIDERS } from '@/config/providers'
import { aiProviderService } from '@/services/aiProviderService'

export interface ProviderConfig {
  apiKey: string
  selectedModel: string
  customBaseUrl: string
  testStatus: 'untested' | 'success' | 'failed'
  lastTestedAt: string | null
  latencyMs: number | null
  errorMessage: string | null
}

export interface ActiveProvider {
  providerId: ProviderID
  modelId: string
}

const STORAGE_KEY = 'xl_mcp_providers'
const ACTIVE_KEY = 'xl_mcp_active_provider'

function defaultConfig(): ProviderConfig {
  return {
    apiKey: '',
    selectedModel: '',
    customBaseUrl: '',
    testStatus: 'untested',
    lastTestedAt: null,
    latencyMs: null,
    errorMessage: null
  }
}

function loadConfigs(): Record<string, ProviderConfig> {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

function loadActive(): ActiveProvider | null {
  try {
    const raw = localStorage.getItem(ACTIVE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export const useProvidersStore = defineStore('providers', () => {
  const configs = ref<Record<string, ProviderConfig>>(loadConfigs())
  const active = ref<ActiveProvider | null>(loadActive())
  const testing = ref<Set<ProviderID>>(new Set())

  // ── Getters ──────────────────────────────────────────────────────────────────

  function getConfig(id: ProviderID): ProviderConfig {
    return configs.value[id] ?? defaultConfig()
  }

  const activeProviderDef = computed(() =>
    active.value ? PROVIDER_MAP[active.value.providerId] : null
  )

  const activeConfig = computed(() =>
    active.value ? getConfig(active.value.providerId) : null
  )

  function isConfigured(id: ProviderID): boolean {
    const def = PROVIDER_MAP[id]
    if (def.requiresNoKey) return true
    const cfg = getConfig(id)
    return cfg.apiKey.trim().length > 0
  }

  function isActive(id: ProviderID): boolean {
    return active.value?.providerId === id
  }

  function isTesting(id: ProviderID): boolean {
    return testing.value.has(id)
  }

  // ── Actions ──────────────────────────────────────────────────────────────────

  function updateConfig(id: ProviderID, patch: Partial<ProviderConfig>): void {
    const current = getConfig(id)
    configs.value[id] = { ...current, ...patch }
    persist()
  }

  function setActive(providerId: ProviderID, modelId: string): void {
    active.value = { providerId, modelId }
    localStorage.setItem(ACTIVE_KEY, JSON.stringify(active.value))
  }

  function clearActive(): void {
    active.value = null
    localStorage.removeItem(ACTIVE_KEY)
  }

  function clearProvider(id: ProviderID): void {
    delete configs.value[id]
    if (active.value?.providerId === id) clearActive()
    persist()
  }

  async function testProvider(id: ProviderID): Promise<void> {
    const cfg = getConfig(id)
    const def = PROVIDER_MAP[id]
    const modelId = cfg.selectedModel || def.models.find((m) => m.recommended)?.id || def.models[0]?.id || ''

    testing.value.add(id)

    try {
      const result = await aiProviderService.testConnection(
        id,
        modelId,
        def.requiresNoKey ? 'ollama' : cfg.apiKey,
        cfg.customBaseUrl || undefined
      )

      updateConfig(id, {
        testStatus: result.success ? 'success' : 'failed',
        lastTestedAt: new Date().toISOString(),
        latencyMs: result.latencyMs,
        errorMessage: result.error ?? null
      })
    } finally {
      testing.value.delete(id)
    }
  }

  function persist(): void {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(configs.value))
  }

  return {
    configs,
    active,
    getConfig,
    activeProviderDef,
    activeConfig,
    isConfigured,
    isActive,
    isTesting,
    updateConfig,
    setActive,
    clearActive,
    clearProvider,
    testProvider
  }
})
