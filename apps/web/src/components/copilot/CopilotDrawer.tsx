'use client';

import { useState } from 'react';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { CopilotMessage } from '@/hooks/useCopilotSession';
import { VoiceOrb } from './VoiceOrb';
import { useVoiceSession } from '@/hooks/useVoiceSession';
import { useCopilotPresence } from '@/hooks/useCopilotPresence';
import { PresenceHint } from './PresenceHint';
import { SuggestedActionsStrip } from './SuggestedActionsStrip';
import { ContextSnapshotCard } from './ContextSnapshotCard';
import { SmartEntryPrompt } from './SmartEntryPrompt';
import { ActionResultCard, isStructuredResponse } from './ActionResultCard';
import { ApprovalPromptCard } from './ApprovalPromptCard';
import { useApprovalActions } from '@/hooks/useApprovalActions';

interface CopilotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  messages: CopilotMessage[];
  sendMessage: (text: string) => void;
  isSending: boolean;
  onAddAssistantMessage: (userMsg: CopilotMessage, assistantMsg: CopilotMessage) => void;
  onUpdateMessage: (idx: number, updated: CopilotMessage) => void;
}

export function CopilotDrawer({
  isOpen,
  onClose,
  messages,
  sendMessage,
  isSending,
  onAddAssistantMessage,
  onUpdateMessage
}: CopilotDrawerProps) {
  const pathname = usePathname();
  const [inputVal, setInputVal] = useState('');
  
  const { decideApproval, isProcessing } = useApprovalActions();
  const [processingIdx, setProcessingIdx] = useState<number | null>(null);

  const { isListening, isThinking, startListening, stopListening } = useVoiceSession(
    (userMsg, assistantMsg) => {
      onAddAssistantMessage(userMsg, assistantMsg);
    }
  );

  const { presence, suggestions } = useCopilotPresence();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputVal.trim()) return;
    sendMessage(inputVal);
    setInputVal('');
  };

  const handleOrbClick = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening();
    }
  };

  const handleDecision = async (idx: number, approve: boolean) => {
    const msg = messages[idx];
    if (!msg.approval_request || !msg.token) return;

    setProcessingIdx(idx);
    const res = await decideApproval(msg.approval_request.id, approve, msg.token);
    setProcessingIdx(null);

    if (res.success) {
      onUpdateMessage(idx, {
        ...msg,
        approval_decided: true,
        approval_decision_status: approve ? 'success' : 'denied',
        content: `Status: ${approve ? 'Success' : 'Denied'}\nAction: ${msg.suggested_action?.action_name || 'Action'}\nResult: ${approve ? 'Action approved and executed successfully.' : 'Action denied. No changes were made.'}\nScope: workspace`
      });
    } else {
      onUpdateMessage(idx, {
        ...msg,
        approval_decided: true,
        approval_decision_status: 'failed',
        content: `Status: Fail\nAction: ${msg.suggested_action?.action_name || 'Action'}\nResult: ${res.error || 'Verification failed.'}\nScope: workspace`
      });
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-80 bg-background/95 border-l border-border shadow-2xl backdrop-blur-md flex flex-col transition-all duration-300">
      {/* Header */}
      <div className="p-4 border-b border-border flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-foreground text-sm flex items-center gap-1.5">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              Warborn Copilot
            </h3>
            <p className="text-[10px] text-muted-foreground truncate max-w-[200px]">
              Route: {pathname}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-muted-foreground hover:text-foreground p-1 rounded-md hover:bg-muted"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-4 h-4"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <PresenceHint intent={presence.intent} />
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3">
        {messages.length === 0 && (
          <div className="flex flex-col gap-3 py-4">
            <ContextSnapshotCard intent={presence.intent} />
            <SmartEntryPrompt
              intent={presence.intent}
              onAccept={() => sendMessage("Help me resolve stalled steps or failed workflow runs.")}
            />
          </div>
        )}
        {messages.map((msg, idx) => {
          const showApprovalCard = msg.role === 'assistant' && msg.approval_required && !msg.approval_decided;
          
          return (
            <div
              key={idx}
              className={cn(
                'flex flex-col gap-1 max-w-[85%] rounded-lg text-xs',
                showApprovalCard 
                  ? 'w-full max-w-full' 
                  : msg.role === 'user'
                    ? 'bg-primary text-primary-foreground ml-auto p-2.5'
                    : 'bg-muted text-foreground p-2.5'
              )}
            >
              {showApprovalCard ? (
                <ApprovalPromptCard
                  request={msg.approval_request!}
                  token={msg.token!}
                  isProcessing={processingIdx === idx}
                  onDecision={(approved) => handleDecision(idx, approved)}
                />
              ) : msg.role === 'assistant' && isStructuredResponse(msg.content) ? (
                <ActionResultCard content={msg.content} />
              ) : (
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              )}
              {msg.suggested_action && !showApprovalCard && !msg.approval_decided && (
                <div className="mt-2 pt-2 border-t border-border/20 text-[10px] opacity-90 font-medium">
                  Action: {msg.suggested_action.action_name}
                </div>
              )}
            </div>
          );
        })}
        {isSending && (
          <div className="bg-muted text-muted-foreground rounded-lg p-2.5 text-xs max-w-[85%] animate-pulse">
            Thinking...
          </div>
        )}
        {isThinking && (
          <div className="bg-muted text-muted-foreground rounded-lg p-2.5 text-xs max-w-[85%] animate-pulse">
            Transcribing voice...
          </div>
        )}
      </div>

      {/* Footer Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-border space-y-3">
        <SuggestedActionsStrip
          suggestions={suggestions}
          onSelectSuggestion={(text) => sendMessage(text)}
        />
        <div className="flex gap-2">
          <input
            type="text"
            value={inputVal}
            onChange={e => setInputVal(e.target.value)}
            placeholder={isListening ? 'Listening...' : 'Ask copilot...'}
            disabled={isListening}
            className="flex-1 bg-muted/50 border border-border rounded-md px-2.5 py-1.5 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
          />
          <button
            type="submit"
            disabled={isSending || isListening}
            className="bg-primary text-primary-foreground px-3 py-1.5 rounded-md text-xs font-semibold hover:bg-primary/95 disabled:opacity-50"
          >
            Send
          </button>
        </div>
        
        <div className="flex items-center justify-center pt-2">
          <VoiceOrb
            isListening={isListening}
            isThinking={isThinking}
            onClick={handleOrbClick}
          />
        </div>
      </form>
    </div>
  );
}
