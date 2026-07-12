'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Send, RefreshCw, Terminal, Activity, ArrowRight, ShieldCheck } from 'lucide-react';

interface ChatMessage {
  sender: 'user' | 'agent';
  text: string;
}

export default function WarbornAuthenticatedApp() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Generate a random local session token on mount
    setSessionId(Math.random().toString(36).substring(2, 15));
    setMessages([
      {
        sender: 'agent',
        text: "Warborn Terminal Session Activated. Unrestricted agentEnglish runtime available. You have full system capabilities."
      }
    ]);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || loading) return;

    const userText = inputText;
    setInputText('');
    setMessages(prev => [...prev, { sender: 'user', text: userText }]);
    setLoading(true);
    setErrorMsg(null);

    try {
      const apiHost = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const token = localStorage.getItem('token') || '';
      
      const res = await fetch(`${apiHost}/api/warborn/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userText
        }),
      });

      if (res.status === 401) {
        setErrorMsg("Session expired or unauthorized. Please log in again.");
        return;
      }

      const data = await res.json();
      setMessages(prev => [...prev, { sender: 'agent', text: data.message }]);
    } catch (err) {
      console.error(err);
      setErrorMsg("Connection error to Warborn backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in text-foreground text-left">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-mono font-bold uppercase tracking-[0.25em] text-primary flex items-center gap-1">
            <ShieldCheck className="h-3 w-3" /> {"SECURE CONNECTION ACTIVE"}
          </span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Terminal className="h-7 w-7 text-primary" />
            {"Warborn Authenticated Terminal"}
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            {"Accessing local agentEnglish models with private memory, file utilities, and advanced tools."}
          </p>
        </div>
      </div>

      {/* Main Console Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Left Status Bar */}
        <div className="lg:col-span-1 space-y-4">
          <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4 font-mono text-[10px]">
            <h3 className="text-2xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5 border-b border-border/40 pb-2">
              <Activity className="h-3.5 w-3.5 text-primary" />
              {"SYSTEM TELEMETRY"}
            </h3>
            <div className="space-y-2 text-muted-foreground">
              <div className="flex justify-between">
                <span>{"Tenant Isolation:"}</span>
                <span className="text-emerald-400 font-bold">{"ENABLED"}</span>
              </div>
              <div className="flex justify-between">
                <span>{"Private Memory:"}</span>
                <span className="text-foreground">{"ACTIVE"}</span>
              </div>
              <div className="flex justify-between">
                <span>{"Model Router:"}</span>
                <span className="text-foreground">{"gpt-4o-mini"}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Chat window */}
        <div className="lg:col-span-3 rounded-2xl border border-border bg-card/45 flex flex-col h-[500px] overflow-hidden shadow-lg backdrop-blur-sm">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[85%] rounded-xl px-4 py-2.5 text-xs leading-relaxed ${
                    m.sender === 'user'
                      ? 'bg-primary text-primary-foreground font-semibold'
                      : 'bg-secondary text-foreground border border-border/60 font-mono'
                  }`}
                >
                  {m.text}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-secondary text-muted-foreground border border-border/40 rounded-xl px-4 py-2.5 text-xs font-mono flex items-center gap-2">
                  <span className="h-1.5 w-1.5 rounded-full bg-primary animate-bounce" />
                  <span className="h-1.5 w-1.5 rounded-full bg-primary animate-bounce delay-75" />
                  <span className="h-1.5 w-1.5 rounded-full bg-primary animate-bounce delay-150" />
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          {/* Form input */}
          <form onSubmit={handleSend} className="border-t border-border/60 p-3 bg-secondary/20 flex gap-2">
            <input
              type="text"
              placeholder="Ask anything, format queries, run corrections..."
              disabled={loading}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              className="flex-1 h-9 px-3.5 rounded-lg border border-border/40 bg-background/50 text-xs focus:outline-none focus:border-primary/50"
            />
            <button
              type="submit"
              disabled={loading || !inputText.trim()}
              className="h-9 w-9 rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground flex items-center justify-center transition-all disabled:opacity-50"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      </div>
      
      {errorMsg && (
        <div className="text-center font-mono text-[10px] text-rose-400">
          {errorMsg}
        </div>
      )}
    </div>
  );
}
