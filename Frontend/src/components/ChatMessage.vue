<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import { Bot, User, AlertCircle, Loader2 } from '@lucide/vue'
import type { ChatMessage } from '@/types'
import ActionCard from './ActionCard.vue'

interface Props {
  message: ChatMessage
}

const props = defineProps<Props>()

function highlightCode(code: string, lang?: string): string {
  if (lang === 'excel-actions' || lang === 'json' || lang === 'js' || lang === 'javascript') {
    return code
      .replace(/(".*?")/g, '<span class="text-emerald-400 font-mono">$1</span>')
      .replace(/\b(true|false|null)\b/g, '<span class="text-amber-400 font-bold">$1</span>')
      .replace(/\b(\d+)\b/g, '<span class="text-sky-400">$1</span>')
      .replace(/\b(const|let|var|function|return|import|from|export)\b/g, '<span class="text-indigo-300 font-semibold">$1</span>')
  }
  if (lang === 'excel' || code.trim().startsWith('=')) {
    return code
      .replace(/(=[A-Z]+|\b[A-Z]+\b)(?=\()/g, '<span class="text-indigo-300 font-semibold">$1</span>')
      .replace(/\b([A-Z]+\d+|\b[A-Z]+\d+:[A-Z]+\d+)\b/g, '<span class="text-sky-300 font-medium">$1</span>')
      .replace(/(".*?")/g, '<span class="text-emerald-400">$1</span>')
      .replace(/\b(\d+(\.\d+)?)\b/g, '<span class="text-sky-400">$1</span>')
  }
  return code
}

const customRenderer = {
  code(token: { text: string; lang?: string }): string {
    const text = token.text
    const lang = token.lang
    const highlighted = highlightCode(text, lang)
    return `<pre class="bg-[#1c1b1b] text-[#e5e2e1] p-3 rounded-lg overflow-x-auto font-mono text-[12px] my-2"><code class="language-${lang || 'text'}">${highlighted}</code></pre>`
  }
}

marked.use({ renderer: customRenderer as any })

const renderedContent = computed(() => {
  if (!props.message.content) return ''
  return marked.parse(props.message.content) as string
})

const isUser = computed(() => props.message.role === 'user')
const isStreaming = computed(() => props.message.status === 'streaming')
const isError = computed(() => props.message.status === 'error')

const progressPercent = computed(() => {
  if (!props.message.plan || props.message.plan.length === 0) return 0
  const current = props.message.results?.length || 0
  return Math.round((current / props.message.plan.length) * 100)
})

function formatTime(date: Date): string {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div :class="['flex gap-3 mb-4', isUser ? 'flex-row-reverse' : 'flex-row']">
    
    <div
      :class="[
        'w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5',
        isUser ? 'bg-primary' : 'bg-surface-container border border-outline-variant/40'
      ]"
    >
      <User v-if="isUser" :size="14" class="text-on-primary" />
      <Bot v-else :size="14" class="text-secondary" />
    </div>

    
    <div :class="['max-w-[75%] space-y-2', isUser ? 'items-end' : 'items-start', 'flex flex-col']">
      <div
        :class="[
          'px-4 py-3 rounded-2xl text-body-main',
          isUser
            ? 'bg-primary text-on-primary rounded-tr-sm'
            : isError
              ? 'bg-error-container text-on-error-container rounded-tl-sm'
              : 'bg-surface border border-outline-variant/30 text-on-surface rounded-tl-sm shadow-sm'
        ]"
      >
        
        <div v-if="isStreaming && !message.content" class="flex items-center gap-1.5 py-0.5">
          <Loader2 :size="14" class="animate-spin text-on-surface-variant" />
          <span class="text-card-body text-on-surface-variant">Thinking...</span>
        </div>

        
        <div v-if="isError" class="flex items-center gap-2 mb-1">
          <AlertCircle :size="14" />
          <span class="text-card-title font-medium">Error</span>
        </div>

        
        <div v-if="message.imageUrl" class="mb-2 max-w-[280px] rounded-lg overflow-hidden border border-outline-variant/20 shadow-sm bg-black/5">
          <img :src="message.imageUrl" class="w-full h-auto max-h-[180px] object-contain block" />
        </div>

        
        <div
          v-if="message.content"
          class="prose-chat"
          :class="isUser ? 'text-on-primary' : ''"
          v-html="renderedContent"
        />
        
        <span
          v-else-if="!isStreaming && !isError"
          class="text-card-body text-on-surface-variant/50 italic"
        >The model returned an empty response. Go to Settings → Integrations to configure a provider.</span>

        
        <span v-if="isStreaming && message.content" class="inline-block w-0.5 h-4 bg-current ml-0.5 animate-pulse" />

        
        <div v-if="isStreaming && message.plan && message.plan.length > 0" class="w-full mt-3 pt-2.5 border-t border-outline-variant/20">
          <div class="flex items-center justify-between text-[10.5px] text-on-surface-variant/70 mb-1.5 font-mono">
            <span>Executing: {{ message.results?.length || 0 }} / {{ message.plan.length }} actions</span>
            <span class="font-bold">{{ progressPercent }}%</span>
          </div>
          <div class="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden border border-outline-variant/10">
            <div
              class="h-full bg-primary transition-all duration-300 ease-out"
              :style="{ width: `${progressPercent}%` }"
            />
          </div>
        </div>
      </div>

      
      <div v-if="message.results && message.results.length > 0" class="w-full space-y-1.5">
        <ActionCard
          v-for="(result, idx) in message.results"
          :key="idx"
          :result="result"
        />
      </div>

      
      <span class="text-[11px] text-on-surface-variant/50 px-1">
        {{ formatTime(message.timestamp) }}
      </span>
    </div>
  </div>
</template>

