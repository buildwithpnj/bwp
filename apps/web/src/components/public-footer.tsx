import React from 'react';
import Link from 'next/link';

export function PublicFooter() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full border-t border-border bg-background py-12 md:py-16 mt-20 relative z-20">
      <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 lg:gap-12 text-left">
          
          {/* Brand Column */}
          <div className="md:col-span-2 flex flex-col gap-4">
            <Link href="/" className="font-pixel text-2xl tracking-widest text-primary">
              PNJ
            </Link>
            <p className="text-sm text-muted-foreground max-w-sm leading-relaxed">
              AI Engineer building production-ready systems in public. Sharing architecture decisions, codebase iterations, and practical learnings.
            </p>
          </div>

          {/* Navigation Links Column */}
          <div className="flex flex-col gap-3">
            <h4 className="font-pixel text-xs text-foreground uppercase tracking-wider">{"// NAVIGATE"}</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <Link href="/" className="hover:text-foreground transition-colors">Home</Link>
              <Link href="/projects" className="hover:text-foreground transition-colors">Projects</Link>
              <Link href="/labs" className="hover:text-foreground transition-colors">Labs</Link>
              <Link href="/journal" className="hover:text-foreground transition-colors">Journal</Link>
              <Link href="/about" className="hover:text-foreground transition-colors">About</Link>
              <Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link>
              <Link href="/mission-control" className="hover:text-foreground transition-colors">Mission Control</Link>
            </div>
          </div>

          {/* Connect Column */}
          <div className="flex flex-col gap-3">
            <h4 className="font-pixel text-xs text-foreground uppercase tracking-wider">{"// CONNECT"}</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <a href="https://github.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">GitHub ↗</a>
              <a href="https://twitter.com/buildwithpnj" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">Twitter / X ↗</a>
              <a href="https://linkedin.com/in/pnj" target="_blank" rel="noopener noreferrer" className="hover:text-foreground transition-colors">LinkedIn ↗</a>
              <a href="mailto:hello@buildwithpnj.com" className="hover:text-foreground transition-colors">Email ↗</a>
            </div>
          </div>

        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-border flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-muted-foreground text-center sm:text-left">
            © {currentYear} BuildWithPNJ. All rights reserved.
          </p>
          <p className="text-xs text-muted-foreground text-center sm:text-right">
            Built with Next.js & Tailwind. Deployed on Vercel.
          </p>
        </div>
      </div>
    </footer>
  );
}
