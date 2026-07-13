'use client';

import { useState } from 'react';

interface CopilotConfigPanelProps {
  onUpdatePolicy: (fieldName: string, value: string) => void;
}

export function CopilotConfigPanel({ onUpdatePolicy }: CopilotConfigPanelProps) {
  const [quotaVal, setQuotaVal] = useState('50000000');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdatePolicy('modality_limit', quotaVal);
  };

  return (
    <div className="bg-muted/30 border border-border p-3.5 rounded-xl space-y-3">
      <h4 className="font-semibold text-foreground text-xs">Copilot & Quota Limits</h4>
      
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="flex flex-col gap-1.5 text-xs">
          <label className="text-muted-foreground font-medium">Daily Ingestion Byte Limit (Bytes)</label>
          <input
            type="text"
            value={quotaVal}
            onChange={e => setQuotaVal(e.target.value)}
            className="bg-background border border-border px-3 py-1.5 rounded-md text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
        <button
          type="submit"
          className="bg-primary text-primary-foreground px-3 py-1.5 rounded-md text-xs font-semibold hover:bg-primary/95 transition-all w-full"
        >
          Save Quota Limit
        </button>
      </form>
    </div>
  );
}
