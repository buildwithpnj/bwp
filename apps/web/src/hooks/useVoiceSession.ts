import { useState } from 'react';
import { usePathname } from 'next/navigation';
import { CopilotMessage } from './useCopilotSession';

export function useVoiceSession(
  onTranscriptionReceived: (userMsg: CopilotMessage, assistantMsg: CopilotMessage) => void
) {
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
        
        const userMsg: CopilotMessage = {
          role: 'user',
          content: data.transcription
        };
        
        const assistantMsg: CopilotMessage = {
          role: 'assistant',
          content: data.reply,
          suggested_action: data.suggested_action,
          approval_required: data.approval_required,
          approval_request: data.approval_request,
          token: data.token,
          approval_decided: false
        };
        
        onTranscriptionReceived(userMsg, assistantMsg);
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
