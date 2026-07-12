'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, CheckCircle2 } from 'lucide-react';

export default function RequestAccessPage() {
  const [submitted, setSubmitted] = useState(false);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [reason, setReason] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || !email || !reason) return;
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen text-foreground relative grid-dots py-12 px-6 flex flex-col items-center justify-center">
      <div className="max-w-md w-full space-y-6 bg-card/45 p-8 border border-border rounded-2xl shadow-xl backdrop-blur-sm">
        {/* Back Link */}
        <Link
          href="/warborn"
          className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground font-mono transition-colors"
        >
          <ArrowLeft className="h-3.5 w-3.5" /> {"Back to Warborn"}
        </Link>

        {submitted ? (
          <div className="text-center py-6 space-y-4 font-mono text-xs">
            <div className="flex justify-center text-primary">
              <CheckCircle2 className="h-10 w-10" />
            </div>
            <h2 className="text-base font-bold text-foreground">{"Access Request Received"}</h2>
            <p className="text-muted-foreground leading-relaxed">
              {"Thank you for your interest. We will review your application and issue credential credentials if approved."}
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4 text-left">
            <div>
              <h2 className="text-base font-bold">{"Request System Access"}</h2>
              <p className="text-2xs text-muted-foreground mt-0.5">
                {"Apply for authenticated developer credentials to access the unrestricted Warborn dashboard."}
              </p>
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div className="space-y-1">
                <label className="text-[10px] text-muted-foreground uppercase font-bold">{"Full Name *"}</label>
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full h-10 px-3.5 rounded-xl border border-border/40 bg-background/50 text-xs focus:outline-none focus:border-primary/50"
                  placeholder="John Doe"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] text-muted-foreground uppercase font-bold">{"Email Address *"}</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full h-10 px-3.5 rounded-xl border border-border/40 bg-background/50 text-xs focus:outline-none focus:border-primary/50"
                  placeholder="john@example.com"
                />
              </div>

              <div className="space-y-1">
                <label className="text-[10px] text-muted-foreground uppercase font-bold">{"Intended Use Case / Reason *"}</label>
                <textarea
                  required
                  rows={4}
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  className="w-full p-3.5 rounded-xl border border-border/40 bg-background/50 text-xs focus:outline-none focus:border-primary/50 resize-none leading-relaxed"
                  placeholder="Explain why you require access to the agent orchestrator console..."
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full h-10 rounded-xl bg-primary text-primary-foreground font-semibold hover:bg-primary/95 flex items-center justify-center transition-all text-xs"
            >
              {"Submit Request"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
