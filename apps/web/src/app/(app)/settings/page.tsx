'use client';

import { Settings, Shield, User, HardDrive, Cpu } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">System Config</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Settings className="h-7 w-7 text-primary" />
            OS Settings
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Configure system themes, security hashes, encryption keys, and connected cloud nodes.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Security / keys */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <Shield className="h-4 w-4 text-primary" />
            Cryptography & Security
          </h3>
          <div className="space-y-3 font-mono text-2xs">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Encryption Engine:</span>
              <span className="text-emerald-400 font-semibold">Fernet (AES-128-CBC)</span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Argon2 Password Hash:</span>
              <span className="text-foreground">Argon2id (active)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Session Expiry:</span>
              <span className="text-foreground">7 Days</span>
            </div>
          </div>
        </div>

        {/* Storage credentials summary */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
            <HardDrive className="h-4 w-4 text-primary" />
            Storage Credentials
          </h3>
          <div className="space-y-3 font-mono text-2xs">
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Google Client ID (A):</span>
              <span className="text-foreground truncate max-w-[180px]">200014542692-m2...</span>
            </div>
            <div className="flex justify-between border-b border-border/40 pb-2">
              <span className="text-muted-foreground">Google Client ID (B):</span>
              <span className="text-foreground truncate max-w-[180px]">711956582579-61...</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">OAuth Redirect URI:</span>
              <span className="text-foreground">/auth/google/callback</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
