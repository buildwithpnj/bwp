import React from 'react';
import { Mail, Github, Twitter, Linkedin } from 'lucide-react';

export const metadata = {
  title: 'Contact — BuildWithPNJ',
  description: 'Connect with Prakash Nandan Jha (PNJ). Contact details for collaborations, consulting, and questions.',
};

export default function PublicContactPage() {
  return (
    <div className="min-h-[60vh] flex flex-col justify-center items-center py-10 px-4">
      
      <div className="w-full max-w-md flex flex-col gap-8 text-center sm:text-left">
        
        {/* Title */}
        <div className="flex flex-col gap-2 text-center">
          <div className="font-pixel text-[11px] text-primary tracking-wider uppercase">{"// CONTACT"}</div>
          <h1 className="text-3xl sm:text-4xl font-pixel text-foreground">{"Let's Connect"}</h1>
          <p className="text-sm text-muted-foreground leading-relaxed max-w-xs mx-auto">
            Got a system design question, an open-source idea, or want to collaborate?
          </p>
        </div>

        {/* Minimal Directory Card */}
        <div className="p-6 rounded-2xl border border-border bg-card flex flex-col gap-5 text-left relative overflow-hidden card-glow-hover">
          {/* Status badge */}
          <div className="flex items-center justify-between pb-3 border-b border-border text-xs">
            <span className="text-muted-foreground font-mono">STATUS:</span>
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full font-semibold bg-positive/10 text-positive">
              <span className="w-1.5 h-1.5 rounded-full bg-positive" />
              Open to Collabs & Consulting
            </span>
          </div>

          {/* Email link */}
          <a
            href="mailto:hello@buildwithpnj.com"
            className="flex items-center gap-4 p-3 rounded-xl border border-border bg-background hover:bg-accent group transition-all duration-200"
          >
            <div className="h-10 w-10 rounded-lg bg-card border border-border flex items-center justify-center text-primary group-hover:text-primary/80">
              <Mail className="h-4 w-4" />
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-muted-foreground font-mono leading-none">EMAIL DIRECT</span>
              <span className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors mt-1">hello@buildwithpnj.com</span>
            </div>
          </a>

          {/* Social connections */}
          <div className="flex flex-col gap-2.5">
            <div className="text-[10px] font-pixel text-muted-foreground tracking-widest uppercase mb-1">{"// SOCIAL NETWORKS"}</div>
            
            <a
              href="https://github.com/buildwithpnj"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-2 rounded-xl text-sm text-muted-foreground hover:text-foreground hover:bg-accent transition-all"
            >
              <div className="flex items-center gap-3">
                <Github className="h-4 w-4 text-muted-foreground" />
                <span>GitHub Profile</span>
              </div>
              <span className="text-[10px] font-mono text-muted-foreground">@buildwithpnj</span>
            </a>

            <a
              href="https://twitter.com/buildwithpnj"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-2 rounded-xl text-sm text-muted-foreground hover:text-foreground hover:bg-accent transition-all"
            >
              <div className="flex items-center gap-3">
                <Twitter className="h-4 w-4 text-muted-foreground" />
                <span>Twitter / X</span>
              </div>
              <span className="text-[10px] font-mono text-muted-foreground">@buildwithpnj</span>
            </a>

            <a
              href="https://linkedin.com/in/pnj"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-2 rounded-xl text-sm text-muted-foreground hover:text-foreground hover:bg-accent transition-all"
            >
              <div className="flex items-center gap-3">
                <Linkedin className="h-4 w-4 text-muted-foreground" />
                <span>LinkedIn Workspace</span>
              </div>
              <span className="text-[10px] font-mono text-muted-foreground">in/pnj</span>
            </a>
          </div>

        </div>

        {/* Info text */}
        <p className="text-center text-xs text-muted-foreground leading-relaxed max-w-xs mx-auto">
          Typically responds within 48 hours for engineering inquiries and open-source coordination.
        </p>

      </div>

    </div>
  );
}
