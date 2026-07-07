'use client';

import React, { useState } from 'react';
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

  // Lock body scroll when mobile menu is open
  React.useEffect(() => {
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
    <header className="sticky top-0 z-40 w-full border-b border-border/40 bg-background/80 backdrop-blur-md transition-all duration-200">
      <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <span className="font-pixel text-2xl tracking-widest text-primary group-hover:text-foreground transition-colors duration-200">
            PNJ
          </span>
          <span className="hidden sm:inline font-pixel text-xs text-muted-foreground mt-1 tracking-wider uppercase opacity-80 group-hover:opacity-100 transition-opacity">
            {"// AI LABS"}
          </span>
        </Link>

        {/* Desktop Nav Links */}
        <nav className="hidden md:flex items-center gap-6 lg:gap-8">
          {navLinks.map((link) => {
            const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  'text-sm font-medium transition-colors duration-200 relative py-1.5',
                  isActive 
                    ? 'text-foreground' 
                    : 'text-muted-foreground hover:text-foreground'
                )}
              >
                {link.label}
                {isActive && (
                  <span className="absolute bottom-0 left-0 w-full h-[2px] bg-primary rounded-full" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Command Palette trigger / GitHub link / Theme Toggle */}
        <div className="hidden md:flex items-center gap-3">
          <button
            onClick={() => {
              const event = new KeyboardEvent('keydown', { key: 'k', metaKey: true });
              window.dispatchEvent(event);
            }}
            className="flex items-center gap-2 h-9 px-3 text-xs rounded-xl border border-border bg-secondary hover:bg-accent text-muted-foreground transition-all hover:text-foreground hover:border-primary/30"
          >
            <Command className="h-3 w-3" />
            <span>Search</span>
            <kbd className="kbd text-[9px]">
              ⌘K
            </kbd>
          </button>
          
          <a
            href="https://github.com/buildwithpnj"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center h-9 w-9 rounded-xl border border-border bg-secondary text-muted-foreground hover:text-foreground hover:border-primary/30 transition-all"
          >
            <Github className="h-4 w-4" />
          </a>

          <ThemeToggle />
        </div>

        {/* Mobile Hamburger toggle */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden flex items-center justify-center p-2 rounded-xl text-muted-foreground hover:text-foreground hover:bg-accent transition-all"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <div className="md:hidden fixed inset-0 top-16 z-30 bg-background flex flex-col justify-between p-6 animate-fade-in">
          <nav className="flex flex-col gap-4">
            {navLinks.map((link) => {
              const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={cn(
                    'text-lg font-medium py-2 border-b border-border transition-colors',
                    isActive ? 'text-primary' : 'text-muted-foreground'
                  )}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          <div className="flex flex-col gap-4">
            <div className="flex items-center gap-3">
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  setTimeout(() => {
                    const event = new KeyboardEvent('keydown', { key: 'k', metaKey: true });
                    window.dispatchEvent(event);
                  }, 200);
                }}
                className="flex flex-1 items-center justify-center gap-2 h-12 rounded-xl border border-border bg-secondary text-muted-foreground text-sm font-medium"
              >
                <Command className="h-4 w-4" />
                <span>Search Console</span>
              </button>
              <div className="shrink-0 h-12 w-12 rounded-xl border border-border bg-secondary flex items-center justify-center">
                <ThemeToggle />
              </div>
            </div>
            <div className="flex justify-center gap-6 py-4">
              <a href="https://github.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground">GitHub</a>
              <a href="https://twitter.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground">Twitter</a>
              <a href="https://linkedin.com/in/pnj" target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-foreground">LinkedIn</a>
            </div>
            <div className="text-center text-xs text-muted-foreground">
              © 2026 BuildWithPNJ. All rights reserved.
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
