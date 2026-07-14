import React from 'react';
import { DestructiveActionWarning } from './DestructiveActionWarning';
import { ApprovalDecisionBar } from './ApprovalDecisionBar';

export interface ApprovalRequest {
  id: string;
  action_name: string;
  policy_tier: string;
  risk_level: string;
  human_summary: string;
  execution_preview: string;
  expires_at: string;
}

interface ApprovalPromptCardProps {
  request: ApprovalRequest;
  token: string;
  onDecision: (approved: boolean) => void;
  isProcessing: boolean;
}

export function ApprovalPromptCard({
  request,
  token,
  onDecision,
  isProcessing
}: ApprovalPromptCardProps) {
  const isDestructive = request.policy_tier === 'destructive_confirmed';
  
  // Risk styling
  let borderColor = 'border-indigo-500/30 bg-indigo-500/5';
  let badgeColor = 'text-indigo-400 bg-indigo-400/10 border-indigo-400/20';
  let riskLabel = 'Medium Risk';

  if (isDestructive) {
    borderColor = 'border-rose-500/30 bg-rose-500/5';
    badgeColor = 'text-rose-400 bg-rose-400/10 border-rose-400/20';
    riskLabel = 'High Risk';
  }

  return (
    <div className={`p-4 rounded-xl border flex flex-col gap-3 transition-all duration-300 backdrop-blur-md ${borderColor} text-[11px] font-sans shadow-lg`}>
      {/* Risk Header */}
      <div className="flex items-center justify-between border-b border-white/5 pb-2">
        <span className="font-bold tracking-wide uppercase text-[9px] text-muted-foreground">
          Awaiting Authorization
        </span>
        <span className={`px-2 py-0.5 rounded text-[8px] font-extrabold tracking-wider border uppercase ${badgeColor}`}>
          {riskLabel}
        </span>
      </div>

      {/* Target & Summary */}
      <div className="flex flex-col gap-1.5 py-1">
        <h4 className="text-[12px] font-bold text-foreground leading-snug">
          {request.human_summary}
        </h4>
        
        {isDestructive ? (
          <DestructiveActionWarning actionName={request.action_name} />
        ) : (
          <div className="flex items-center gap-1.5 text-muted-foreground text-[10px]">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3.5 h-3.5 text-emerald-400">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <span>This action is reversible.</span>
          </div>
        )}
      </div>

      {/* Execution Code Preview */}
      <div className="bg-black/40 border border-white/5 rounded-lg p-2.5 font-mono text-[9px] text-muted-foreground whitespace-pre-wrap max-h-24 overflow-y-auto leading-relaxed">
        {request.execution_preview}
      </div>

      {/* Action Bar */}
      <ApprovalDecisionBar 
        approvalId={request.id}
        onDecision={onDecision}
        isProcessing={isProcessing}
      />
    </div>
  );
}
