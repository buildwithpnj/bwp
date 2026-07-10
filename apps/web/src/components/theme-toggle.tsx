'use client';

import React, { useEffect, useState } from 'react';
import { useTheme as useNextTheme } from 'next-themes';
import { Sun, Moon } from 'lucide-react';
import { cn } from '@/lib/utils';

export function ThemeToggle({ className, style }: { className?: string; style?: React.CSSProperties }) {
  const { setTheme, resolvedTheme } = useNextTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <button 
        className={cn("inline-flex items-center justify-center rounded-lg text-muted-foreground transition-all h-8 w-8", className)}
        style={style}
        aria-label="Toggle theme"
      >
        <Sun className="h-4 w-4" />
      </button>
    );
  }

  const isDark = resolvedTheme === 'dark';

  return (
    <button
      onClick={() => setTheme(isDark ? 'light' : 'dark')}
      className={cn("inline-flex items-center justify-center rounded-lg text-muted-foreground transition-all h-8 w-8", className)}
      style={style}
      aria-label="Toggle theme"
      id="theme-toggle"
    >
      {isDark ? (
        <Sun className="h-4 w-4 text-[#3B82F6] animate-fade-in" />
      ) : (
        <Moon className="h-4 w-4 text-[#3B82F6] animate-fade-in" />
      )}
    </button>
  );
}
