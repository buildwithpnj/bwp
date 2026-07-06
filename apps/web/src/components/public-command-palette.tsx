'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Search, Command, ArrowRight, X } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PaletteItem {
  title: string;
  subtitle?: string;
  category: 'Pages' | 'Quick Actions' | 'Content';
  shortcut?: string;
  action: () => void;
}

export function PublicCommandPalette() {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Global keydown listeners for Cmd+K and G chords
  useEffect(() => {
    let lastKey = '';
    let timeoutId: NodeJS.Timeout;

    const handleKeyDown = (e: KeyboardEvent) => {
      const activeEl = document.activeElement;
      const isInput = 
        activeEl?.tagName === 'INPUT' || 
        activeEl?.tagName === 'TEXTAREA' || 
        (activeEl as HTMLElement)?.isContentEditable;

      const key = e.key.toLowerCase();

      // Ignore shortcuts if writing in an input, unless it is our command input
      if (isInput && activeEl?.id !== 'command-palette-input') {
        return;
      }

      // Cmd+K or Ctrl+K trigger toggle
      if ((e.metaKey || e.ctrlKey) && key === 'k') {
        e.preventDefault();
        setOpen((prev) => !prev);
        return;
      }

      // Escape close
      if (e.key === 'Escape') {
        setOpen(false);
        return;
      }

      // Chord G sequences
      if (lastKey === 'g') {
        if (key === 'h') { e.preventDefault(); router.push('/'); setOpen(false); }
        else if (key === 'p') { e.preventDefault(); router.push('/projects'); setOpen(false); }
        else if (key === 'l') { e.preventDefault(); router.push('/labs'); setOpen(false); }
        else if (key === 'j') { e.preventDefault(); router.push('/journal'); setOpen(false); }
        else if (key === 'm') { e.preventDefault(); router.push('/mission-control'); setOpen(false); }
        else if (key === 'a') { e.preventDefault(); router.push('/about'); setOpen(false); }
        else if (key === 'c') { e.preventDefault(); router.push('/contact'); setOpen(false); }
        else if (key === 'd') { e.preventDefault(); router.push('/dashboard'); setOpen(false); }
        lastKey = '';
        clearTimeout(timeoutId);
      } else if (key === 'g' && !isInput) {
        lastKey = 'g';
        timeoutId = setTimeout(() => {
          lastKey = '';
        }, 1000);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      clearTimeout(timeoutId);
    };
  }, [router]);

  // Focus input when opened
  useEffect(() => {
    if (open) {
      setTimeout(() => inputRef.current?.focus(), 50);
      setSelectedIndex(0);
      setSearchQuery('');
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  // Static options list
  const items: PaletteItem[] = [
    { title: 'Home', category: 'Pages', shortcut: 'G H', action: () => router.push('/') },
    { title: 'Projects Showcase', category: 'Pages', shortcut: 'G P', action: () => router.push('/projects') },
    { title: 'Labs Experiments', category: 'Pages', shortcut: 'G L', action: () => router.push('/labs') },
    { title: 'Engineering Journal', category: 'Pages', shortcut: 'G J', action: () => router.push('/journal') },
    { title: 'Mission Control Telemetry', category: 'Pages', shortcut: 'G M', action: () => router.push('/mission-control') },
    { title: 'About Prakash', category: 'Pages', shortcut: 'G A', action: () => router.push('/about') },
    { title: 'Contact / Collaboration', category: 'Pages', shortcut: 'G C', action: () => router.push('/contact') },
    { title: 'Personal OS Dashboard', category: 'Pages', shortcut: 'G D', action: () => router.push('/dashboard') },
    { title: 'Personal OS Case Study', subtitle: 'Detailed project writeup', category: 'Content', action: () => router.push('/projects/personal-os') },
    { title: 'Building a Personal OS from Scratch', subtitle: 'Journal post', category: 'Content', action: () => router.push('/journal/building-personal-os-from-scratch') },
    { title: 'Multi-Agent Code Reviewer', subtitle: 'Lab experiment writeup', category: 'Content', action: () => router.push('/labs/multi-agent-code-reviewer') },
    { title: 'Follow on Twitter / X', subtitle: '@buildwithpnj', category: 'Quick Actions', action: () => window.open('https://twitter.com/buildwithpnj', '_blank') },
    { title: 'View GitHub Profile', subtitle: '@buildwithpnj', category: 'Quick Actions', action: () => window.open('https://github.com/buildwithpnj', '_blank') },
  ];

  // Filter items by search
  const filteredItems = items.filter(item => 
    item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (item.subtitle && item.subtitle.toLowerCase().includes(searchQuery.toLowerCase())) ||
    item.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Keyboard navigation inside list
  const handleListKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev + 1) % filteredItems.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev - 1 + filteredItems.length) % filteredItems.length);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filteredItems[selectedIndex]) {
        filteredItems[selectedIndex].action();
        setOpen(false);
      }
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4">
      {/* Backdrop */}
      <div 
        onClick={() => setOpen(false)}
        className="fixed inset-0 bg-background/80 backdrop-blur-sm transition-opacity duration-300" 
      />

      {/* Palette Container */}
      <div 
        ref={containerRef}
        onKeyDown={handleListKeyDown}
        className="relative w-full max-w-xl bg-card border border-border rounded-2xl shadow-2xl overflow-hidden z-10 animate-in text-left"
      >
        {/* Input area */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border">
          <Search className="h-4 w-4 text-muted-foreground" />
          <input
            ref={inputRef}
            id="command-palette-input"
            type="text"
            placeholder="Type a command or search..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setSelectedIndex(0);
            }}
            className="flex-1 bg-transparent border-0 outline-none text-sm text-foreground placeholder:text-muted-foreground h-8"
          />
          <button 
            onClick={() => setOpen(false)}
            className="p-1 rounded-md text-muted-foreground hover:bg-accent hover:text-foreground"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-[360px] overflow-y-auto p-2">
          {filteredItems.length === 0 ? (
            <div className="py-8 text-center text-sm text-muted-foreground">
              No results found for &ldquo;{searchQuery}&rdquo;
            </div>
          ) : (
            <div>
              {/* Group items by category */}
              {['Pages', 'Content', 'Quick Actions'].map((cat) => {
                const catItems = filteredItems.filter(item => item.category === cat);
                if (catItems.length === 0) return null;

                return (
                  <div key={cat} className="mb-3 last:mb-0">
                    <div className="px-3 py-1 font-pixel text-[10px] text-muted-foreground tracking-wider uppercase">
                      {"//"} {cat}
                    </div>
                    <div className="mt-1 flex flex-col gap-0.5">
                      {catItems.map((item) => {
                        // Find global index in filteredItems
                        const globalIndex = filteredItems.indexOf(item);
                        const isSelected = globalIndex === selectedIndex;

                        return (
                          <button
                            key={item.title}
                            onClick={() => {
                              item.action();
                              setOpen(false);
                            }}
                            className={cn(
                              "w-full text-left flex items-center justify-between px-3 py-2.5 rounded-xl transition-all duration-100",
                              isSelected 
                                ? "bg-accent text-foreground border-l-2 border-primary pl-2.5" 
                                : "text-muted-foreground hover:bg-accent hover:text-foreground"
                            )}
                          >
                            <div className="flex flex-col gap-0.5">
                              <span className="text-sm font-medium">{item.title}</span>
                              {item.subtitle && (
                                <span className="text-xs text-muted-foreground">{item.subtitle}</span>
                              )}
                            </div>
                            
                            <div className="flex items-center gap-2">
                              {item.shortcut ? (
                                <span className="font-mono text-[10px] text-muted-foreground bg-secondary px-1.5 py-0.5 rounded border border-border">
                                  {item.shortcut}
                                </span>
                              ) : isSelected ? (
                                <ArrowRight className="h-3 w-3 text-primary" />
                              ) : null}
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer info */}
        <div className="px-4 py-2 bg-background/50 border-t border-border flex justify-between items-center text-[10px] text-muted-foreground">
          <div className="flex items-center gap-3">
            <span>↑↓ to navigate</span>
            <span>↵ to select</span>
            <span>esc to close</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Command className="h-2.5 w-2.5" />
            <span>K to toggle</span>
          </div>
        </div>
      </div>
    </div>
  );
}
