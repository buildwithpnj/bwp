import React from 'react';
import { getBlogPosts } from '@/lib/content';
import { JournalList } from '@/components/journal-list';

export const metadata = {
  title: 'Engineering Journal — BuildWithPNJ',
  description: 'Technical writing on AI systems architecture, building in public updates, monorepos, and FastAPI backend engineering.',
};

export default function PublicJournalPage() {
  const posts = getBlogPosts();

  return (
    <div className="flex flex-col gap-8 text-left">
      {/* Title */}
      <div className="flex flex-col gap-2">
        <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// ENGINEERING JOURNAL"}</div>
        <h1 className="text-3xl sm:text-4xl font-pixel text-foreground">Code & Logic Logs</h1>
        <p className="text-base text-muted-foreground max-w-xl leading-relaxed">
          Deep architectural reviews, Monorepo setups, databases migrations, and direct progress updates about building AI-first software.
        </p>
      </div>

      {/* Filter and listing cards */}
      <JournalList initialPosts={posts} />
    </div>
  );
}
