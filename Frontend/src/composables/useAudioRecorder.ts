import { ref } from 'vue'

export function useAudioRecorder(onTranscript: (text: string) => void) {
  const isListening = ref(false)
  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
  const supported = !!SpeechRecognition
  let recognition: any = null

  if (supported) {
    recognition = new SpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = false
    recognition.lang = 'en-US'

    recognition.onstart = () => {
      isListening.value = true
    }

    recognition.onresult = (event: any) => {
      const result = event.results[0][0].transcript
      if (result) {
        onTranscript(result)
      }
    }

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error)
      isListening.value = false
    }

    recognition.onend = () => {
      isListening.value = false
    }
  }

  function toggleListening(): void {
    if (!supported || !recognition) return
    if (isListening.value) {
      recognition.stop()
    } else {
      recognition.start()
    }
  }

  return {
    isListening,
    supported,
    toggleListening
  }
}
