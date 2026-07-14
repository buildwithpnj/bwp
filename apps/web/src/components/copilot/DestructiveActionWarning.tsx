import React from 'react';

interface DestructiveActionWarningProps {
  actionName: string;
}

export function DestructiveActionWarning({ actionName }: DestructiveActionWarningProps) {
  return (
    <div className="flex gap-2 p-2.5 rounded-lg border border-red-500/20 bg-red-500/10 text-red-200 text-[10px] font-sans items-start">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 text-red-400 shrink-0 mt-0.5 animate-pulse">
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
      </svg>
      <div className="flex flex-col gap-0.5">
        <span className="font-bold text-red-300">Irreversible Action</span>
        <p className="opacity-90 leading-relaxed">
          This action may not be reversible. Confirming will modify or purge this record.
        </p>
      </div>
    </div>
  );
}
