'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Search, Cpu } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Project } from '@/lib/content';

interface ProjectsListProps {
  initialProjects: Project[];
}

import { TerminalThumbnail } from './terminal-thumbnail';

export function ProjectsList({ initialProjects }: ProjectsListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('All');
  const [categoryFilter, setCategoryFilter] = useState<string>('All');

  const filteredProjects = initialProjects.filter((project) => {
    // Search match
    const matchesSearch = 
      project.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      project.tagline.toLowerCase().includes(searchQuery.toLowerCase()) ||
      project.techStack.some((tech) => tech.toLowerCase().includes(searchQuery.toLowerCase()));

    // Status filter match
    let matchesStatus = true;
    if (statusFilter !== 'All') {
      if (statusFilter === 'Active') matchesStatus = project.status === 'active';
      else if (statusFilter === 'Complete') matchesStatus = project.status === 'complete';
      else if (statusFilter === 'Experiment') matchesStatus = project.category === 'experiment';
      else if (statusFilter === 'Open Source') matchesStatus = !!project.githubUrl;
    }

    // Category filter match
    let matchesCategory = true;
    if (categoryFilter !== 'All') {
      if (categoryFilter === 'AI/ML') {
        matchesCategory = project.techStack.some((t) => 
          ['ai', 'llm', 'rag', 'multi-agent', 'pgvector', 'prompt-engineering'].includes(t.toLowerCase())
        );
      } else if (categoryFilter === 'Full-Stack') {
        matchesCategory = project.techStack.some((t) => 
          ['next.js', 'react', 'fastapi', 'postgresql', 'redis', 'typescript'].includes(t.toLowerCase())
        );
      } else if (categoryFilter === 'Tools') {
        matchesCategory = project.category === 'tool';
      } else if (categoryFilter === 'Research') {
        matchesCategory = project.category === 'experiment';
      }
    }

    return matchesSearch && matchesStatus && matchesCategory;
  });

  return (
    <div className="flex flex-col gap-8 text-left">
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search projects by name, tagline, or tech stack..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full h-14 pl-12 pr-4 rounded-2xl border border-border bg-card text-foreground placeholder:text-muted-foreground outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all"
        />
      </div>

      {/* Filter Options */}
      <div className="flex flex-col gap-4">
        {/* Status filters */}
        <div className="flex flex-wrap gap-2 items-center text-xs">
          <span className="text-muted-foreground mr-2">Filters:</span>
          {['All', 'Active', 'Complete', 'Experiment', 'Open Source'].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={cn(
                "h-8 px-4 rounded-full border transition-all active:scale-95",
                statusFilter === status
                  ? "border-primary bg-primary/10 text-foreground font-medium"
                  : "border-border bg-card text-muted-foreground hover:text-foreground"
              )}
            >
              {status}
            </button>
          ))}
        </div>

        {/* Category filters */}
        <div className="flex flex-wrap gap-2 items-center text-xs">
          <span className="text-muted-foreground mr-2">Categories:</span>
          {['All', 'AI/ML', 'Full-Stack', 'Tools', 'Research'].map((cat) => (
            <button
              key={cat}
              onClick={() => setCategoryFilter(cat)}
              className={cn(
                "h-8 px-4 rounded-full border transition-all active:scale-95",
                categoryFilter === cat
                  ? "border-primary bg-primary/10 text-foreground font-medium"
                  : "border-border bg-card text-muted-foreground hover:text-foreground"
              )}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Divider */}
      <div className="h-px bg-border my-2" />

      {/* Projects Grid */}
      {filteredProjects.length === 0 ? (
        <div className="py-16 text-center text-sm text-muted-foreground border border-dashed border-border rounded-2xl bg-card/20">
          No projects match the current search filters.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project, index) => (
            <Link
              key={project.slug}
              href={`/projects/${project.slug}`}
              className="group p-6 rounded-2xl border border-border bg-card flex flex-col gap-4 card-glow-hover"
            >
              <div className="aspect-video w-full rounded-xl bg-background flex items-center justify-center relative overflow-hidden border border-border">
                <div className="absolute inset-0 grid-dots opacity-20" />
                <TerminalThumbnail index={index} slug={project.slug} />
                <div className="absolute top-3 right-3 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-primary/10 text-primary capitalize">
                  {project.category}
                </div>
              </div>
              
              <div className="flex flex-col gap-1.5">
                <div className="flex items-center justify-between gap-4">
                  <h3 className="text-lg font-bold text-foreground group-hover:text-primary transition-colors line-clamp-1">{project.title}</h3>
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-secondary text-muted-foreground border border-border uppercase font-mono shrink-0">
                    {project.status}
                  </span>
                </div>
                <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                  {project.tagline}
                </p>
              </div>

              <div className="flex flex-wrap gap-1.5 mt-auto pt-3 border-t border-border">
                {project.techStack.map((tech) => (
                  <span key={tech} className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary text-muted-foreground border border-border">
                    {tech}
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
