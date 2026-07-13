'use client';

import { cn } from '@/lib/utils';

interface VoiceOrbProps {
  isListening: boolean;
  isThinking: boolean;
  onClick: () => void;
}

export function VoiceOrb({ isListening, isThinking, onClick }: VoiceOrbProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'relative flex h-12 w-12 items-center justify-center rounded-full transition-all duration-300',
        isListening
          ? 'bg-red-500/20 text-red-400 border border-red-500/50 scale-105'
          : isThinking
          ? 'bg-primary/20 text-primary border border-primary/50 animate-pulse'
          : 'bg-muted/30 text-muted-foreground border border-muted hover:bg-muted/50 hover:text-foreground'
      )}
    >
      {/* Orb Pulsing rings */}
      {isListening && (
        <span className="absolute inset-0 rounded-full border border-red-500 animate-ping opacity-75" />
      )}
      
      <svg
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        strokeWidth={1.5}
        stroke="currentColor"
        className="w-5 h-5"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z"
        />
      </svg>
    </button>
  );
}
