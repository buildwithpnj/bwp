import React from 'react';

export default function PublicLoadingPage() {
  return (
    <div className="min-h-[60vh] w-full flex flex-col justify-center items-center gap-6">
      
      {/* Outer pulsing ring */}
      <div className="relative flex items-center justify-center">
        {/* Core Pulsing square */}
        <div className="w-10 h-10 rounded-lg border border-primary/20 bg-card flex items-center justify-center font-pixel text-primary text-lg select-none animate-pulse shadow-sm shadow-primary/20">
          P
        </div>
        {/* Ambient ring overlay */}
        <div className="absolute inset-0 rounded-lg border border-primary/30 scale-125 animate-ping opacity-60" style={{ animationDuration: '2.5s' }} />
      </div>

      {/* Loading telemetry text */}
      <div className="flex flex-col gap-1 text-center">
        <span className="font-pixel text-[10px] tracking-[0.2em] text-primary uppercase animate-pulse">
          {"// COMPILING VIEW"}
        </span>
        <span className="font-mono text-[9px] text-muted-foreground">
          syncing telemetry streams...
        </span>
      </div>

    </div>
  );
}
