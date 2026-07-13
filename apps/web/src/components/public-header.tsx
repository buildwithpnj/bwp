'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X, Command, Github } from 'lucide-react';
import { cn } from '@/lib/utils';
import { ThemeToggle } from '@/components/theme-toggle';

interface NavLink {
  label: string;
  href: string;
}

const navLinks: NavLink[] = [
  { label: 'Projects', href: '/projects' },
  { label: 'Labs', href: '/labs' },
  { label: 'Journal', href: '/journal' },
  { label: 'About', href: '/about' },
  { label: 'Contact', href: '/contact' },
  { label: 'Mission Control', href: '/mission-control' },
];

export function PublicHeader() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // 1. Listen to scroll events to toggle floating island styling
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 15) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // 2. Lock body scroll when mobile menu overlay is active
  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [mobileMenuOpen]);

  return (
    <header className="sticky top-0 z-50 w-full transition-all duration-300 py-3 sm:py-4 px-4 sm:px-6 lg:px-8">
      {/* Floating Island Navigation bar container */}
      <div 
        className={cn(
          "max-w-7xl mx-auto rounded-2xl border transition-all duration-300 flex items-center justify-between relative overflow-hidden",
          scrolled 
            ? "h-12 sm:h-14 px-4 sm:px-6 dark:bg-gradient-to-r dark:from-[#0A0F1D]/80 dark:to-[#0A0F1D]/60 bg-gradient-to-r from-white/90 to-white/75 backdrop-blur-md" 
            : "h-14 sm:h-16 px-5 sm:px-8 dark:bg-gradient-to-r dark:from-[#0A0F1D]/35 dark:to-transparent bg-gradient-to-r from-white/35 to-transparent backdrop-blur-[4px]"
        )}
        style={{
          borderColor: scrolled 
            ? 'var(--hero-active-color-glow, rgba(229, 72, 77, 0.35))' 
            : 'var(--hero-active-color-glow, rgba(229, 72, 77, 0.15))',
          boxShadow: scrolled
            ? '0 12px 40px rgba(0, 0, 0, 0.15), 0 0 15px var(--hero-active-color-glow, rgba(229, 72, 77, 0.08))'
            : 'none'
        }}
      >
        
        {/* Accent background glass tint overlay (dynamic synced color) */}
        <div 
          className="absolute inset-0 pointer-events-none z-0 transition-colors duration-300"
          style={{ backgroundColor: 'var(--hero-active-color-glow, hsla(358, 76%, 59%, 0.08))' }}
        />

        {/* Blueprint pattern & trace sweep overlay */}
        <div className="absolute inset-0 pointer-events-none rounded-2xl overflow-hidden z-0">
          {/* Subtle blueprint grid dots backdrop (Dark Mode) */}
          <div className="hidden dark:block absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.025)_1px,transparent_1px)] bg-[size:16px_16px] opacity-40" />
          {/* Subtle blueprint grid dots backdrop (Light Mode) */}
          <div className="block dark:hidden absolute inset-0 bg-[radial-gradient(rgba(0,0,0,0.04)_1px,transparent_1px)] bg-[size:16px_16px] opacity-30" />
          
          {/* Dynamic border pcb traces (Electric Blue) */}
          <div className="absolute top-0 left-0 w-[140px] h-[1.2px] bg-gradient-to-r from-transparent via-[#3B82F6]/50 to-transparent animate-pcb-trace-top" />
          <div className="absolute bottom-0 left-0 w-[140px] h-[1.2px] bg-gradient-to-r from-transparent via-[#3B82F6]/50 to-transparent animate-pcb-trace-bottom" />
        </div>

        {/* Brand / Logo */}
        <div className="flex items-center gap-2 relative z-10">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="relative">
              <span 
                className="font-pixel text-xl sm:text-2xl tracking-widest group-hover:text-black dark:group-hover:text-white transition-colors duration-200"
                style={{ color: 'var(--hero-active-color, #E5484D)' }}
              >
                PNJ
              </span>
              <span className="absolute -top-1 -right-2 text-[7px] font-mono text-emerald-400 opacity-60 group-hover:opacity-100 transition-opacity">v0.45</span>
            </div>
            <span className="hidden sm:inline font-mono text-[9px] text-muted-foreground mt-1.5 tracking-wider uppercase opacity-60 group-hover:opacity-100 transition-opacity">
              {"// AI_LABS"}
            </span>
          </Link>

          {/* Pulse network status */}
          <span className="hidden lg:inline-flex items-center gap-1.5 font-mono text-[8px] text-muted-foreground/80 px-2 py-0.5 rounded border border-border/30 dark:bg-secondary/30 bg-secondary/70 ml-4 uppercase tracking-widest">
            <span className="h-1 w-1 rounded-full bg-emerald-500 animate-pulse" />
            SYSTEM ONLINE
          </span>
        </div>

        {/* Desktop Nav Links (High performance CSS background hover pills) */}
        <nav className="hidden md:flex items-center gap-1.5 p-1 rounded-full border border-transparent z-10 transition-all duration-300 bg-black/5 dark:bg-white/5">
          {navLinks.map((link) => {
            const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  'text-[10px] font-mono font-bold tracking-wider uppercase px-3.5 py-1.5 rounded-full transition-all duration-[250ms] border relative',
                  isActive 
                    ? 'dark:shadow-[0_0_12px_rgba(229,72,77,0.15)] shadow-[0_0_8px_rgba(229,72,77,0.06)] border-t-white/10' 
                    : 'text-muted-foreground hover:text-black dark:hover:text-white border-transparent hover:bg-black/5 dark:hover:bg-white/5 hover:border-black/5 dark:hover:border-white/10 hover:translate-y-[-1px] nav-hover-sweep'
                )}
                style={isActive ? { 
                  color: 'var(--hero-active-color, #E5484D)',
                  backgroundColor: 'var(--hero-active-color-glow, rgba(229, 72, 77, 0.12))',
                  borderColor: 'var(--hero-active-color-glow, rgba(229, 72, 77, 0.25))'
                } : undefined}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* System Toolbar Options (Search trigger, Github logo, ThemeToggle) */}
        <div className="hidden md:flex items-center gap-2 relative z-10">
          <button
            onClick={() => {
              const event = new KeyboardEvent('keydown', { key: 'k', metaKey: true });
              window.dispatchEvent(event);
            }}
            className="btn-engineering flex items-center gap-2 h-8 px-2.5 text-[10px] font-mono rounded-lg border border-transparent bg-black/5 dark:bg-white/5 text-muted-foreground"
          >
            <Command className="h-2.5 w-2.5" />
            <span>SEARCH</span>
            <kbd className="text-[8px] bg-background/80 px-1 py-0.5 rounded border border-border/40 font-sans">
              ⌘K
            </kbd>
          </button>
          
          <a
            href="https://github.com/buildwithpnj"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-engineering flex items-center justify-center h-8 w-8 rounded-lg border border-transparent bg-black/5 dark:bg-white/5 text-muted-foreground"
          >
            <Github className="h-3.5 w-3.5" />
          </a>

          <ThemeToggle className="btn-engineering border border-transparent bg-black/5 dark:bg-white/5" />
        </div>

        {/* Mobile Hamburger toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden flex items-center justify-center p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-accent transition-all"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Menu Fullscreen Glass Overlay */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 top-16 z-30 bg-background/95 backdrop-blur-md flex flex-col justify-between p-6 animate-fade-in border-t border-border/20">
          <nav className="flex flex-col gap-2">
            <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest pb-2 mb-2 border-b border-border/20">
              Navigation
            </div>
            {navLinks.map((link) => {
              const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    'text-base font-mono font-bold py-2 px-3 rounded-lg border transition-all duration-[250ms]',
                    isActive 
                      ? 'text-[#E5484D] bg-[#E5484D]/10 border-[#E5484D]/30 shadow-[0_0_12px_rgba(229,72,77,0.1)]' 
                      : 'text-muted-foreground hover:text-white border-transparent hover:bg-white/5'
                  )}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  setTimeout(() => {
                    const event = new KeyboardEvent('keydown', { key: 'k', metaKey: true });
                    window.dispatchEvent(event);
                  }, 200);
                }}
                className="btn-engineering flex flex-1 items-center justify-center gap-2 h-10 rounded-lg border border-transparent bg-black/5 dark:bg-white/5 text-muted-foreground text-xs font-mono font-bold"
              >
                <Command className="h-3.5 w-3.5" />
                <span>SEARCH CONSOLE</span>
              </button>
              <ThemeToggle className="btn-engineering shrink-0 h-10 w-10 border border-transparent bg-black/5 dark:bg-white/5 flex items-center justify-center" />
            </div>
            <div className="flex justify-center gap-6 py-2 border-t border-border/20 pt-4 text-xs font-mono">
              <a href="https://github.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground">GitHub</a>
              <a href="https://twitter.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground">Twitter</a>
              <a href="https://linkedin.com/in/pnj" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground">LinkedIn</a>
            </div>
            <div className="text-center text-[10px] font-mono text-muted-foreground">
              © 2026 BuildWithPNJ. All rights reserved.
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
