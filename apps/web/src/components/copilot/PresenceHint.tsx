'use client';

interface PresenceHintProps {
  intent: string;
}

export function PresenceHint({ intent }: PresenceHintProps) {
  if (intent !== 'stuck') return null;
  return (
    <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-[10px] px-2 py-1 rounded flex items-center gap-1.5 animate-pulse">
      <span className="h-1.5 w-1.5 rounded-full bg-red-500" />
      <span>Anomalies detected. Request recovery guidance below.</span>
    </div>
  );
}
