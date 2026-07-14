import React from 'react';

interface ApprovalDecisionBarProps {
  approvalId: string;
  onDecision: (approved: boolean) => void;
  isProcessing: boolean;
}

export function ApprovalDecisionBar({
  approvalId,
  onDecision,
  isProcessing
}: ApprovalDecisionBarProps) {
  return (
    <div className="flex gap-2 w-full mt-1">
      <button
        onClick={() => onDecision(false)}
        disabled={isProcessing}
        className="flex-1 px-3 py-1.5 rounded-lg border border-white/10 hover:border-white/20 bg-white/5 hover:bg-white/10 text-white font-semibold transition-all text-[11px] disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Deny
      </button>
      <button
        onClick={() => onDecision(true)}
        disabled={isProcessing}
        className="flex-1 px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-emerald-950 font-bold transition-all text-[11px] flex items-center justify-center gap-1.5 shadow-md shadow-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isProcessing ? (
          <>
            <svg className="animate-spin h-3 w-3 text-emerald-950" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>Applying...</span>
          </>
        ) : (
          <span>Allow</span>
        )}
      </button>
    </div>
  );
}
