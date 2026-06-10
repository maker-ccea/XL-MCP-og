<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  Check, ChevronDown, ChevronUp, ExternalLink, Loader2,
  Zap, ZapOff, Eye, EyeOff, Trash2, Wifi, TriangleAlert
} from '@lucide/vue'
import { PROVIDERS, PROVIDER_MAP } from '@/config/providers'
import type { ProviderID, ProviderDefinition } from '@/config/providers'
import { useProvidersStore } from '@/stores/providersStore'
import ProviderIcon from './ProviderIcon.vue'

const store = useProvidersStore()

// ── Expand/collapse ───────────────────────────────────────────────────────────

const expanded = ref<ProviderID | null>(null)

function toggle(id: ProviderID): void {
  expanded.value = expanded.value === id ? null : id
}

// ── Local edit state (per-provider draft before saving) ───────────────────────

const drafts = ref<Record<string, { apiKey: string; model: string; baseUrl: string }>>({})

function getDraft(id: ProviderID) {
  if (!drafts.value[id]) {
    const cfg = store.getConfig(id)
    const def = PROVIDER_MAP[id]
    drafts.value[id] = {
      apiKey: cfg.apiKey,
      model: cfg.selectedModel || def.models.find((m) => m.recommended)?.id || def.models[0]?.id || '',
      baseUrl: cfg.customBaseUrl || def.baseUrl
    }
  }
  return drafts.value[id]
}

// When expanded changes, init draft
watch(expanded, (id) => { if (id) getDraft(id) })

// ── Show/hide API key ─────────────────────────────────────────────────────────

const showKey = ref<Record<string, boolean>>({})
function toggleShowKey(id: ProviderID): void {
  showKey.value[id] = !showKey.value[id]
}

// ── Save config ───────────────────────────────────────────────────────────────

function saveConfig(id: ProviderID): void {
  const draft = getDraft(id)
  store.updateConfig(id, {
    apiKey: draft.apiKey,
    selectedModel: draft.model,
    customBaseUrl: draft.baseUrl,
    testStatus: 'untested',
    errorMessage: null
  })
}

// ── Test ─────────────────────────────────────────────────────────────────────

async function testProvider(id: ProviderID): Promise<void> {
  saveConfig(id)
  await store.testProvider(id)
}

// ── Set active ────────────────────────────────────────────────────────────────

function setActive(id: ProviderID): void {
  const draft = getDraft(id)
  saveConfig(id)
  store.setActive(id, draft.model)
}

// ── Status helpers ────────────────────────────────────────────────────────────

function statusBadge(id: ProviderID): { label: string; classes: string } {
  if (store.isActive(id)) return { label: 'Active', classes: 'bg-primary text-on-primary' }
  const cfg = store.getConfig(id)
  if (!store.isConfigured(id)) return { label: 'Not configured', classes: 'bg-surface-container-highest text-on-surface-variant' }
  if (cfg.testStatus === 'success') return { label: 'Connected', classes: 'bg-emerald-100 text-emerald-700' }
  if (cfg.testStatus === 'failed') return { label: 'Error', classes: 'bg-red-100 text-red-600' }
  return { label: 'Configured', classes: 'bg-sky-100 text-sky-700' }
}

function latencyLabel(id: ProviderID): string {
  const cfg = store.getConfig(id)
  if (cfg.latencyMs === null) return ''
  return `${cfg.latencyMs}ms`
}

function errorHint(msg: string, id: ProviderID): string {
  const m = msg.toLowerCase()
  if (m.includes('401') || m.includes('auth') || m.includes('api key') || m.includes('invalid key') || m.includes('unauthorized') || m.includes('credentials'))
    return 'Your API key appears to be invalid or expired. Double-check it on the provider\'s dashboard.'
  if (m.includes('403') || m.includes('forbidden') || m.includes('permission') || m.includes('access denied'))
    return 'Access denied. Your key may lack permission for this model or endpoint.'
  if (m.includes('404') || m.includes('not found') || m.includes('model') && m.includes('exist'))
    return 'Model not found. Check the model ID is correct and your account has access to it.'
  if (m.includes('429') || m.includes('rate limit') || m.includes('quota') || m.includes('too many'))
    return 'Rate limit or quota exceeded. Wait a moment and try again, or upgrade your plan.'
  if (m.includes('500') || m.includes('502') || m.includes('503') || m.includes('provider returned error') || m.includes('upstream'))
    return id === 'openrouter'
      ? 'The upstream provider returned an error. Try a different model, or check openrouter.ai/status.'
      : 'The provider\'s server returned an error. Try again or check the provider\'s status page.'
  if (m.includes('timeout') || m.includes('timed out'))
    return 'Request timed out. The provider may be overloaded — try again in a moment.'
  if (m.includes('connection') || m.includes('econnrefused') || m.includes('network'))
    return id === 'ollama'
      ? 'Cannot reach Ollama. Make sure it is running: ollama serve'
      : 'Network error. Check your internet connection.'
  return 'Check that your API key, model ID, and account permissions are correct.'
}

