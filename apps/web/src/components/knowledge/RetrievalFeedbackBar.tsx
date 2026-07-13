'use client';

import { useState } from 'react';

interface RetrievalFeedbackBarProps {
  traceId: string;
  onSubmitFeedback: (traceId: string, score: number, notes: string) => Promise<boolean>;
}

export function RetrievalFeedbackBar({ traceId, onSubmitFeedback }: RetrievalFeedbackBarProps) {
  const [submitted, setSubmitted] = useState(false);
  const [notes, setNotes] = useState('');

  const sendScore = async (score: number) => {
    const ok = await onSubmitFeedback(traceId, score, notes || 'User response rating feedback');
    if (ok) {
      setSubmitted(true);
    }
  };

  if (submitted) {
    return (
      <div className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 p-2 rounded-lg text-center text-[10px] font-semibold">
        Thank you for your feedback!
      </div>
    );
  }

  return (
    <div className="bg-background border border-border p-3.5 rounded-xl space-y-3 text-xs flex flex-col md:flex-row md:items-center justify-between gap-3">
      <div className="flex-1 space-y-1">
        <span className="text-[9px] text-muted-foreground uppercase font-semibold">Submit Retrieval Feedback</span>
        <input
          type="text"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Any notes (e.g. correct source found)..."
          className="bg-muted/30 border border-border/80 px-2.5 py-1 rounded text-[10px] text-foreground w-full focus:outline-none focus:border-primary/50"
        />
      </div>

      <div className="flex gap-2 justify-end self-end">
        <button
          onClick={() => sendScore(1)}
          className="bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 border border-emerald-500/20 px-3 py-1 rounded text-[10px] font-semibold"
        >
          Helpful
        </button>
        <button
          onClick={() => sendScore(-1)}
          className="bg-rose-500/20 text-rose-400 hover:bg-rose-500/30 border border-rose-500/20 px-3 py-1 rounded text-[10px] font-semibold"
        >
          Unhelpful
        </button>
      </div>
    </div>
  );
}
export default RetrievalFeedbackBar;
