<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowLeft, HelpCircle, Bell, User, Palette, BellRing, Keyboard,
  Table2, Brain, Lock, Network, Check
} from '@lucide/vue'
import { useSettingsStore } from '@/stores/settingsStore'
import type { AppSettings, AvatarColor } from '@/types'
import IntegrationsSection from '@/components/IntegrationsSection.vue'

const router = useRouter()
const settingsStore = useSettingsStore()

// Deep-copy so nested profile object is independent
const local = reactive<AppSettings>({
  ...settingsStore.settings,
  profile: { ...settingsStore.settings.profile }
})

type Section = 'profile' | 'appearance' | 'notifications' | 'shortcuts' | 'excel' | 'ai' | 'privacy' | 'integrations'
const activeSection = ref<Section>('ai')

const generalNav = [
  { id: 'profile' as Section, label: 'Local Profile', icon: User },
  { id: 'appearance' as Section, label: 'Appearance', icon: Palette },
  { id: 'notifications' as Section, label: 'Notifications', icon: BellRing },
  { id: 'shortcuts' as Section, label: 'Shortcuts', icon: Keyboard }
]

const workspaceNav = [
  { id: 'excel' as Section, label: 'Excel connection', icon: Table2 },
  { id: 'ai' as Section, label: 'AI behavior', icon: Brain },
  { id: 'privacy' as Section, label: 'Privacy & data', icon: Lock },
  { id: 'integrations' as Section, label: 'Integrations', icon: Network }
]

// ── Profile helpers ───────────────────────────────────────────────────────────

const avatarColorOptions: { id: AvatarColor; bg: string; ring: string }[] = [
  { id: 'zinc',    bg: 'bg-zinc-200',    ring: 'ring-zinc-400' },
  { id: 'rose',    bg: 'bg-rose-100',    ring: 'ring-rose-400' },
  { id: 'amber',   bg: 'bg-amber-100',   ring: 'ring-amber-400' },
  { id: 'emerald', bg: 'bg-emerald-100', ring: 'ring-emerald-400' },
  { id: 'sky',     bg: 'bg-sky-100',     ring: 'ring-sky-400' },
  { id: 'violet',  bg: 'bg-violet-100',  ring: 'ring-violet-400' },
  { id: 'orange',  bg: 'bg-orange-100',  ring: 'ring-orange-400' }
]

const avatarBgMap: Record<AvatarColor, string> = {
  zinc:    'bg-zinc-200 text-zinc-700',
  rose:    'bg-rose-100 text-rose-700',
  amber:   'bg-amber-100 text-amber-700',
  emerald: 'bg-emerald-100 text-emerald-700',
  sky:     'bg-sky-100 text-sky-700',
  violet:  'bg-violet-100 text-violet-700',
  orange:  'bg-orange-100 text-orange-700'
}

const initials = computed(() => {
  const name = local.profile.displayName.trim()
  if (!name) return ''
  const parts = name.split(/\s+/).filter(Boolean)
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
})

const avatarBg = computed(() => avatarBgMap[local.profile.avatarColor])

// ── Persistence ───────────────────────────────────────────────────────────────

const saved = ref(false)

function save(): void {
  Object.assign(settingsStore.settings, {
    ...local,
    profile: { ...local.profile }
  })
  settingsStore.save()
  saved.value = true
  setTimeout(() => { saved.value = false }, 2000)
}

function reset(): void {
  const fresh = settingsStore.reset()
  Object.assign(local, { ...fresh, profile: { ...fresh.profile } })
}
</script>

