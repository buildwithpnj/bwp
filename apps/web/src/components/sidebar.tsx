'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Terminal,
  StickyNote,
  BookOpen,
  Briefcase,
  BookMarked,
  Image,
  Film,
  HardDrive,
  Calendar,
  Cpu,
  Settings,
  Trash2,
  ChevronLeft,
  ChevronRight,
  Target,
  Flame,
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { create } from 'zustand';

interface SidebarState {
  collapsed: boolean;
  toggle: () => void;
}

export const useSidebarStore = create<SidebarState>((set) => ({
  collapsed: false,
  toggle: () => set((s) => ({ collapsed: !s.collapsed })),
}));

const navItems = [
  { href: '/dashboard', label: 'Mission Control', icon: LayoutDashboard, shortcut: 'G M' },
  { href: '/workspace', label: 'Workspace', icon: Terminal, shortcut: 'G W' },
  { href: '/notes', label: 'Notes', icon: StickyNote, shortcut: 'G N' },
  { href: '/knowledge', label: 'Knowledge Base', icon: BookOpen, shortcut: 'G K' },
  { href: '/projects-dashboard', label: 'Projects', icon: Briefcase, shortcut: 'G P' },
  { href: '/books', label: 'Books', icon: BookMarked, shortcut: 'G B' },
  { href: '/assets', label: 'Assets', icon: Image, shortcut: 'G A' },
  { href: '/media', label: 'Media', icon: Film, shortcut: 'G H' },
  { href: '/storage', label: 'Storage Manager', icon: HardDrive, shortcut: 'G S' },
  { href: '/calendar', label: 'Calendar', icon: Calendar, shortcut: 'G C' },
  { href: '/habits', label: 'Habits', icon: Target, shortcut: 'G L' },
  { href: '/recovery', label: 'Quit Addiction', icon: Flame, shortcut: 'G Q' },
  { href: '/ai-memory', label: 'AI Memory', icon: Cpu, shortcut: 'G I' },
  { href: '/settings', label: 'Settings', icon: Settings, shortcut: 'G E' },
  { href: '/trash', label: 'Trash', icon: Trash2, shortcut: 'G R' },
];

export function Sidebar() {
  const pathname = usePathname();
  const { collapsed, toggle } = useSidebarStore();

  return (
    <aside
      className={cn(
        'fixed left-0 top-0 z-30 flex h-screen flex-col border-r border-border bg-card transition-all duration-200',
        collapsed ? 'w-14' : 'w-52'
      )}
      id="sidebar"
    >
      {/* Logo */}
      <div className="flex h-12 items-center border-b border-border px-3">
        {!collapsed && (
          <span className="text-sm font-semibold tracking-tight text-foreground">
            WarBorn<span className="text-primary">OS</span>
          </span>
        )}
        <button
          onClick={toggle}
          className={cn(
            'ml-auto inline-flex items-center justify-center rounded p-1 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors',
            collapsed && 'ml-0'
          )}
          aria-label="Toggle sidebar"
          id="sidebar-toggle"
        >
          {collapsed ? (
            <ChevronRight className="h-4 w-4" />
          ) : (
            <ChevronLeft className="h-4 w-4" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-2 px-2">
        {navItems.map((item) => {
          const isActive =
            item.href === '/'
              ? pathname === '/'
              : pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'group flex items-center gap-2.5 px-2.5 py-1.5 text-[13px] font-medium transition-all duration-150',
                isActive
                  ? 'bg-primary/10 text-primary border-l-2 border-primary rounded-none'
                  : 'text-muted-foreground hover:bg-accent hover:text-foreground border-l-2 border-transparent rounded-sm'
              )}
              id={`nav-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
            >
              <item.icon className="h-4 w-4 flex-shrink-0" />
              {!collapsed && (
                <>
                  <span className="flex-1">{item.label}</span>
                  <span className="kbd opacity-0 group-hover:opacity-100 transition-opacity">
                    {item.shortcut}
                  </span>
                </>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      {!collapsed && (
        <div className="border-t border-border p-3">
          <p className="text-2xs text-muted-foreground">
            <span className="kbd">?</span> Shortcuts
          </p>
        </div>
      )}
    </aside>
  );
}
