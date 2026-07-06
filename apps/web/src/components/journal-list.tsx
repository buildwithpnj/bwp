'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Search, Calendar, Clock } from 'lucide-react';
import { cn } from '@/lib/utils';
import { BlogPost } from '@/lib/content';

interface JournalListProps {
  initialPosts: BlogPost[];
}

export function JournalList({ initialPosts }: JournalListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTag, setSelectedTag] = useState<string>('All');

  // Extract all unique tags
  const allTags = ['All', ...Array.from(new Set(initialPosts.flatMap(post => post.tags)))];

  const filteredPosts = initialPosts.filter((post) => {
    const matchesSearch = 
      post.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
      post.tags.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));

    const matchesTag = 
      selectedTag === 'All' || 
      post.tags.some(t => t.toLowerCase() === selectedTag.toLowerCase());

    return matchesSearch && matchesTag;
  });

  return (
    <div className="flex flex-col gap-8 text-left">
      
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search journal entries..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full h-14 pl-12 pr-4 rounded-2xl border border-border bg-card text-foreground placeholder:text-muted-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
        />
      </div>

      {/* Tag filters */}
      <div className="flex flex-wrap gap-2 items-center text-xs">
        <span className="text-muted-foreground mr-2">Tags:</span>
        {allTags.map((tag) => (
          <button
            key={tag}
            onClick={() => setSelectedTag(tag)}
            className={cn(
              "h-8 px-4 rounded-full border transition-all active:scale-95",
              selectedTag === tag
                ? "border-primary bg-primary/10 text-foreground font-medium"
                : "border-border bg-card text-muted-foreground hover:text-foreground"
            )}
          >
            {tag === 'All' ? tag : `#${tag}`}
          </button>
        ))}
      </div>

      {/* Divider */}
      <div className="h-px bg-border my-2" />

      {/* Listing Grid */}
      {filteredPosts.length === 0 ? (
        <div className="py-16 text-center text-sm text-muted-foreground border border-dashed border-border rounded-2xl bg-card/20">
          No articles found matching your criteria.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredPosts.map((post) => (
            <Link
              key={post.slug}
              href={`/journal/${post.slug}`}
              className="group p-6 rounded-2xl border border-border bg-card flex flex-col justify-between gap-4 card-glow-hover"
            >
              <div className="flex flex-col gap-3">
                <div className="flex items-center gap-3 text-xs text-muted-foreground">
                  <span className="flex items-center gap-1"><Calendar className="h-3 w-3" /> {post.publishDate}</span>
                  <span>·</span>
                  <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> {post.readingTime} min read</span>
                </div>
                <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition-colors leading-snug">
                  {post.title}
                </h3>
                <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
                  {post.excerpt}
                </p>
              </div>

              <div className="flex flex-wrap gap-1.5 pt-3 border-t border-border">
                {post.tags.map((tag) => (
                  <span 
                    key={tag} 
                    className="text-[10px] px-2 py-0.5 rounded bg-primary/5 text-primary"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </Link>
          ))}
        </div>
      )}

    </div>
  );
}
