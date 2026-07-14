'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { useKeyboardShortcuts } from '@/hooks/use-keyboard-shortcuts';
import { Sidebar, useSidebarStore } from '@/components/sidebar';
import { Header } from '@/components/header';
import { CommandPalette } from '@/components/command-palette';
import { ShortcutCheatsheet } from '@/components/shortcut-cheatsheet';
import { QuickCapture } from '@/components/quick-capture';
import { UploadCenter } from '@/components/upload-center';
import { useUploadCenter } from '@/hooks/use-upload-center';
import { cn } from '@/lib/utils';
import { GlobalCopilotShell } from '@/components/copilot/GlobalCopilotShell';
import { OperatingThreadBar } from '@/components/threads/OperatingThreadBar';

export function AppLayoutClient({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { isAuthenticated, isLoading, fetchUser } = useAuth();
  const { collapsed } = useSidebarStore();
  const { addFiles } = useUploadCenter();

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // Register global keyboard shortcuts
  useKeyboardShortcuts((path) => router.push(path));

  // Global Drag & Drop Listener
  useEffect(() => {
    const handleDragOver = (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
    };

    const handleDrop = (e: DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      if (e.dataTransfer && e.dataTransfer.files.length > 0) {
        const filesArray = Array.from(e.dataTransfer.files);
        addFiles(filesArray);
      }
    };

    window.addEventListener('dragover', handleDragOver);
    window.addEventListener('drop', handleDrop);

    return () => {
      window.removeEventListener('dragover', handleDragOver);
      window.removeEventListener('drop', handleDrop);
    };
  }, [addFiles]);

  // Auth guard
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="flex min-h-[100vh] items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-3 animate-fade-in">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-muted-foreground border-t-primary" />
          <p className="text-sm text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background pb-6">
      <Sidebar />
      <div
        className={cn(
          'transition-all duration-200',
          collapsed ? 'ml-14' : 'ml-52'
        )}
      >
        <Header />
        <OperatingThreadBar />
        <main className="p-4 pb-12">{children}</main>
      </div>

      {/* Telemetry Gutter */}
      <footer className="fixed bottom-0 left-0 right-0 z-20 h-6 border-t border-border bg-card flex items-center px-4 font-mono text-[11px] text-muted-foreground justify-between">
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse" />
            DB_SYNC: OK
          </span>
          <span className="opacity-30">|</span>
          <span>LLM_LATENCY: 120ms</span>
          <span className="opacity-30">|</span>
          <span>API_STATUS: ACTIVE</span>
        </div>
        <div className="flex items-center gap-3">
          <span>GIT: MAIN</span>
          <span className="opacity-30">|</span>
          <span>ENV: DEV_COCKPIT</span>
        </div>
      </footer>

      {/* Overlays */}
      <CommandPalette />
      <ShortcutCheatsheet />
      <QuickCapture />
      <UploadCenter />
      <GlobalCopilotShell />
    </div>
  );
}
