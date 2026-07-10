'use client';

import { BookOpen, Search, Compass, HardDrive, Star, ArrowUpRight } from 'lucide-react';
import Link from 'next/link';

export default function KnowledgeBasePage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">AI Context</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <BookOpen className="h-7 w-7 text-primary" />
            Knowledge Base
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Structured information, documentation wikis, guides, and vectorized reference logs.
          </p>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* pinned wikis */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Star className="h-4 w-4 text-primary fill-primary/10" />
            Featured Guides
          </h3>
          <div className="space-y-3">
            {[
              { title: 'Google drive developer console credentials setup.md', href: '/notes' },
              { title: 'Warborn OS Phase 2 architecture decisions.md', href: '/notes' },
            ].map((wiki, idx) => (
              <Link
                key={idx}
                href={wiki.href}
                className="block p-3 rounded-xl border border-border/60 bg-muted/20 hover:bg-muted/40 hover:border-primary/20 transition-all group"
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs font-semibold truncate group-hover:text-primary transition-colors">
                    {wiki.title}
                  </span>
                  <ArrowUpRight className="h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Categories */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Compass className="h-4 w-4 text-primary" />
            Subject Index
          </h3>
          <div className="space-y-2 text-xs font-mono text-muted-foreground">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span>Engineering (OS kernel, Alembic schemas):</span>
              <span className="text-foreground font-semibold">12 notes</span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span>Financial logs (Balances, sync logs):</span>
              <span className="text-foreground font-semibold">4 notes</span>
            </div>
            <div className="flex justify-between">
              <span>External API reference guides:</span>
              <span className="text-foreground font-semibold">7 notes</span>
            </div>
          </div>
        </div>

        {/* storage node alignment */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <HardDrive className="h-4 w-4 text-primary" />
            Storage Node Reference
          </h3>
          <p className="text-xs text-muted-foreground leading-relaxed">
            All notes and wiki articles are stored locally in the database and periodically backed up to the target primary Google Drive (A) node.
          </p>
        </div>
      </div>
    </div>
  );
}