const activeProviderDef = computed(() => store.activeProviderDef)
const activeConfig = computed(() => store.activeConfig)
</script>

<template>
  <div class="max-w-[640px] mx-auto pb-8">
    <!-- Header -->
    <header class="mb-6 border-b border-outline-variant/20 pb-4">
      <h1 class="text-[20px] font-semibold text-on-surface mb-1">Integrations</h1>
      <p class="text-[13px] text-on-surface-variant/80">Connect AI providers to power your Excel workspace. Your API keys are stored locally and never leave your device.</p>
    </header>

    <!-- Active Provider Banner -->
    <div v-if="store.active && activeProviderDef" class="mb-6 flex items-center gap-3 px-4 py-3.5 bg-primary/5 border border-primary/20 rounded-xl">
      <div :class="['w-9 h-9 rounded-xl flex items-center justify-center shrink-0', activeProviderDef.color, activeProviderDef.textColor]">
        <ProviderIcon :id="store.active.providerId" :size="20" />
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-[13px] font-medium text-on-surface">
          XL-MCP is using <span class="font-semibold">{{ activeProviderDef.name }}</span>
          <span class="text-on-surface-variant"> · {{ store.active.modelId }}</span>
        </p>
        <p class="text-[11px] text-on-surface-variant/60 mt-0.5">AI responses come directly from this provider</p>
      </div>
      <button
        class="text-[11px] font-medium text-on-surface-variant hover:text-red-600 border border-outline-variant/30 hover:border-red-200 px-2.5 py-1 rounded-lg transition-colors shrink-0"
        @click="store.clearActive()"
      >
        Disconnect
      </button>
    </div>

    <div v-else class="mb-6 flex items-center gap-2.5 px-4 py-3 bg-surface-container-low rounded-xl border border-outline-variant/20">
      <ZapOff :size="15" class="text-on-surface-variant/50 shrink-0" />
      <p class="text-[12px] text-on-surface-variant">No AI provider active. Using backend default. Configure a provider below to unlock direct AI access.</p>
    </div>

    <!-- Provider grid -->
    <div class="space-y-2">
      <div v-for="provider in PROVIDERS" :key="provider.id" class="border border-outline-variant/30 rounded-xl overflow-hidden bg-surface transition-colors" :class="{ 'border-primary/30 shadow-sm': expanded === provider.id }">

        <!-- Card header (always visible) -->
        <div
          class="flex items-center gap-3 px-4 py-3.5 cursor-pointer hover:bg-surface-container-low/50 transition-colors select-none"
          @click="toggle(provider.id)"
        >
          <!-- Provider icon -->
          <div :class="['w-9 h-9 rounded-xl flex items-center justify-center shrink-0', provider.color, provider.textColor]">
            <ProviderIcon :id="provider.id" :size="20" />
          </div>

          <!-- Name + tagline -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <span class="text-[13px] font-semibold text-on-surface">{{ provider.name }}</span>
              <span v-if="store.isActive(provider.id)" class="flex items-center gap-1 text-[10px] font-semibold text-primary">
                <Zap :size="10" />ACTIVE
              </span>
            </div>
            <p class="text-[11px] text-on-surface-variant/70 truncate">{{ provider.tagline }}</p>
          </div>

          <!-- Status badge -->
          <span :class="['text-[10px] font-semibold px-2 py-0.5 rounded-full shrink-0 uppercase tracking-wide', statusBadge(provider.id).classes]">
            {{ statusBadge(provider.id).label }}
          </span>

          <!-- Expand chevron -->
          <component :is="expanded === provider.id ? ChevronUp : ChevronDown" :size="15" class="text-on-surface-variant/50 shrink-0" />
        </div>

        <!-- Config panel (expanded) -->
        <Transition name="expand">
          <div v-if="expanded === provider.id" class="border-t border-outline-variant/20 bg-surface-container-low/30 px-5 py-4">
            <div class="space-y-4">

              <!-- API Key -->
              <div v-if="!provider.requiresNoKey">
                <div class="flex items-center justify-between mb-1.5">
                  <label class="text-[12px] font-medium text-on-surface">API Key</label>
                  <a
                    :href="provider.apiKeyLink"
                    target="_blank"
                    class="flex items-center gap-1 text-[11px] text-on-surface-variant/60 hover:text-primary transition-colors"
                  >
                    Get API key <ExternalLink :size="11" />
                  </a>
                </div>
                <div class="flex items-center gap-2">
                  <div class="flex-1 flex items-center bg-surface border border-outline-variant/40 rounded-lg overflow-hidden focus-within:border-outline transition-colors">
                    <input
                      v-model="getDraft(provider.id).apiKey"
                      :type="showKey[provider.id] ? 'text' : 'password'"
                      :placeholder="provider.apiKeyPlaceholder"
                      class="flex-1 bg-transparent text-[13px] text-on-surface px-3 py-2 outline-none placeholder:text-on-surface-variant/30 font-mono"
                    />
                    <button
                      class="px-2.5 text-on-surface-variant/50 hover:text-on-surface-variant transition-colors"
                      @click="toggleShowKey(provider.id)"
                    >
                      <component :is="showKey[provider.id] ? EyeOff : Eye" :size="14" />
                    </button>
                  </div>
                </div>
              </div>

              <div v-else class="flex items-center gap-2 px-3 py-2 bg-surface-container rounded-lg border border-outline-variant/20">
                <Wifi :size="14" class="text-on-surface-variant/60" />
                <p class="text-[12px] text-on-surface-variant">No API key required — connects to your local Ollama instance.</p>
              </div>

              <!-- Model selector -->
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <label class="text-[12px] font-medium text-on-surface">Model</label>
                  <a
                    v-if="provider.id === 'openrouter'"
                    href="https://openrouter.ai/models"
                    target="_blank"
                    class="flex items-center gap-1 text-[11px] text-on-surface-variant/60 hover:text-primary transition-colors"
                  >
                    Browse all models <ExternalLink :size="11" />
                  </a>
                </div>

                <!-- OpenRouter: free-text model ID input -->
                <template v-if="provider.id === 'openrouter'">
                  <input
                    v-model="getDraft(provider.id).model"
                    type="text"
                    placeholder="e.g. anthropic/claude-3.5-sonnet"
                    class="w-full bg-surface border border-outline-variant/40 text-on-surface text-[13px] rounded-lg px-3 py-2 outline-none focus:border-outline transition-colors font-mono placeholder:text-on-surface-variant/30"
                  />
                  <!-- Quick-pick chips -->
                  <div class="flex flex-wrap gap-1.5 mt-2">
                    <button
                      v-for="model in provider.models"
                      :key="model.id"
                      class="px-2 py-0.5 text-[11px] rounded-full border transition-colors"
                      :class="getDraft(provider.id).model === model.id
                        ? 'bg-primary text-on-primary border-primary'
                        : 'border-outline-variant/40 text-on-surface-variant hover:border-outline hover:text-on-surface'"
                      @click="getDraft(provider.id).model = model.id"
                    >
                      {{ model.name }}
                    </button>
                  </div>
                  <p class="text-[11px] text-on-surface-variant/50 mt-1.5 ml-0.5">
                    Enter any model ID from the OpenRouter catalogue, or click a chip above.
                  </p>
                </template>

                <!-- All other providers: dropdown -->
                <template v-else>
                  <select
                    v-model="getDraft(provider.id).model"
                    class="w-full bg-surface border border-outline-variant/40 text-on-surface text-[13px] rounded-lg px-3 py-2 outline-none focus:border-outline transition-colors cursor-pointer"
                  >
                    <option
                      v-for="model in provider.models"
                      :key="model.id"
                      :value="model.id"
                    >
                      {{ model.name }}{{ model.recommended ? ' ★' : '' }} — {{ (model.contextLength / 1000).toFixed(0) }}K ctx
                    </option>
                  </select>
                  <p class="text-[11px] text-on-surface-variant/60 mt-1.5 ml-0.5">
                    {{ provider.models.find((m) => m.id === getDraft(provider.id).model)?.description ?? '' }}
                  </p>
                </template>
              </div>

              <!-- Custom base URL (Ollama and other custom providers) -->
              <div v-if="provider.supportsCustomBaseUrl">
                <label class="text-[12px] font-medium text-on-surface block mb-1.5">{{ provider.customBaseUrlLabel ?? 'Base URL' }}</label>
                <input
                  v-model="getDraft(provider.id).baseUrl"
                  type="text"
                  :placeholder="provider.baseUrl"
                  class="w-full bg-surface border border-outline-variant/40 text-on-surface text-[13px] rounded-lg px-3 py-2 outline-none focus:border-outline transition-colors font-mono placeholder:text-on-surface-variant/30"
                />
              </div>

              <!-- Test result -->
              <template v-if="store.getConfig(provider.id).testStatus !== 'untested'">
                <!-- Success -->
                <div v-if="store.getConfig(provider.id).testStatus === 'success'"
                  class="flex items-center gap-2.5 px-3 py-2.5 rounded-lg bg-emerald-50 border border-emerald-200"
                >
                  <Check :size="14" class="text-emerald-600 shrink-0" />
                  <p class="text-[12px] font-medium text-emerald-800">
                    Connected successfully
                    <span class="font-normal text-[11px] opacity-70 ml-1">{{ latencyLabel(provider.id) }}</span>
                  </p>
                </div>

                <!-- Failure — rich error display -->
                <div v-else class="rounded-lg bg-red-50 border border-red-200 overflow-hidden">
                  <div class="flex items-start gap-2.5 px-3 py-2.5">
                    <TriangleAlert :size="14" class="text-red-500 shrink-0 mt-0.5" />
                    <div class="flex-1 min-w-0">
                      <p class="text-[12px] font-medium text-red-700">
                        Connection failed
                        <span class="font-normal text-[11px] opacity-70 ml-1">{{ latencyLabel(provider.id) }}</span>
                      </p>
                      <!-- Error message + hint -->
                      <p v-if="store.getConfig(provider.id).errorMessage" class="text-[11px] text-red-600 mt-1 break-words font-mono">
                        {{ store.getConfig(provider.id).errorMessage }}
                      </p>
                      <p class="text-[11px] text-red-500/70 mt-1.5 leading-relaxed">
                        {{ errorHint(store.getConfig(provider.id).errorMessage ?? '', provider.id) }}
                      </p>
                    </div>
                  </div>
                </div>
              </template>

              <!-- Action buttons -->
              <div class="flex items-center gap-2 pt-1">
                <!-- Test -->
                <button
                  :disabled="store.isTesting(provider.id) || (!provider.requiresNoKey && !getDraft(provider.id).apiKey.trim())"
                  class="flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-medium text-on-surface-variant border border-outline-variant/40 rounded-lg hover:bg-surface-container-high hover:text-on-surface transition-colors disabled:opacity-40"
                  @click="testProvider(provider.id)"
                >
                  <Loader2 v-if="store.isTesting(provider.id)" :size="13" class="animate-spin" />
                  <Wifi v-else :size="13" />
                  {{ store.isTesting(provider.id) ? 'Testing…' : 'Test connection' }}
                </button>

                <!-- Set active -->
                <button
                  v-if="!store.isActive(provider.id)"
                  :disabled="!store.isConfigured(provider.id) && !provider.requiresNoKey"
                  class="flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-medium bg-primary text-on-primary rounded-lg hover:opacity-90 transition-opacity disabled:opacity-40 ml-auto"
                  @click="setActive(provider.id)"
                >
                  <Zap :size="13" />
                  Set as active
                </button>
                <button
                  v-else
                  class="flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg ml-auto"
                  disabled
                >
                  <Check :size="13" />
                  Currently active
                </button>

                <!-- Clear -->
                <button
                  v-if="store.isConfigured(provider.id) && !provider.requiresNoKey"
                  class="p-1.5 text-on-surface-variant/40 hover:text-red-500 transition-colors"
                  title="Clear configuration"
                  @click="store.clearProvider(provider.id)"
                >
                  <Trash2 :size="14" />
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Footer note -->
    <p class="text-[11px] text-on-surface-variant/40 text-center mt-6 leading-relaxed">
      API keys are encrypted and stored in your browser's local storage. They are never transmitted to XL-MCP servers.
    </p>
  </div>
</template>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}
.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 600px;
}
</style>
