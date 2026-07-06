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
