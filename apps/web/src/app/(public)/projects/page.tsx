import React from 'react';
import { getProjects } from '@/lib/content';
import { ProjectsList } from '@/components/projects-list';

export const metadata = {
  title: 'Projects — BuildWithPNJ',
  description: 'Technical project showcase of Prakash Nandan Jha (PNJ), AI Engineer building production-grade tools in public.',
};

export default function PublicProjectsPage() {
  const projects = getProjects();

  return (
    <div className="flex flex-col gap-8 text-left">
      {/* Title */}
      <div className="flex flex-col gap-2">
        <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// PROJECTS"}</div>
        <h1 className="text-3xl sm:text-4xl font-pixel text-foreground">Engineering Builds</h1>
        <p className="text-base text-muted-foreground max-w-xl leading-relaxed">
          Open-source frameworks, local orchestrators, and full-stack software built with performance, security, and developer taste in mind.
        </p>
      </div>

      {/* Interactive search and cards listing */}
      <ProjectsList initialProjects={projects} />
    </div>
  );
}
