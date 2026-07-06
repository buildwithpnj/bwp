'use client';

import React, { useState } from 'react';

export function NewsletterForm() {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email.trim()) {
      setSubscribed(true);
      setEmail('');
    }
  };

  if (subscribed) {
    return (
      <div className="h-12 flex items-center justify-center font-mono text-xs text-positive bg-positive/10 border border-positive/20 px-6 rounded-xl animate-fade-in">
        ✓ Subscription confirmed. Welcome to the crew!
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-3 w-full max-w-md mt-2">
      <input
        type="email"
        placeholder="your@email.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full h-12 px-4 rounded-xl border border-border bg-card text-foreground placeholder:text-muted-foreground outline-none text-xs focus:border-primary focus:ring-1 focus:ring-primary transition-all"
        required
      />
      <button
        type="submit"
        className="w-full sm:w-auto h-12 px-6 shrink-0 rounded-xl font-semibold bg-primary text-primary-foreground hover:opacity-90 active:scale-[0.98] transition-all"
      >
        Subscribe
      </button>
    </form>
  );
}
