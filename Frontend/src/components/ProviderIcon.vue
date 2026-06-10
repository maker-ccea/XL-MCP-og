<script setup lang="ts">
import { computed } from 'vue'
import { BrainCircuit, Zap, Layers, GitMerge } from '@lucide/vue'
import {
  siAnthropic,
  siGooglegemini,
  siMistralai,
  siOllama,
  siOpenrouter,
  siPerplexity
} from 'simple-icons'
import type { ProviderID } from '@/config/providers'

interface Props {
  id: ProviderID
  size?: number
}

const props = withDefaults(defineProps<Props>(), { size: 18 })

// Brand SVG paths from simple-icons (correct, official paths)
const siIconMap: Partial<Record<ProviderID, { path: string; hex: string }>> = {
  anthropic:  siAnthropic,
  google:     siGooglegemini,
  mistral:    siMistralai,
  ollama:     siOllama,
  openrouter: siOpenrouter,
  perplexity: siPerplexity
}

// Lucide icons for providers not in simple-icons
const lucideIconMap = {
  openai:    BrainCircuit,  // GPT = intelligence/reasoning
  groq:      Zap,           // Groq = ultra-fast inference
  cohere:    Layers,        // Cohere = enterprise data layers
  together:  GitMerge       // Together = merging/collaboration
} as Partial<Record<ProviderID, unknown>>

const siIcon    = computed(() => siIconMap[props.id])
const lucideIcon = computed(() => lucideIconMap[props.id])
</script>

<template>
  <!-- Official brand SVG from simple-icons -->
  <svg
    v-if="siIcon"
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <path :d="siIcon.path" />
  </svg>

  <!-- Lucide fallback for OpenAI / Groq / Cohere / Together -->
  <component
    v-else-if="lucideIcon"
    :is="lucideIcon"
    :size="size"
    aria-hidden="true"
  />
</template>
