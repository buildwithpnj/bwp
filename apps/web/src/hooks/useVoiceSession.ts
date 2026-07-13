import { useState } from 'react';
import { usePathname } from 'next/navigation';

export function useVoiceSession(onTranscriptionReceived: (text: string, reply: string) => void) {
  const pathname = usePathname();
  const [isListening, setIsListening] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const startListening = () => {
    setIsListening(true);
  };

  const stopListening = async () => {
    setIsListening(false);
    setIsThinking(true);

    try {
      const response = await fetch('/api/copilot/voice', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_route: pathname || '/',
          visible_module_hints: [],
          selected_entity_id: null,
          workflow_state: null
        })
      });

      if (response.ok) {
        const data = await response.json();
        onTranscriptionReceived(data.transcription, data.reply);
      }
    } catch (e) {
      console.error('Voice session error:', e);
    } finally {
      setIsThinking(false);
    }
  };

  return {
    isListening,
    isThinking,
    startListening,
    stopListening
  };
}
