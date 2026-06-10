import { ref } from 'vue'
import { useChatStore } from '@/stores/chatStore'

export function useChat() {
  const chatStore = useChatStore()
  const inputText = ref('')

  async function submit(): Promise<void> {
    const text = inputText.value.trim()
    if (!text || chatStore.loading) return
    inputText.value = ''
    await chatStore.sendMessage(text)
  }

  function handleKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      submit()
    }
  }

  return { inputText, submit, handleKeydown }
}

