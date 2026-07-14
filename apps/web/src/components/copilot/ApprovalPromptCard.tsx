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
  let borderColor = 'border-border bg-card';
  let badgeColor = 'text-primary border-primary bg-primary/5';
  let riskLabel = 'REVERSIBLE_ACTION';

  if (isDestructive) {
    borderColor = 'border-red-500/20 bg-red-500/5';
    badgeColor = 'text-red-500 border-red-500/25 bg-red-500/5';
    riskLabel = 'DESTRUCTIVE_ACTION';
  }

  return (
    <div className={`p-4 rounded-none border flex flex-col gap-3 transition-all duration-150 ${borderColor} text-[11px] font-sans`}>
      {/* Risk Header */}
      <div className="flex items-center justify-between border-b border-border/40 pb-2">
        <span className="font-bold tracking-wide uppercase text-[9px] text-muted-foreground font-mono">
          Awaiting Authorization
        </span>
        <span className={`px-2 py-0.5 rounded-none text-[8px] font-extrabold tracking-wider border uppercase font-mono ${badgeColor}`}>
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
          <div className="flex items-center gap-1.5 text-muted-foreground text-[10px] font-mono">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3.5 h-3.5 text-primary">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
            </svg>
            <span>This action is reversible.</span>
          </div>
        )}
      </div>

      {/* Execution Code Preview */}
      <div className="bg-background border border-border/60 p-2.5 font-mono text-[9px] text-muted-foreground whitespace-pre-wrap max-h-24 overflow-y-auto leading-relaxed rounded-none">
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
