import { ref } from 'vue'
import { useChatStore } from '@/stores/chatStore'

export function useChat() {
  const chatStore = useChatStore()
  const inputText = ref('')
  const imageUrl = ref('')

  async function submit(): Promise<void> {
    const text = inputText.value.trim()
    const img = imageUrl.value
    if ((!text && !img) || chatStore.loading) return
    inputText.value = ''
    imageUrl.value = ''
    await chatStore.sendMessage(text, img)
  }

  function handleKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      submit()
    }
  }

  return { inputText, imageUrl, submit, handleKeydown }
}

