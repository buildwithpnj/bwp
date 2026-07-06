'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { AlertOctagon, RefreshCw, Home } from 'lucide-react';

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function PublicErrorPage({ error, reset }: ErrorProps) {
  useEffect(() => {
    // Log error to console/telemetry Sentry service
    console.error('Captured public route error:', error);
  }, [error]);

  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="w-full max-w-md flex flex-col gap-6 p-6 sm:p-8 rounded-2xl border border-border bg-card relative overflow-hidden card-glow-hover">
        
        {/* Error icon overlay */}
        <div className="mx-auto h-12 w-12 rounded-full bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-500">
          <AlertOctagon className="h-6 w-6" />
        </div>

        {/* Title */}
        <div className="flex flex-col gap-1.5 text-center">
          <div className="font-pixel text-[11px] text-red-500 tracking-wider uppercase">{"// SYSTEMS ERROR"}</div>
          <h2 className="text-xl font-pixel text-foreground">Exception Detected</h2>
          <p className="text-xs text-muted-foreground leading-relaxed mt-1">
            An unexpected error occurred during client-side hydration or page data fetching.
          </p>
        </div>

        {/* Diagnostic info block */}
        <div className="p-4 rounded-xl border border-border bg-background text-left font-mono text-[10px] text-muted-foreground overflow-x-auto flex flex-col gap-1.5 select-text">
          <div className="text-foreground font-semibold">DIAGNOSTIC LOG:</div>
          <div className="truncate">MSG: {error.message || 'Unknown Exception'}</div>
          {error.digest && <div>HASH: {error.digest}</div>}
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 mt-2">
          <button
            onClick={() => reset()}
            className="flex-1 inline-flex items-center justify-center gap-2 h-11 px-4 rounded-xl font-semibold bg-primary text-primary-foreground hover:opacity-90 active:scale-[0.98] transition-all"
          >
            <RefreshCw className="h-4 w-4" /> Reset System
          </button>
          
          <Link
            href="/"
            className="flex-1 inline-flex items-center justify-center gap-2 h-11 px-4 rounded-xl font-semibold border border-border bg-background text-muted-foreground hover:text-foreground transition-all active:scale-[0.98]"
          >
            <Home className="h-4 w-4" /> Go Home
          </Link>
        </div>

      </div>
    </div>
  );
}
