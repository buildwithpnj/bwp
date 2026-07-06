'use client';

import React, { useState } from 'react';
import { Twitter, Linkedin, Link, Check } from 'lucide-react';

interface ArticleShareProps {
  url: string;
  title: string;
}

export function ArticleShare({ url, title }: ArticleShareProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const shareText = encodeURIComponent(title);
  const shareUrl = encodeURIComponent(url);

  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-muted-foreground font-medium mr-2 font-mono uppercase">{"// SHARE:"}</span>
      
      <a
        href={`https://twitter.com/intent/tweet?text=${shareText}&url=${shareUrl}`}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center justify-center h-10 w-10 rounded-xl border border-border bg-card text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all active:scale-[0.98]"
        title="Share on Twitter"
      >
        <Twitter className="h-4 w-4" />
      </a>
      
      <a
        href={`https://www.linkedin.com/sharing/share-offsite/?url=${shareUrl}`}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center justify-center h-10 w-10 rounded-xl border border-border bg-card text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all active:scale-[0.98]"
        title="Share on LinkedIn"
      >
        <Linkedin className="h-4 w-4" />
      </a>

      <button
        onClick={handleCopy}
        className="flex items-center justify-center h-10 w-10 rounded-xl border border-border bg-card text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all active:scale-[0.98]"
        title="Copy Link"
      >
        {copied ? <Check className="h-4 w-4 text-positive" /> : <Link className="h-4 w-4" />}
      </button>
    </div>
  );
}
