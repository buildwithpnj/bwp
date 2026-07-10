import React from 'react';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { ArrowLeft, ExternalLink, Github, BookOpen, Calendar, HelpCircle } from 'lucide-react';
import { getProjectBySlug } from '@/lib/content';
import { cn } from '@/lib/utils';

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const project = getProjectBySlug(slug);
  if (!project) return { title: 'Project Not Found' };

  return {
    title: project.title,
    description: project.tagline,
    alternates: {
      canonical: `/projects/${project.slug}`,
    },
    openGraph: {
      title: project.title,
      description: project.tagline,
      url: `https://buildwithpnj.in/projects/${project.slug}`,
      type: 'website',
      siteName: 'BuildWithPNJ',
    },
    twitter: {
      card: 'summary_large_image',
      title: project.title,
      description: project.tagline,
      creator: '@buildwithpnj',
    },
  };
}

export default async function PublicProjectDetailPage({ params }: PageProps) {
  const { slug } = await params;
  const project = getProjectBySlug(slug);

  if (!project) {
    notFound();
  }

  // Get active status color
  const statusColor = 
    project.status === 'active' ? 'bg-positive/10 text-positive' :
    project.status === 'complete' ? 'bg-primary/10 text-primary' :
    project.status === 'planned' ? 'bg-yellow-500/10 text-yellow-500' :
    'bg-muted/15 text-muted-foreground';

  return (
    <div className="flex flex-col gap-10 text-left">
      
      {/* Back link */}
      <div>
        <Link 
          href="/projects" 
          className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" /> Back to Projects
        </Link>
      </div>

      {/* Header section */}
      <div className="flex flex-col gap-4 border-b border-border pb-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex flex-col gap-1">
            <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// PROJECT"}</div>
            <h1 className="text-3xl sm:text-4xl font-pixel text-foreground">{project.title}</h1>
          </div>
          <span className={cn("self-start sm:self-auto inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider font-mono", statusColor)}>
            ● {project.status}
          </span>
        </div>

        <p className="text-lg text-muted-foreground max-w-3xl leading-relaxed">
          {project.tagline}
        </p>

        {/* CTAs */}
        <div className="flex flex-wrap gap-3 mt-2">
          {project.liveUrl && (
            <a
              href={project.liveUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 h-10 px-4 rounded-xl text-xs font-semibold bg-primary hover:opacity-90 text-primary-foreground transition-all active:scale-[0.98]"
            >
              Live Demo <ExternalLink className="h-3 w-3" />
            </a>
          )}
          {project.githubUrl && (
            <a
              href={project.githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 h-10 px-4 rounded-xl text-xs font-semibold border border-border hover:border-primary/30 bg-card hover:bg-accent text-muted-foreground hover:text-foreground transition-all active:scale-[0.98]"
            >
              GitHub <Github className="h-3 w-3" />
            </a>
          )}
          <Link
            href="/journal/building-personal-os-from-scratch"
            className="inline-flex items-center gap-1.5 h-10 px-4 rounded-xl text-xs font-semibold border border-border hover:border-primary/30 bg-card hover:bg-accent text-muted-foreground hover:text-foreground transition-all active:scale-[0.98]"
          >
            Read Architecture Article <BookOpen className="h-3 w-3" />
          </Link>
        </div>
      </div>

      {/* Grid Layout: Main info (8 cols) + tech stack sidebar (4 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        
        {/* Main Column */}
        <div className="lg:col-span-8 flex flex-col gap-10">
          
          {/* Compiled markdown overview */}
          <section className="prose dark:prose-invert max-w-none text-foreground leading-relaxed prose-headings:font-pixel prose-headings:text-foreground prose-h2:text-xl prose-h2:border-b prose-h2:border-border prose-h2:pb-2 prose-h2:mt-8">
            <div dangerouslySetInnerHTML={{ __html: project.contentHtml }} />
          </section>

          {/* Timeline */}
          {project.timeline && project.timeline.length > 0 && (
            <section className="flex flex-col gap-4 border-t border-border pt-8">
              <h2 className="font-pixel text-xl text-foreground tracking-tight uppercase">{"// TIMELINE"}</h2>
              <div className="flex flex-col gap-0 border-l border-border pl-4 ml-2">
                {project.timeline.map((event, index) => (
                  <div key={index} className="relative py-3 group">
                    <span className="absolute -left-[21px] top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-primary" />
                    <p className="text-sm text-foreground font-medium leading-none">{event}</p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Challenges & Lessons learned */}
          {project.challenges && project.challenges.length > 0 && (
            <section className="flex flex-col gap-4 border-t border-border pt-8">
              <h2 className="font-pixel text-xl text-foreground tracking-tight uppercase">{"// CHALLENGES & LESSONS"}</h2>
              <div className="flex flex-col gap-3">
                {project.challenges.map((challenge, index) => (
                  <div key={index} className="p-5 rounded-2xl border border-border bg-card">
                    <div className="flex items-center gap-2 mb-2">
                      <HelpCircle className="h-4 w-4 text-primary" />
                      <h4 className="font-bold text-foreground text-sm">{challenge.title}</h4>
                    </div>
                    <p className="text-xs text-muted-foreground leading-relaxed pl-6">
                      {challenge.content}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

        </div>

        {/* Sidebar Column */}
        <div className="lg:col-span-4 flex flex-col gap-6 lg:sticky lg:top-24 h-fit">
          
          {/* Tech Stack Details */}
          <div className="p-5 rounded-2xl border border-border bg-card flex flex-col gap-4">
            <h3 className="font-pixel text-xs text-foreground tracking-wider uppercase">{"// TECH STACK"}</h3>
            <div className="flex flex-col gap-2.5">
              {project.techStack.map((tech) => (
                <div key={tech} className="flex items-center gap-3 p-2 rounded-xl bg-background border border-border">
                  <span className="w-2 h-2 rounded-full bg-primary" />
                  <span className="text-sm font-medium text-foreground">{tech}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Metadata Card */}
          <div className="p-5 rounded-2xl border border-border bg-card flex flex-col gap-4 font-mono text-xs text-muted-foreground">
            <h3 className="font-pixel text-xs text-foreground tracking-wider uppercase font-sans">{"// METADATA"}</h3>
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span>STARTED:</span>
              <span className="text-foreground">{project.startDate}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span>PUBLISHED:</span>
              <span className="text-foreground">{project.publishDate}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span>STATUS:</span>
              <span className="text-foreground capitalize">{project.status}</span>
            </div>
          </div>

        </div>

      </div>

    </div>
  );
}
