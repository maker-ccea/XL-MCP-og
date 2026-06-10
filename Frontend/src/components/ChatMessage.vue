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

const renderedContent = computed(() => {
  if (!props.message.content) return ''
  return marked.parse(props.message.content) as string
})

const isUser = computed(() => props.message.role === 'user')
const isStreaming = computed(() => props.message.status === 'streaming')
const isError = computed(() => props.message.status === 'error')

function formatTime(date: Date): string {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<template>
  <div :class="['flex gap-3 mb-4', isUser ? 'flex-row-reverse' : 'flex-row']">
    <!-- Avatar -->
    <div
      :class="[
        'w-7 h-7 rounded-full flex items-center justify-center shrink-0 mt-0.5',
        isUser ? 'bg-primary' : 'bg-surface-container border border-outline-variant/40'
      ]"
    >
      <User v-if="isUser" :size="14" class="text-on-primary" />
      <Bot v-else :size="14" class="text-secondary" />
    </div>

    <!-- Bubble -->
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
        <!-- Streaming indicator -->
        <div v-if="isStreaming && !message.content" class="flex items-center gap-1.5 py-0.5">
          <Loader2 :size="14" class="animate-spin text-on-surface-variant" />
          <span class="text-card-body text-on-surface-variant">Thinking...</span>
        </div>

        <!-- Error icon -->
        <div v-if="isError" class="flex items-center gap-2 mb-1">
          <AlertCircle :size="14" />
          <span class="text-card-title font-medium">Error</span>
        </div>

        <!-- Content -->
        <div
          v-if="message.content"
          class="prose-chat"
          :class="isUser ? 'text-on-primary' : ''"
          v-html="renderedContent"
        />
        <!-- Fallback: done but content is empty (should be caught by the store guard above) -->
        <span
          v-else-if="!isStreaming && !isError"
          class="text-card-body text-on-surface-variant/50 italic"
        >The model returned an empty response. Go to Settings → Integrations to configure a provider.</span>

        <!-- Streaming cursor -->
        <span v-if="isStreaming && message.content" class="inline-block w-0.5 h-4 bg-current ml-0.5 animate-pulse" />
      </div>

      <!-- Action results cards -->
      <div v-if="message.results && message.results.length > 0" class="w-full space-y-1.5">
        <ActionCard
          v-for="(result, idx) in message.results"
          :key="idx"
          :result="result"
        />
      </div>

      <!-- Timestamp -->
      <span class="text-[11px] text-on-surface-variant/50 px-1">
        {{ formatTime(message.timestamp) }}
      </span>
    </div>
  </div>
</template>

