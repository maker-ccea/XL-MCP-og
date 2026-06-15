<script setup lang="ts">
import { computed } from 'vue'
import { BrainCircuit, Zap, Layers, GitMerge, Cpu } from '@lucide/vue'
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


const siIconMap: Partial<Record<ProviderID, { path: string; hex: string }>> = {
  anthropic:  siAnthropic,
  google:     siGooglegemini,
  mistral:    siMistralai,
  ollama:     siOllama,
  openrouter: siOpenrouter,
  perplexity: siPerplexity
}


const lucideIconMap = {
  openai:    BrainCircuit,  
  groq:      Zap,           
  cohere:    Layers,        
  together:  GitMerge,      
  custom:    Cpu            
} as Partial<Record<ProviderID, unknown>>

const siIcon    = computed(() => siIconMap[props.id])
const lucideIcon = computed(() => lucideIconMap[props.id])
</script>

<template>
  
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

  
  <component
    v-else-if="lucideIcon"
    :is="lucideIcon"
    :size="size"
    aria-hidden="true"
  />
</template>
