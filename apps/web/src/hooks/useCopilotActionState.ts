import { useState } from 'react';

export type ActionStatus = 'idle' | 'executing' | 'waiting_for_approval' | 'approved' | 'denied' | 'failed';

export function useCopilotActionState() {
  const [status, setStatus] = useState<ActionStatus>('idle');
  const [message, setMessage] = useState<string>('');

  const resetState = () => {
    setStatus('idle');
    setMessage('');
  };

  return {
    status,
    setStatus,
    message,
    setMessage,
    resetState
  };
}
