'use client';

import { useState } from 'react';
import { useCopilotSession, CopilotMessage } from '@/hooks/useCopilotSession';
import { CopilotDrawer } from './CopilotDrawer';

export function GlobalCopilotShell() {
  const { isOpen, setIsOpen, messages, sendMessage, isSending } = useCopilotSession();
  const [extraMessages, setExtraMessages] = useState<CopilotMessage[]>([]);

  // Local helper to merge voice/STT triggers
  const handleAddAssistantMessage = (userText: string, reply: string) => {
    const userMsg: CopilotMessage = { role: 'user', content: userText };
    const replyMsg: CopilotMessage = { role: 'assistant', content: reply };
    setExtraMessages(prev => [...prev, userMsg, replyMsg]);
  };

  const combinedMessages = [...messages, ...extraMessages];

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-40 flex h-12 w-12 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lg hover:bg-primary/90 hover:scale-105 active:scale-95 transition-all duration-200"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
            className="w-6 h-6 animate-pulse"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 17.25 4.5H6.75A2.25 2.25 0 0 0 4.5 6.75v10.5a2.25 2.25 0 0 0 2.25 2.25Z"
            />
          </svg>
        </button>
      )}

      {/* Drawer */}
      <CopilotDrawer
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        messages={combinedMessages}
        sendMessage={sendMessage}
        isSending={isSending}
        onAddAssistantMessage={handleAddAssistantMessage}
      />
    </>
  );
}
export default GlobalCopilotShell;
