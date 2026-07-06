'use client';

import React, { useState } from 'react';
import { Copy, Check, FileCode } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CodeBlockProps {
  filename?: string;
  language?: string;
  code: string;
  className?: string;
}

export function CodeBlock({ filename, language = 'typescript', code, className }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={cn("w-full rounded-2xl border border-border bg-card overflow-hidden text-left", className)}>
      
      {/* Code Header bar */}
      <div className="flex items-center justify-between px-4 py-3 bg-background/60 border-b border-border text-xs text-muted-foreground font-mono">
        <div className="flex items-center gap-2">
          <FileCode className="h-4 w-4 text-primary" />
          <span className="text-foreground font-semibold">{filename || `file.${language === 'javascript' ? 'js' : language === 'python' ? 'py' : 'ts'}`}</span>
          {language && (
            <span className="px-1.5 py-0.5 rounded text-[10px] uppercase font-bold bg-secondary font-sans border border-border">
              {language}
            </span>
          )}
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center gap-1.5 h-8 px-3 rounded-lg border border-border bg-card hover:bg-accent hover:text-foreground transition-all active:scale-[0.98]"
        >
          {copied ? (
            <>
              <Check className="h-3.5 w-3.5 text-positive" />
              <span className="text-positive text-[10px]">Copied</span>
            </>
          ) : (
            <>
              <Copy className="h-3.5 w-3.5" />
              <span className="text-[10px]">Copy</span>
            </>
          )}
        </button>
      </div>

      {/* Code Area */}
      <pre className="p-5 font-mono text-xs overflow-x-auto text-muted-foreground leading-relaxed bg-card select-text">
        <code className={cn(`language-${language}`)}>
          {code}
        </code>
      </pre>

    </div>
  );
}