<template>
  <div class="bg-surface-container-lowest font-body-main text-on-surface antialiased h-screen flex flex-col overflow-hidden">
    <!-- Top App Bar -->
    <header class="fixed top-0 w-full z-50 flex justify-between items-center px-8 h-14 bg-surface border-b border-outline-variant/30">
      <div class="flex items-center gap-4">
        <span class="text-[18px] font-semibold text-on-surface tracking-tight">XL-MCP</span>
      </div>
      <div class="flex items-center gap-3">
        <button
          class="flex items-center gap-1.5 text-card-body text-on-surface-variant hover:text-on-surface transition-colors mr-2"
          @click="router.push('/')"
        >
          <ArrowLeft :size="18" />
          <span>Back to Chat</span>
        </button>
        <HelpCircle :size="18" class="text-on-surface-variant cursor-pointer hover:text-on-surface transition-colors" />
        <Bell :size="18" class="text-on-surface-variant cursor-pointer hover:text-on-surface transition-colors" />
      </div>
    </header>

    <!-- Settings Container -->
    <main class="pt-14 h-screen flex items-center justify-center bg-surface-container-lowest">
      <div class="relative w-full max-w-[1024px] h-[680px] bg-surface border border-outline-variant/30 rounded-lg overflow-hidden flex shadow-2xl">
        <!-- Sidebar Nav -->
        <aside class="w-[240px] bg-surface-container-low/50 border-r border-outline-variant/30 flex flex-col">
          <div class="p-5">
            <h2 class="text-[16px] font-semibold text-on-surface mb-5">Settings</h2>
            <nav class="space-y-6">
              <!-- General -->
              <div>
                <p class="font-label-caps text-label-caps text-on-surface-variant/70 mb-2 px-2 uppercase">General</p>
                <ul class="space-y-[2px]">
                  <li
                    v-for="item in generalNav"
                    :key="item.id"
                    :class="[
                      'flex items-center px-2 py-1.5 text-[13px] font-medium cursor-pointer rounded transition-all',
                      activeSection === item.id
                        ? 'bg-surface-container-highest/80 text-on-surface shadow-sm border border-outline-variant/20'
                        : 'text-on-surface-variant hover:bg-surface-container-highest/50 hover:text-on-surface'
                    ]"
                    @click="activeSection = item.id"
                  >
                    <component :is="item.icon" :size="16" class="mr-2.5" />
                    {{ item.label }}
                  </li>
                </ul>
              </div>
              <!-- Workspace -->
              <div>
                <p class="font-label-caps text-label-caps text-on-surface-variant/70 mb-2 px-2 uppercase">Workspace</p>
                <ul class="space-y-[2px]">
                  <li
                    v-for="item in workspaceNav"
                    :key="item.id"
                    :class="[
                      'flex items-center px-2 py-1.5 text-[13px] font-medium cursor-pointer rounded transition-all',
                      activeSection === item.id
                        ? 'bg-surface-container-highest/80 text-on-surface shadow-sm border border-outline-variant/20'
                        : 'text-on-surface-variant hover:bg-surface-container-highest/50 hover:text-on-surface'
                    ]"
                    @click="activeSection = item.id"
                  >
                    <component :is="item.icon" :size="16" class="mr-2.5" />
                    {{ item.label }}
                  </li>
                </ul>
              </div>
            </nav>
          </div>
          <div class="mt-auto p-5 border-t border-outline-variant/30">
            <p class="font-mono text-mono-small text-outline/60 tracking-wider">VERSION 1.0.0-STABLE</p>
          </div>
        </aside>

        <!-- Content Panel -->
        <section class="flex-1 overflow-y-auto bg-surface p-8">
          <!-- AI Behavior -->
          <div v-if="activeSection === 'ai'" class="max-w-[640px] mx-auto">
            <header class="mb-8 border-b border-outline-variant/20 pb-4">
              <h1 class="text-[20px] font-semibold text-on-surface mb-1">AI Behavior</h1>
              <p class="text-[13px] text-on-surface-variant/80">Configure how the intelligence layer interacts with your datasets and provides suggestions.</p>
            </header>

            <!-- Interactive Behavior -->
            <div class="mb-8">
              <h3 class="font-label-caps text-label-caps text-on-surface-variant/70 mb-3 uppercase tracking-wider">Interactive Behavior</h3>
              <div class="border border-outline-variant/30 rounded-lg bg-surface-container-lowest/50 divide-y divide-outline-variant/20">
                <template v-for="toggle in [
                  { label: 'Action preview', desc: 'Show visual highlight before applying changes.', key: 'actionPreview' },
                  { label: 'Auto-suggest', desc: 'Predict formulas as you type in the grid.', key: 'autoSuggest' },
                  { label: 'Formula explanations', desc: 'Briefly describe the logic of complex formulas.', key: 'formulaExplanations' },
                  { label: 'Streaming responses', desc: 'Display AI output character-by-character.', key: 'streamingResponses' }
                ]" :key="toggle.key">
                  <div class="flex items-center justify-between p-4">
                    <div class="pr-4">
                      <p class="text-[13px] font-medium text-on-surface mb-0.5">{{ toggle.label }}</p>
                      <p class="text-[11px] text-on-surface-variant/70 leading-relaxed">{{ toggle.desc }}</p>
                    </div>
                    <label class="relative inline-flex items-center cursor-pointer">
                      <input
                        v-model="(local as any)[toggle.key]"
                        type="checkbox"
                        class="sr-only peer"
                      />
                      <div class="w-8 h-[18px] bg-surface-variant border border-outline-variant/50 rounded-full peer-checked:bg-primary peer-checked:border-primary transition-all relative">
                        <div class="absolute top-[1px] left-[1px] w-3.5 h-3.5 bg-on-surface rounded-full shadow-sm transition-transform peer-checked:translate-x-3.5 peer-checked:bg-background" />
                      </div>
                    </label>
                  </div>
                </template>
              </div>
            </div>

            <!-- Context & Range -->
            <div class="mb-8">
              <h3 class="font-label-caps text-label-caps text-on-surface-variant/70 mb-3 uppercase tracking-wider">Context &amp; Range</h3>
              <div class="border border-outline-variant/30 rounded-lg bg-surface-container-lowest/50 divide-y divide-outline-variant/20">
                <div class="flex items-center justify-between p-4">
                  <div class="pr-4">
                    <p class="text-[13px] font-medium text-on-surface mb-0.5">Active sheet context</p>
                    <p class="text-[11px] text-on-surface-variant/70 leading-relaxed">Allow AI to read current sheet data.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input v-model="local.activeSheetContext" type="checkbox" class="sr-only peer" />
                    <div class="w-8 h-[18px] bg-surface-variant border border-outline-variant/50 rounded-full peer-checked:bg-primary peer-checked:border-primary transition-all relative">
                      <div class="absolute top-[1px] left-[1px] w-3.5 h-3.5 bg-on-surface rounded-full shadow-sm transition-transform peer-checked:translate-x-3.5 peer-checked:bg-background" />
                    </div>
                  </label>
                </div>
                <div class="flex items-center justify-between p-4">
                  <div class="pr-4">
                    <p class="text-[13px] font-medium text-on-surface mb-0.5">Workbook name</p>
                    <p class="text-[11px] text-on-surface-variant/70 leading-relaxed">Include filename in context for specific tasks.</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input v-model="local.workbookNameContext" type="checkbox" class="sr-only peer" />
                    <div class="w-8 h-[18px] bg-surface-variant border border-outline-variant/50 rounded-full peer-checked:bg-primary peer-checked:border-primary transition-all relative">
                      <div class="absolute top-[1px] left-[1px] w-3.5 h-3.5 bg-on-surface rounded-full shadow-sm transition-transform peer-checked:translate-x-3.5 peer-checked:bg-background" />
                    </div>
                  </label>
                </div>
                <div class="flex items-center justify-between p-4">
                  <div class="pr-4">
                    <p class="text-[13px] font-medium text-on-surface mb-0.5">Max context rows</p>
                    <p class="text-[11px] text-on-surface-variant/70 leading-relaxed">The maximum data depth the AI analyzes.</p>
                  </div>
                  <select
                    v-model.number="local.maxContextRows"
                    class="bg-surface-container-low border border-outline-variant/40 text-on-surface text-[12px] rounded px-2.5 py-1.5 outline-none focus:border-outline transition-colors min-w-[100px] cursor-pointer"
                  >
                    <option :value="100">100</option>
                    <option :value="500">500</option>
                    <option :value="1000">1000</option>
                    <option :value="5000">5000</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Save / Reset -->
            <div class="flex items-center justify-end gap-3 mt-8 pb-8">
              <button
                class="px-4 py-1.5 text-[12px] font-medium text-on-surface-variant border border-outline-variant/30 rounded hover:bg-surface-container-highest/50 hover:text-on-surface transition-all"
                @click="reset"
              >
                Reset
              </button>
              <button
                class="px-4 py-1.5 text-[12px] font-medium bg-primary text-background rounded hover:opacity-90 active:scale-95 transition-all shadow-sm"
                @click="save"
              >
                Save Changes
              </button>
            </div>
          </div>

          <!-- Appearance -->
          <div v-else-if="activeSection === 'appearance'" class="max-w-[640px] mx-auto">
            <header class="mb-8 border-b border-outline-variant/20 pb-4">
              <h1 class="text-[20px] font-semibold text-on-surface mb-1">Appearance</h1>
              <p class="text-[13px] text-on-surface-variant/80">Customize the look and feel of XL-MCP.</p>
            </header>
            <div class="border border-outline-variant/30 rounded-lg bg-surface-container-lowest/50 divide-y divide-outline-variant/20">
              <div class="flex items-center justify-between p-4">
                <div class="pr-4">
                  <p class="text-[13px] font-medium text-on-surface mb-0.5">Theme</p>
                  <p class="text-[11px] text-on-surface-variant/70 leading-relaxed">Choose your preferred color scheme.</p>
                </div>
                <select
                  v-model="local.theme"
                  class="bg-surface-container-low border border-outline-variant/40 text-on-surface text-[12px] rounded px-2.5 py-1.5 outline-none focus:border-outline transition-colors min-w-[120px] cursor-pointer"
                >
                  <option value="light">Light</option>
                  <option value="dark">Dark</option>
                  <option value="system">System</option>
                </select>
              </div>
            </div>
            <div class="flex items-center justify-end gap-3 mt-8">
              <button class="px-4 py-1.5 text-[12px] font-medium bg-primary text-background rounded hover:opacity-90 transition-all shadow-sm" @click="save">
                Save Changes
              </button>
            </div>
          </div>

          <!-- Excel Connection -->
          <div v-else-if="activeSection === 'excel'" class="max-w-[640px] mx-auto">
            <header class="mb-8 border-b border-outline-variant/20 pb-4">
              <h1 class="text-[20px] font-semibold text-on-surface mb-1">Excel Connection</h1>
              <p class="text-[13px] text-on-surface-variant/80">Status of the Microsoft Excel and backend connection.</p>
            </header>
            <div class="border border-outline-variant/30 rounded-lg bg-surface-container-lowest/50 p-6 space-y-4">
              <p class="text-[13px] text-on-surface-variant">
                XL-MCP connects to a local Python backend (port 8000) which communicates with Microsoft Excel via xlwings.
              </p>
              <div class="bg-primary-container text-inverse-on-surface text-[11px] font-mono rounded-lg px-4 py-3">
                uvicorn main:app --host 127.0.0.1 --port 8000
              </div>
              <p class="text-[11px] text-on-surface-variant/70">Make sure Excel is open and the backend is running before sending messages.</p>
            </div>
          </div>

          <!-- Local Profile -->
          <div v-else-if="activeSection === 'profile'" class="max-w-[640px] mx-auto">
            <header class="mb-8 border-b border-outline-variant/20 pb-4">
              <h1 class="text-[20px] font-semibold text-on-surface mb-1">Local Profile</h1>
              <p class="text-[13px] text-on-surface-variant/80">Personalize your workspace. All data is stored locally on this device.</p>
            </header>

            <!-- Avatar + name preview card -->
            <div class="flex items-center gap-5 p-5 mb-6 border border-outline-variant/30 rounded-xl bg-surface-container-lowest/50">
              <div :class="['w-[64px] h-[64px] rounded-full flex items-center justify-center shrink-0 text-[22px] font-semibold select-none transition-colors', avatarBg]">
                <span v-if="initials">{{ initials }}</span>
                <User v-else :size="26" class="text-on-surface-variant/50" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-[15px] font-semibold text-on-surface truncate">{{ local.profile.displayName || 'Your Name' }}</p>
                <p class="text-card-body text-on-surface-variant truncate mt-0.5">{{ local.profile.role || 'Role not set' }}</p>
                <p class="text-[11px] text-on-surface-variant/50 mt-1">Preview of how your profile appears</p>
              </div>
            </div>

            <!-- Fields -->
            <div class="mb-6">
              <h3 class="font-label-caps text-label-caps text-on-surface-variant/70 mb-3 uppercase tracking-wider">Identity</h3>
              <div class="border border-outline-variant/30 rounded-lg bg-surface-container-lowest/50 divide-y divide-outline-variant/20">
                <div class="p-4">
                  <label class="text-[13px] font-medium text-on-surface mb-1 block">Display name</label>
                  <p class="text-[11px] text-on-surface-variant/70 mb-2">Shown in the workspace greeting and message bubbles.</p>
                  <input v-model="local.profile.displayName" type="text" maxlength="48" placeholder="e.g. Sarah Chen"
                    class="w-full bg-surface border border-outline-variant/40 text-on-surface text-[13px] rounded-lg px-3 py-2 outline-none focus:border-outline transition-colors placeholder:text-on-surface-variant/40" />
                </div>
                <div class="p-4">
                  <label class="text-[13px] font-medium text-on-surface mb-1 block">Role / title</label>
                  <p class="text-[11px] text-on-surface-variant/70 mb-2">Your job title or team role.</p>
                  <input v-model="local.profile.role" type="text" maxlength="64" placeholder="e.g. Financial Analyst"
                    class="w-full bg-surface border border-outline-variant/40 text-on-surface text-[13px] rounded-lg px-3 py-2 outline-none focus:border-outline transition-colors placeholder:text-on-surface-variant/40" />
                </div>
                <div class="p-4">
                  <label class="text-[13px] font-medium text-on-surface mb-1 block">Bio</label>
                  <p class="text-[11px] text-on-surface-variant/70 mb-2">A short description about yourself or your work context.</p>
                  <textarea v-model="local.profile.bio" rows="3" maxlength="200" placeholder="e.g. I work on quarterly financial reports and budget forecasting."
                    class="w-full bg-surface border border-outline-variant/40 text-on-surface text-[13px] rounded-lg px-3 py-2 outline-none focus:border-outline transition-colors placeholder:text-on-surface-variant/40 resize-none" />
                  <p class="text-[11px] text-on-surface-variant/40 text-right mt-1">{{ local.profile.bio.length }}/200</p>
                </div>
              </div>
            </div>

            <!-- Avatar color -->
            <div class="mb-8">
              <h3 class="font-label-caps text-label-caps text-on-surface-variant/70 mb-3 uppercase tracking-wider">Avatar Color</h3>
              <div class="border border-outline-variant/30 rounded-lg bg-surface-container-lowest/50 p-4">
                <p class="text-[11px] text-on-surface-variant/70 mb-3">Choose the color for your avatar initials.</p>
                <div class="flex items-center gap-2.5 flex-wrap">
                  <button v-for="color in avatarColorOptions" :key="color.id"
                    :class="['w-8 h-8 rounded-full transition-all flex items-center justify-center', color.bg,
                      local.profile.avatarColor === color.id ? ['ring-2 ring-offset-2', color.ring] : 'hover:scale-110']"
                    :title="color.id" @click="local.profile.avatarColor = color.id">
                    <Check v-if="local.profile.avatarColor === color.id" :size="13" class="text-on-surface/60" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-between mt-2 pb-8">
              <p v-if="saved" class="text-[12px] text-emerald-600 font-medium flex items-center gap-1.5">
                <Check :size="13" /> Profile saved
              </p>
              <span v-else />
              <div class="flex items-center gap-3">
                <button class="px-4 py-1.5 text-[12px] font-medium text-on-surface-variant border border-outline-variant/30 rounded hover:bg-surface-container-highest/50 hover:text-on-surface transition-all" @click="reset">Reset</button>
                <button class="px-4 py-1.5 text-[12px] font-medium bg-primary text-background rounded hover:opacity-90 active:scale-95 transition-all shadow-sm" @click="save">Save Changes</button>
              </div>
            </div>
          </div>



          <!-- Integrations -->
          <div v-else-if="activeSection === 'integrations'">
            <IntegrationsSection />
          </div>

          <!-- Other sections (placeholder) -->
          <div v-else class="max-w-[640px] mx-auto flex flex-col items-center justify-center py-20 text-center gap-3">
            <div class="w-12 h-12 rounded-full bg-surface-container-low flex items-center justify-center">
              <component :is="[...generalNav, ...workspaceNav].find(n => n.id === activeSection)?.icon ?? User" :size="22" class="text-on-surface-variant" />
            </div>
            <p class="text-[15px] font-medium text-on-surface">Coming soon</p>
            <p class="text-card-body text-on-surface-variant">This section is not yet available.</p>
          </div>
        </section>
      </div>

      <!-- Disclaimer -->
      <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-1.5 text-[11px] text-outline/50 pointer-events-none">
        <HelpCircle :size="12" />
        <span>Settings apply to the current workspace.</span>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Peer workaround for scoped toggle — target inner div via sibling selector */
input[type='checkbox']:checked ~ div > div {
  transform: translateX(14px);
  background-color: white;
}
</style>
