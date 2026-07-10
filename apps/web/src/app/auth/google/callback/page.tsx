'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Loader2, CheckCircle2, XCircle, HardDrive } from 'lucide-react';
import { api } from '@/lib/api';

import { Suspense } from 'react';

function GoogleDriveBCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [errorMsg, setErrorMsg] = useState('');
  const [email, setEmail] = useState('');
  const callbackCalled = useRef(false);

  useEffect(() => {
    // Prevent duplicate calls in React StrictMode
    if (callbackCalled.current) return;
    callbackCalled.current = true;

    const code = searchParams.get('code');

    if (!code) {
      setStatus('error');
      setErrorMsg('No authorization code found in URL.');
      return;
    }

    async function handleCallback() {
      try {
        const res = await api<{ status: string; email?: string; provider?: string }>(
          '/api/storage/auth/google/provider-b/callback',
          {
            method: 'POST',
            body: { code },
          }
        );
        setEmail(res.email ?? '');
        setStatus('success');
        setTimeout(() => {
          router.push('/storage');
        }, 2500);
      } catch (err: unknown) {
        setStatus('error');
        const message = err instanceof Error ? err.message : 'Unknown error during connection';
        setErrorMsg(message);
      }
    }

    handleCallback();
  }, [searchParams, router]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-6 text-center bg-background">
      <div className="w-full max-w-md rounded-2xl border border-border bg-card p-10 shadow-xl">
        <div className="mb-6 flex justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-blue-500/10 border border-blue-500/30">
            <HardDrive className="h-8 w-8 text-blue-400" />
          </div>
        </div>

        <div className="mb-2 text-xs font-bold uppercase tracking-[0.25em] text-blue-400">
          WARBORN OS — DRIVE B
        </div>

        {status === 'loading' && (
          <div className="flex flex-col items-center gap-4">
            <Loader2 className="h-10 w-10 animate-spin text-blue-400" />
            <h1 className="text-xl font-semibold text-foreground">Connecting Google Drive B…</h1>
            <p className="text-sm text-muted-foreground">
              Exchanging authorization code and registering your secondary drive account.
            </p>
          </div>
        )}

        {status === 'success' && (
          <div className="flex flex-col items-center gap-4">
            <CheckCircle2 className="h-12 w-12 text-emerald-500 animate-bounce" />
            <h1 className="text-xl font-bold text-foreground">Drive B Connected!</h1>
            {email && (
              <p className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-1 text-sm font-medium text-emerald-400">
                {email}
              </p>
            )}
            <p className="text-sm text-muted-foreground">
              Your secondary Google Drive account is now active in Warborn OS. Redirecting to Storage…
            </p>
          </div>
        )}

        {status === 'error' && (
          <div className="flex flex-col items-center gap-4">
            <XCircle className="h-12 w-12 text-destructive" />
            <h1 className="text-xl font-semibold text-foreground">Connection Failed</h1>
            <p className="text-sm text-destructive font-medium bg-destructive/10 rounded-lg px-4 py-2 border border-destructive/20">
              {errorMsg}
            </p>
            <button
              onClick={() => router.push('/storage')}
              className="mt-2 rounded-lg bg-primary px-6 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90 transition-all"
            >
              Back to Storage
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default function GoogleDriveBCallback() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen flex-col items-center justify-center p-6 text-center bg-background">
        <Loader2 className="h-10 w-10 animate-spin text-blue-400" />
      </div>
    }>
      <GoogleDriveBCallbackContent />
    </Suspense>
  );
}
