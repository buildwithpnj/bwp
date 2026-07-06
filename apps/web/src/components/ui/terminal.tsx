import React from 'react';
import { Terminal as TerminalIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface TerminalProps {
  title?: string;
  lines: string[];
  className?: string;
  showPrompt?: boolean;
}

export function Terminal({ title = 'pnj-telemetry', lines, className, showPrompt = true }: TerminalProps) {
  return (
    <div className={cn("w-full rounded-2xl border border-border bg-card shadow-2xl overflow-hidden font-mono text-xs select-none text-left", className)}>
      
      {/* Terminal Window Header Bar */}
      <div className="flex items-center justify-between px-4 py-3 bg-background/60 border-b border-border">
        <div className="flex items-center gap-2">
          {/* Simulated Mac OS window controls */}
          <span className="w-3 h-3 rounded-full bg-[#FF5F56] border border-[#E0443E]/20" />
          <span className="w-3 h-3 rounded-full bg-[#FFBD2E] border border-[#DEA123]/20" />
          <span className="w-3 h-3 rounded-full bg-[#27C93F] border border-[#1AAB29]/20" />
        </div>
        
        <span className="text-[10px] text-muted-foreground font-medium flex items-center gap-1.5 uppercase tracking-wider font-sans select-none">
          <TerminalIcon className="h-3 w-3 text-primary" /> {title}
        </span>
        
        <div className="w-12" /> {/* Spacer */}
      </div>

      {/* Terminal Content Screen */}
      <div className="p-5 flex flex-col gap-2 max-h-[300px] overflow-y-auto bg-card text-muted-foreground">
        
        {/* Output lines */}
        {lines.map((line, idx) => (
          <div key={idx} className="flex items-start gap-2 leading-relaxed">
            {line.startsWith('pnj@') ? (
              <span className="text-primary shrink-0">pnj@studio:~$</span>
            ) : line.startsWith('>') ? (
              <span className="text-primary shrink-0">&gt;</span>
            ) : null}
            <span className={cn(
              "whitespace-pre-wrap select-text",
              line.includes('SUCCESS') || line.includes('online') ? 'text-positive' :
              line.includes('ERROR') || line.includes('failed') ? 'text-red-500' :
              line.startsWith('pnj@') ? 'text-foreground' : ''
            )}>
              {line.startsWith('pnj@') ? line.replace('pnj@studio:~$ ', '') : line.startsWith('>') ? line.substring(1) : line}
            </span>
          </div>
        ))}

        {/* Bypassed active prompt cursor */}
        {showPrompt && (
          <div className="flex items-center gap-2 mt-1">
            <span className="text-primary">pnj@studio:~$</span>
            <span className="w-2 h-4 bg-primary animate-pulse" />
          </div>
        )}

      </div>

    </div>
  );
}
