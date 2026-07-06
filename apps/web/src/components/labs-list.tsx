'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Search } from 'lucide-react';
import { cn } from '@/lib/utils';
import { LabExperiment } from '@/lib/content';

interface LabsListProps {
  initialExperiments: LabExperiment[];
}

const CATEGORIES = [
  'All',
  'AI Agents',
  'Voice AI',
  'Automation',
  'Design Lab',
  'LLMs',
  'Research',
  'Open Source'
];

export function LabsList({ initialExperiments }: LabsListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  const filteredExperiments = initialExperiments.filter((exp) => {
    const matchesSearch = 
      exp.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      exp.tagline.toLowerCase().includes(searchQuery.toLowerCase()) ||
      exp.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesCategory = 
      activeCategory === 'All' || 
      exp.category.toLowerCase() === activeCategory.toLowerCase();

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="flex flex-col gap-8 text-left">
      
      {/* Category Pills */}
      <div className="flex flex-wrap gap-2 text-xs">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={cn(
              "h-9 px-4 rounded-full border transition-all active:scale-95",
              activeCategory === cat
                ? "border-primary bg-primary/10 text-foreground font-medium"
                : "border-border bg-card text-muted-foreground hover:text-foreground"
            )}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search experiments by hypothesis, tools used..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full h-14 pl-12 pr-4 rounded-2xl border border-border bg-card text-foreground placeholder:text-muted-foreground outline-none focus:border-primary/40 focus:ring-1 focus:ring-primary"
        />
      </div>

      {/* Grid */}
      {filteredExperiments.length === 0 ? (
        <div className="py-16 text-center text-sm text-muted-foreground border border-dashed border-border rounded-2xl bg-card/20">
          No experiments found matching &ldquo;{searchQuery}&rdquo; under {activeCategory}.
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {filteredExperiments.map((exp) => (
            <Link
              key={exp.slug}
              href={`/labs/${exp.slug}`}
              className="group p-6 rounded-2xl border-l-4 border-l-primary border-y border-r border-border bg-card hover:bg-accent hover:border-r-primary/20 hover:border-y-primary/20 flex flex-col sm:flex-row sm:items-center justify-between gap-6 transition-all duration-200"
            >
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <span className="font-mono text-xs font-semibold text-primary tracking-wider bg-primary/5 border border-primary/10 px-2 py-0.5 rounded">
                    {exp.id}
                  </span>
                  <span className="text-xs text-muted-foreground">{exp.category}</span>
                </div>
                <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition-colors">{exp.title}</h3>
                <p className="text-sm text-muted-foreground line-clamp-2 max-w-2xl leading-relaxed">
                  {exp.tagline}
                </p>
              </div>

              <div className="flex sm:flex-col items-start sm:items-end justify-between sm:justify-center gap-4 shrink-0 border-t sm:border-t-0 border-border pt-4 sm:pt-0">
                <span className={cn(
                  "px-3 py-1 rounded-full text-[10px] font-semibold font-mono uppercase tracking-wider",
                  exp.status === 'live' ? 'bg-positive/10 text-positive' :
                  exp.status === 'wip' ? 'bg-yellow-500/10 text-yellow-500' :
                  'bg-red-500/10 text-red-500'
                )}>
                  ● {exp.status}
                </span>
                
                <div className="flex flex-wrap gap-1">
                  {exp.tags.slice(0, 2).map((t) => (
                    <span key={t} className="text-[10px] px-2 py-0.5 rounded bg-secondary text-muted-foreground border border-border">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

    </div>
  );
}
