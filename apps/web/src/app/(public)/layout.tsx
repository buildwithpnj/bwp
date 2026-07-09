import React from 'react';
import { PublicHeader } from '@/components/public-header';
import { PublicFooter } from '@/components/public-footer';
import { PublicCommandPalette } from '@/components/public-command-palette';

export default function PublicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-x-hidden antialiased">
      {/* Visual background layers */}
      <div className="scanlines" />
      <div className="absolute inset-0 grid-dots pointer-events-none" />
      <div className="ambient-glow" />
      <div className="noise-overlay" />

      {/* Floating gradient orbs for ambient depth */}
      <div
        className="floating-orb"
        style={{ top: '10%', right: '15%', width: '400px', height: '400px', background: 'rgba(59, 130, 246, 0.03)' }}
      />
      <div
        className="floating-orb"
        style={{ bottom: '20%', left: '10%', width: '300px', height: '300px', background: 'rgba(139, 92, 246, 0.02)', animationDelay: '-10s' }}
      />
      {/* Page shell */}
      <div className="relative z-10 flex flex-col min-h-screen justify-between">
        <div>
          <PublicHeader />
          <main className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 relative z-20">
            {children}
          </main>
        </div>
        <PublicFooter />
      </div>

      {/* Command Palette navigation handler */}
      <PublicCommandPalette />
    </div>
  );
}
