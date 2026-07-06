import React from 'react';
import Link from 'next/link';
import { ArrowRight, Zap, FlaskConical, Radio, Cpu, Activity } from 'lucide-react';
import { getBlogPosts, getProjects, getExperiments } from '@/lib/content';
import { NewsletterForm } from '@/components/newsletter-form';
import { Terminal } from '@/components/ui/terminal';
import { AIPortraitHero } from '@/components/ai-portrait-hero';

export default async function PublicHomePage() {
  const projects = getProjects().slice(0, 3);
  const posts = getBlogPosts().slice(0, 3);
  const experiments = getExperiments().slice(0, 4);

  return (
    <div className="flex flex-col gap-0 w-full">
      {/* 1. HERO SECTION v2.0 */}
      <AIPortraitHero />
      
      {/* Boxed Content Area */}
      <div className="container max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28 flex flex-col gap-24 md:gap-32 text-left">
        
        {/* 2. MISSION SECTION */}
        <section className="flex flex-col gap-8">
          <div className="flex flex-col gap-2">
            <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// MISSION"}</div>
            <h2 className="text-2xl sm:text-3xl font-bold text-foreground tracking-tight">
              I build systems that solve real problems — then share the blueprints.
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl border border-border bg-card flex flex-col gap-3">
              <Zap className="h-6 w-6 text-primary" />
              <h3 className="text-lg font-semibold text-foreground">Ship Fast</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Iterating quickly in the open. Shipping working software to production, avoiding theoretical engineering delays.
              </p>
            </div>
            <div className="p-6 rounded-2xl border border-border bg-card flex flex-col gap-3">
              <FlaskConical className="h-6 w-6 text-primary" />
              <h3 className="text-lg font-semibold text-foreground">Build Real</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Constructing context-aware, database-driven tools designed for daily operations, not throwaway code snippets.
              </p>
            </div>
            <div className="p-6 rounded-2xl border border-border bg-card flex flex-col gap-3">
              <Radio className="h-6 w-6 text-primary" />
              <h3 className="text-lg font-semibold text-foreground">Share Blueprints</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Publishing detailed system architectures, database migration struggles, and codebase reviews for other engineers.
              </p>
            </div>
          </div>
        </section>

        {/* 3. DEDICATED WARBORN OS SECTION */}
        <section className="flex flex-col gap-8">
          <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// THE ENGINE"}</div>
          
          <div className="p-6 sm:p-8 rounded-2xl border border-border bg-card relative overflow-hidden flex flex-col lg:flex-row gap-8 items-center card-glow-hover">
            <div className="absolute top-0 right-0 w-[200px] h-[200px] bg-primary/5 blur-[80px] pointer-events-none" />

            <div className="flex-1 flex flex-col gap-6 w-full text-left">
              <div className="flex flex-col gap-1.5">
                <span className="font-pixel text-xs tracking-widest text-primary uppercase">
                  INTRODUCING
                </span>
                <h2 className="text-3xl font-bold text-foreground">Warborn OS</h2>
                <p className="text-sm font-mono text-muted-foreground">
                  My AI Operating System, Built inside BuildWithPNJ
                </p>
              </div>

              <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
                Warborn OS is the authenticated workflow engine behind BuildWithPNJ. It serves as my personal workspace to manage notes, finances, habits, and Google Drive storage sync in real-time, leveraging context-aware local intelligence.
              </p>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-4 border-y border-border">
                <div>
                  <div className="font-mono text-xl font-bold text-primary">12</div>
                  <div className="text-xs text-muted-foreground">OS Modules</div>
                </div>
                <div>
                  <div className="font-mono text-xl font-bold text-primary">847</div>
                  <div className="text-xs text-muted-foreground">Total Commits</div>
                </div>
                <div>
                  <div className="font-mono text-xl font-bold text-primary">9</div>
                  <div className="text-xs text-muted-foreground">Integrations</div>
                </div>
                <div>
                  <div className="font-mono text-xl font-bold text-primary">6mo</div>
                  <div className="text-xs text-muted-foreground">Active Dev</div>
                </div>
              </div>

              <div className="flex flex-wrap items-center gap-4">
                <Link
                  href="/dashboard"
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-primary text-primary-foreground hover:opacity-90 transition-all active:scale-[0.98]"
                >
                  Explore Dashboard <ArrowRight className="h-3.5 w-3.5" />
                </Link>
                <Link
                  href="/projects/personal-os"
                  className="text-xs font-medium text-muted-foreground hover:text-foreground border border-border bg-secondary hover:bg-accent px-4 py-2 rounded-xl transition-all"
                >
                  View Architecture
                </Link>
              </div>
            </div>

            <Terminal 
              title="warborn_telemetry.log"
              lines={[
                'API  HTTP/1.1 POST /habits/check_in [200 OK]',
                'TASK celery_worker_1: job_id_894 success',
                'DB   pgvector lookup: notes match 94.6%',
                'MEM  Redis caching keys: 156 initialized',
                'SYNC Google Drive API: 0 changes pending'
              ]}
              className="w-full lg:w-[320px] shrink-0"
              showPrompt={true}
            />
          </div>
        </section>

        {/* 4. FEATURED PROJECTS SECTION */}
        <section className="flex flex-col gap-8">
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-1">
              <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// PROJECTS"}</div>
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Active Builds</h2>
            </div>
            <Link href="/projects" className="flex items-center gap-1.5 text-sm font-semibold text-primary hover:text-primary/80 transition-colors">
              All Projects <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Link
                key={project.slug}
                href={`/projects/${project.slug}`}
                className="group p-5 rounded-2xl border border-border bg-card flex flex-col gap-4 card-glow-hover"
              >
                <div className="aspect-video w-full rounded-lg bg-background flex items-center justify-center relative overflow-hidden border border-border">
                  <div className="absolute inset-0 grid-dots opacity-40" />
                  <Cpu className="h-8 w-8 text-muted-foreground group-hover:text-primary group-hover:scale-110 transition-all duration-300" />
                  <div className="absolute top-2 right-2 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-primary/10 text-primary capitalize">
                    {project.category}
                  </div>
                </div>
                <div className="flex flex-col gap-1">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">{project.title}</h3>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-secondary text-muted-foreground border border-border uppercase font-mono">
                      {project.status}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                    {project.tagline}
                  </p>
                </div>
                <div className="flex flex-wrap gap-1.5 mt-auto pt-2 border-t border-border">
                  {project.techStack.slice(0, 3).map((tech) => (
                    <span key={tech} className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary text-muted-foreground">
                      {tech}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* 5. ENGINEERING JOURNAL PREVIEW */}
        <section className="flex flex-col gap-8">
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-1">
              <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// ENGINEERING JOURNAL"}</div>
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Recent Articles</h2>
            </div>
            <Link href="/journal" className="flex items-center gap-1.5 text-sm font-semibold text-primary hover:text-primary/80 transition-colors">
              All Articles <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {posts.map((post) => (
              <Link
                key={post.slug}
                href={`/journal/${post.slug}`}
                className="group p-5 rounded-2xl border border-border bg-card flex flex-col justify-between gap-4 card-glow-hover"
              >
                <div className="flex flex-col gap-3">
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{post.publishDate}</span>
                    <span>·</span>
                    <span>{post.readingTime} min read</span>
                  </div>
                  <h3 className="font-semibold text-base text-foreground group-hover:text-primary transition-colors leading-snug line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-xs text-muted-foreground line-clamp-2 leading-relaxed">
                    {post.excerpt}
                  </p>
                </div>
                <div className="flex flex-wrap gap-1.5 pt-2 border-t border-border">
                  {post.tags.map((tag) => (
                    <span key={tag} className="text-[10px] px-1.5 py-0.5 rounded bg-primary/5 text-primary">
                      #{tag}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* 6. LABS PREVIEW SECTION */}
        <section className="flex flex-col gap-8">
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-1">
              <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// R&D LABS"}</div>
              <h2 className="text-2xl font-bold text-foreground tracking-tight">Experiments</h2>
            </div>
            <Link href="/labs" className="flex items-center gap-1.5 text-sm font-semibold text-primary hover:text-primary/80 transition-colors">
              Explore Labs <ArrowRight className="h-4 w-4" />
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {experiments.map((exp) => (
              <Link
                key={exp.slug}
                href={`/labs/${exp.slug}`}
                className="p-5 rounded-2xl border border-border bg-card hover:bg-accent flex flex-col gap-3 transition-all duration-200"
              >
                <div className="w-8 h-8 rounded-lg bg-background flex items-center justify-center border border-border font-pixel text-xs text-primary">
                  🧪
                </div>
                <div>
                  <h3 className="text-sm font-bold text-foreground truncate">{exp.title}</h3>
                  <p className="text-[11px] text-muted-foreground truncate">{exp.category}</p>
                </div>
                <div className="text-[10px] font-mono text-muted-foreground mt-auto">
                  Status: <span className="text-positive uppercase">{exp.status}</span>
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* 7. MISSION CONTROL SUMMARY */}
        <section className="p-6 sm:p-8 rounded-2xl border border-border bg-card relative overflow-hidden flex flex-col sm:flex-row items-center justify-between gap-6 card-glow-hover">
          <div className="flex flex-col gap-2 text-left w-full">
            <div className="flex items-center gap-2">
              <Activity className="h-4 w-4 text-primary" />
              <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">TELEMETRY STREAM</div>
            </div>
            <h3 className="text-xl font-bold text-foreground">Mission Control Dashboard</h3>
            <p className="text-sm text-muted-foreground max-w-md">
              View live engineering data, commits telemetry, weekly targets checkerboards, and automated system health meters.
            </p>
          </div>
          <Link
            href="/mission-control"
            className="shrink-0 flex items-center justify-center gap-2 h-10 px-5 rounded-xl text-xs font-semibold border border-border bg-secondary hover:bg-accent text-muted-foreground hover:text-foreground transition-all active:scale-[0.98]"
          >
            Enter Command Center <ArrowRight className="h-3 w-3" />
          </Link>
        </section>

        {/* 8. NEWSLETTER CONTAINER */}
        <section className="py-12 border-t border-border flex flex-col items-center text-center gap-6">
          <div className="flex flex-col gap-2 max-w-md">
            <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// STAY IN THE LOOP"}</div>
            <h2 className="text-2xl font-bold text-foreground">Subscribe to the Builder Crew</h2>
            <p className="text-sm text-muted-foreground leading-relaxed">
              AI engineering logs, deep architectures reviews, and full-stack breakdowns delivered directly.
            </p>
          </div>

          <NewsletterForm />
          <span className="text-[11px] text-muted-foreground">No spam. Unsubscribe anytime.</span>
        </section>

      </div>
    </div>
  );
}
