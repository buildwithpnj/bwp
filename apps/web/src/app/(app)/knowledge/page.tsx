'use client';

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { 
  BookOpen, 
  Search, 
  Compass, 
  HardDrive, 
  Star, 
  ArrowUpRight,
  FileText,
  Folder,
  Calendar,
  Clock,
  Settings,
  AlertTriangle,
  CheckCircle2,
  Copy,
  ExternalLink,
  ChevronRight,
  Code,
  Eye,
  Activity,
  ArrowUpDown,
  CornerDownRight,
  Tag
} from 'lucide-react';
import Link from 'next/link';

interface MarkdownRecord {
  title: string;
  slug: string;
  fileName: string;
  relativePath: string;
  category: string;
  content: string;
  excerpt: string;
  headings: { level: number; text: string; id: string }[];
  tags: string[];
  wordCount: number;
  readingTime: number;
  createdDate: string;
  updatedDate: string;
  status: string;
  description: string;
}

// Custom Markdown renderer that compiles common markdown elements into standard React JSX elements.
// This is used to render markdown safely and responsively on-the-fly without third-party dependencies.
function SafeMarkdownRenderer({ content }: { content: string }) {
  const parts = content.split('\n');
  const renderedElements: React.ReactNode[] = [];
  let inCodeBlock = false;
  let codeBlockLines: string[] = [];
  let codeBlockLang = '';

  for (let i = 0; i < parts.length; i++) {
    const line = parts[i];
    
    // Code block detection
    if (line.trim().startsWith('```')) {
      if (inCodeBlock) {
        inCodeBlock = false;
        renderedElements.push(
          <pre key={`code-${i}`} className="p-4 rounded-xl bg-background border border-border/60 overflow-x-auto text-xs font-mono my-3 max-h-96">
            <code className="text-primary">{codeBlockLines.join('\n')}</code>
          </pre>
        );
        codeBlockLines = [];
      } else {
        inCodeBlock = true;
        codeBlockLang = line.replace('```', '').trim();
      }
      continue;
    }

    if (inCodeBlock) {
      codeBlockLines.push(line);
      continue;
    }

    // Render horizontal rules
    if (line.trim() === '---' || line.trim() === '***') {
      renderedElements.push(<hr key={`hr-${i}`} className="border-t border-border/40 my-6" />);
      continue;
    }

    // Render Headings
    if (line.startsWith('# ')) {
      renderedElements.push(<h1 key={`h1-${i}`} className="text-xl sm:text-2xl font-black mt-6 mb-2 border-b border-border/40 pb-1 text-foreground">{line.slice(2)}</h1>);
      continue;
    }
    if (line.startsWith('## ')) {
      renderedElements.push(<h2 key={`h2-${i}`} className="text-lg sm:text-xl font-bold mt-5 mb-2 text-foreground">{line.slice(3)}</h2>);
      continue;
    }
    if (line.startsWith('### ')) {
      renderedElements.push(<h3 key={`h3-${i}`} className="text-sm sm:text-base font-bold mt-4 mb-1.5 text-foreground">{line.slice(4)}</h3>);
      continue;
    }
    if (line.startsWith('#### ')) {
      renderedElements.push(<h4 key={`h4-${i}`} className="text-xs sm:text-sm font-bold mt-3 mb-1 text-foreground">{line.slice(5)}</h4>);
      continue;
    }

    // Render Blockquotes
    if (line.startsWith('> ')) {
      renderedElements.push(
        <blockquote key={`bq-${i}`} className="border-l-2 border-primary/50 pl-4 py-1 italic text-muted-foreground bg-secondary/15 rounded-r-lg my-2 text-xs">
          {line.slice(2)}
        </blockquote>
      );
      continue;
    }

    // Render Bullet lists
    if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
      renderedElements.push(
        <li key={`li-${i}`} className="text-xs sm:text-sm text-muted-foreground list-disc ml-5 my-1">
          {line.trim().slice(2)}
        </li>
      );
      continue;
    }

    if (line.trim() === '') {
      continue;
    }

    renderedElements.push(<p key={`p-${i}`} className="text-xs sm:text-sm text-muted-foreground leading-relaxed my-2">{line}</p>);
  }

  return <div className="space-y-1">{renderedElements}</div>;
}

export default function KnowledgeBasePage() {
  const [records, setRecords] = useState<MarkdownRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRecord, setSelectedRecord] = useState<MarkdownRecord | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedTag, setSelectedTag] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<'updated' | 'created' | 'title' | 'wordCount' | 'readingTime'>('updated');
  const [activeTab, setActiveTab] = useState<'browse' | 'health'>('browse');
  const [rawMode, setRawMode] = useState(false);

  // Clipboard copy helpers
  const [copyStatus, setCopyStatus] = useState<Record<string, boolean>>({});
  const triggerCopy = (type: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopyStatus({ ...copyStatus, [type]: true });
    setTimeout(() => {
      setCopyStatus({ ...copyStatus, [type]: false });
    }, 1500);
  };

  // Fetch all indexed markdown records on mount
  useEffect(() => {
    const fetchKnowledge = async () => {
      try {
        const res = await fetch('/api/knowledge');
        const data = await res.json();
        if (data.records) {
          setRecords(data.records);
          if (data.records.length > 0) {
            setSelectedRecord(data.records[0]);
          }
        }
      } catch (err) {
        console.error('Failed to load knowledge base indices:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchKnowledge();
  }, []);

  // Compute folder groups and counts
  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    records.forEach(r => {
      counts[r.category] = (counts[r.category] || 0) + 1;
    });
    return counts;
  }, [records]);

  // Compute tags cloud
  const tagsList = useMemo(() => {
    const allTags = new Set<string>();
    records.forEach(r => {
      r.tags.forEach(t => allTags.add(t));
    });
    return Array.from(allTags).sort();
  }, [records]);

  // Handle searching, filtering, and sorting records
  const filteredAndSortedRecords = useMemo(() => {
    let result = [...records];

    // Category / folder filter
    if (selectedCategory) {
      result = result.filter(r => r.category === selectedCategory);
    }

    // Tag filter
    if (selectedTag) {
      result = result.filter(r => r.tags.includes(selectedTag));
    }

    // Search query full-text search
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(r => {
        return (
          r.title.toLowerCase().includes(q) ||
          r.fileName.toLowerCase().includes(q) ||
          r.content.toLowerCase().includes(q) ||
          r.description.toLowerCase().includes(q) ||
          r.tags.some(t => t.toLowerCase().includes(q))
        );
      });
    }

    // Sort order
    result.sort((a, b) => {
      if (sortBy === 'updated') return b.updatedDate.localeCompare(a.updatedDate);
      if (sortBy === 'created') return b.createdDate.localeCompare(a.createdDate);
      if (sortBy === 'title') return a.title.localeCompare(b.title);
      if (sortBy === 'wordCount') return b.wordCount - a.wordCount;
      if (sortBy === 'readingTime') return b.readingTime - a.readingTime;
      return 0;
    });

    return result;
  }, [records, selectedCategory, selectedTag, searchQuery, sortBy]);

  // Related files based on tags and category matches
  const relatedRecords = useMemo(() => {
    if (!selectedRecord) return [];
    return records
      .filter(r => r.relativePath !== selectedRecord.relativePath)
      .filter(r => r.category === selectedRecord.category || r.tags.some(t => selectedRecord.tags.includes(t)))
      .slice(0, 4);
  }, [records, selectedRecord]);

  // Compile detailed Knowledge Health Diagnostics
  const healthStats = useMemo(() => {
    const totalFiles = records.length;
    const totalCategories = Object.keys(categoryCounts).length;
    const missingFrontmatter = records.filter(r => {
      // Check if file doesn't have frontmatter (e.g. category 'root' and empty summary)
      return r.category === 'root' && r.description === '';
    }).length;
    const missingTags = records.filter(r => r.tags.length === 0).length;

    // Check duplicate titles or slugs
    const titles = new Set<string>();
    const duplicateTitles: string[] = [];
    const slugs = new Set<string>();
    const duplicateSlugs: string[] = [];

    records.forEach(r => {
      if (titles.has(r.title)) duplicateTitles.push(r.title);
      else titles.add(r.title);

      if (slugs.has(r.slug)) duplicateSlugs.push(r.slug);
      else slugs.add(r.slug);
    });

    const emptyOrVeryShort = records.filter(r => r.wordCount < 10).length;

    // Stale check (not updated in 30 days)
    const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
    const staleFiles = records.filter(r => {
      const updatedTime = new Date(r.updatedDate).getTime();
      return updatedTime < thirtyDaysAgo;
    }).length;

    // Broken links scanner
    let brokenLinksCount = 0;
    records.forEach(r => {
      // Find matches like [Text](relativepath.md)
      const linkRegex = /\[[^\]]+\]\(([^)]+\.md)\)/g;
      let match;
      while ((match = linkRegex.exec(r.content)) !== null) {
        const linkPath = match[1];
        // Convert to absolute-like relative path matching record paths
        const linkMatches = records.some(rec => rec.relativePath.endsWith(linkPath) || rec.fileName === linkPath);
        if (!linkMatches) brokenLinksCount++;
      }
    });

    return {
      totalFiles,
      totalCategories,
      missingFrontmatter,
      missingTags,
      duplicateTitles: duplicateTitles.length,
      duplicateSlugs: duplicateSlugs.length,
      emptyOrVeryShort,
      staleFiles,
      brokenLinksCount
    };
  }, [records, categoryCounts]);

  return (
    <div className="space-y-6 animate-fade-in text-foreground">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Internal System docs</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <BookOpen className="h-7 w-7 text-primary" />
            Knowledge Base
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Structured information, technical documentation wikis, guides, and vectorized reference logs.
          </p>
        </div>

        {/* Tab Selector */}
        <div className="flex bg-secondary/60 border border-border/50 rounded-xl p-1 font-mono text-[10px]">
          <button 
            onClick={() => setActiveTab('browse')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${activeTab === 'browse' ? 'bg-background font-bold text-primary shadow' : 'text-muted-foreground hover:text-foreground'}`}
          >
            <Compass className="h-3.5 w-3.5" /> BROWSE DOCUMENTS
          </button>
          <button 
            onClick={() => setActiveTab('health')}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg transition-all ${activeTab === 'health' ? 'bg-background font-bold text-primary shadow' : 'text-muted-foreground hover:text-foreground'}`}
          >
            <Activity className="h-3.5 w-3.5" /> KNOWLEDGE HEALTH
          </button>
        </div>
      </div>

      {loading ? (
        <div className="h-96 rounded-2xl border border-border/80 bg-card/25 flex flex-col items-center justify-center gap-3">
          <div className="h-8 w-8 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
          <span className="font-mono text-xs text-muted-foreground uppercase tracking-widest">Scanning local documents...</span>
        </div>
      ) : activeTab === 'health' ? (
        /* KNOWLEDGE HEALTH VIEW */
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Main Health Board Card */}
          <div className="md:col-span-2 rounded-2xl border border-border bg-card/35 p-6 space-y-6">
            <div>
              <h3 className="text-sm font-bold text-foreground">Knowledge Base Quality Report</h3>
              <p className="text-xs text-muted-foreground mt-0.5">Auto-diagnosed structural metadata patterns across local directories.</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-left font-mono">
              <div className="p-4 rounded-xl border border-border/40 bg-secondary/10 flex flex-col gap-1">
                <span className="text-[9px] text-muted-foreground uppercase font-bold">TOTAL DOCS</span>
                <span className="text-2xl font-black text-foreground">{healthStats.totalFiles}</span>
              </div>
              <div className="p-4 rounded-xl border border-border/40 bg-secondary/10 flex flex-col gap-1">
                <span className="text-[9px] text-muted-foreground uppercase font-bold">CATEGORIES</span>
                <span className="text-2xl font-black text-foreground">{healthStats.totalCategories}</span>
              </div>
              <div className="p-4 rounded-xl border border-border/40 bg-secondary/10 flex flex-col gap-1">
                <span className="text-[9px] text-muted-foreground uppercase font-bold">STALE DOCUMENTS</span>
                <span className={`text-2xl font-black ${healthStats.staleFiles > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>{healthStats.staleFiles}</span>
              </div>
              <div className="p-4 rounded-xl border border-border/40 bg-secondary/10 flex flex-col gap-1">
                <span className="text-[9px] text-muted-foreground uppercase font-bold">MISSING FRONTMATTER</span>
                <span className={`text-2xl font-black ${healthStats.missingFrontmatter > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>{healthStats.missingFrontmatter}</span>
              </div>
              <div className="p-4 rounded-xl border border-border/40 bg-secondary/10 flex flex-col gap-1">
                <span className="text-[9px] text-muted-foreground uppercase font-bold">MISSING TAGS</span>
                <span className={`text-2xl font-black ${healthStats.missingTags > 0 ? 'text-amber-400' : 'text-emerald-400'}`}>{healthStats.missingTags}</span>
              </div>
              <div className="p-4 rounded-xl border border-border/40 bg-secondary/10 flex flex-col gap-1">
                <span className="text-[9px] text-muted-foreground uppercase font-bold">BROKEN LINKS</span>
                <span className={`text-2xl font-black ${healthStats.brokenLinksCount > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>{healthStats.brokenLinksCount}</span>
              </div>
            </div>

            {/* Diagnostic Logs */}
            <div className="space-y-3">
              <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-muted-foreground">Diagnostics Log</h4>
              <div className="rounded-xl border border-border/50 bg-secondary/20 p-4 font-mono text-[10px] space-y-2 leading-relaxed">
                {healthStats.brokenLinksCount > 0 && (
                  <div className="flex gap-2 text-rose-400 items-start">
                    <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>[WARN] Found {healthStats.brokenLinksCount} broken internal markdown links. Verify destination file names.</span>
                  </div>
                )}
                {healthStats.staleFiles > 0 && (
                  <div className="flex gap-2 text-amber-400 items-start">
                    <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>[INFO] {healthStats.staleFiles} documentation files have not been updated in 30 days. Recommend review.</span>
                  </div>
                )}
                {healthStats.duplicateTitles > 0 && (
                  <div className="flex gap-2 text-rose-400 items-start">
                    <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>[WARN] Detected {healthStats.duplicateTitles} duplicate document titles. Slugs may collide in page renderers.</span>
                  </div>
                )}
                {healthStats.duplicateSlugs > 0 && (
                  <div className="flex gap-2 text-rose-400 items-start">
                    <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>[WARN] Detected {healthStats.duplicateSlugs} duplicate slugs. Static page generators might overwrite content.</span>
                  </div>
                )}
                {healthStats.missingFrontmatter > 0 && (
                  <div className="flex gap-2 text-amber-400 items-start">
                    <AlertTriangle className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>[INFO] {healthStats.missingFrontmatter} markdown files have missing or empty frontmatter tables.</span>
                  </div>
                )}
                {healthStats.brokenLinksCount === 0 && healthStats.duplicateSlugs === 0 && healthStats.duplicateTitles === 0 && (
                  <div className="flex gap-2 text-emerald-400 items-start">
                    <CheckCircle2 className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                    <span>[OK] All internal file link paths and slug indices are 100% healthy.</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Directory Summary Sidebar */}
          <div className="rounded-2xl border border-border bg-card/35 p-6 flex flex-col gap-6">
            <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Directory Mapping</h3>
            <div className="space-y-3 font-mono text-[10px] text-muted-foreground">
              {Object.entries(categoryCounts).map(([cat, count], idx) => (
                <div key={idx} className="flex justify-between border-b border-border/40 pb-2">
                  <span className="flex items-center gap-1.5">
                    <Folder className="h-3.5 w-3.5 text-primary" /> {cat}
                  </span>
                  <span className="text-foreground font-black">{count} file(s)</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      ) : (
        /* MAIN BROWSE VIEW */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* 1. LEFT SIDEBAR */}
          <div className="lg:col-span-3 flex flex-col gap-4">
            {/* Category / Folder list */}
            <div className="rounded-2xl border border-border/60 bg-card/30 p-4 space-y-3 text-left">
              <span className="text-3xs font-mono font-bold uppercase tracking-widest text-muted-foreground">{"// DIRECTORIES"}</span>
              <div className="space-y-1 font-mono text-xs">
                <button
                  onClick={() => setSelectedCategory(null)}
                  className={`w-full text-left px-2 py-1.5 rounded-lg flex items-center justify-between transition-colors ${selectedCategory === null ? 'bg-secondary text-primary font-bold' : 'text-muted-foreground hover:bg-secondary/25'}`}
                >
                  <span className="truncate flex items-center gap-1.5"><Compass className="h-3.5 w-3.5" /> All folders</span>
                  <span>{records.length}</span>
                </button>
                {Object.entries(categoryCounts).map(([cat, count], idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setSelectedCategory(cat);
                      setSelectedTag(null); // Reset tag filter on category select
                    }}
                    className={`w-full text-left px-2 py-1.5 rounded-lg flex items-center justify-between transition-colors ${selectedCategory === cat ? 'bg-secondary text-primary font-bold' : 'text-muted-foreground hover:bg-secondary/25'}`}
                  >
                    <span className="truncate flex items-center gap-1.5"><Folder className="h-3.5 w-3.5" /> {cat}</span>
                    <span>{count}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Tags Cloud Panel */}
            {tagsList.length > 0 && (
              <div className="rounded-2xl border border-border/60 bg-card/30 p-4 space-y-3 text-left">
                <span className="text-3xs font-mono font-bold uppercase tracking-widest text-muted-foreground">{"// TAG METADATA"}</span>
                <div className="flex flex-wrap gap-1.5">
                  <button
                    onClick={() => setSelectedTag(null)}
                    className={`text-[9px] font-mono px-2 py-0.5 rounded transition-all ${selectedTag === null ? 'bg-primary text-primary-foreground font-black' : 'bg-secondary text-muted-foreground border border-border/40'}`}
                  >
                    All Tags
                  </button>
                  {tagsList.map((tag, idx) => (
                    <button
                      key={idx}
                      onClick={() => {
                        setSelectedTag(tag);
                        setSelectedCategory(null); // Reset category filter on tag select
                      }}
                      className={`text-[9px] font-mono px-2 py-0.5 rounded transition-all flex items-center gap-1 ${selectedTag === tag ? 'bg-primary text-primary-foreground font-black' : 'bg-secondary text-muted-foreground border border-border/40'}`}
                    >
                      <Tag className="h-2 w-2" /> {tag}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* 2. MAIN LIST PANEL */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            {/* Search and Sort controls */}
            <div className="p-4 border border-border/80 rounded-2xl bg-card/35 flex flex-col gap-3">
              <div className="relative">
                <Search className="absolute left-3.5 top-3 h-4 w-4 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search file name, outline headings, tags..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full h-10 pl-10 pr-4 rounded-xl border border-border/40 bg-background/50 focus:border-primary/50 focus:outline-none text-xs transition-colors"
                />
              </div>

              {/* Sort selector */}
              <div className="flex items-center justify-between text-[10px] font-mono text-muted-foreground border-t border-border/40 pt-3">
                <span className="uppercase text-[8px] tracking-wider">SORT DOCS BY:</span>
                <div className="flex gap-2">
                  {[
                    { id: 'updated', label: 'Updated' },
                    { id: 'created', label: 'Created' },
                    { id: 'title', label: 'Title' },
                    { id: 'wordCount', label: 'Words' }
                  ].map((opt) => (
                    <button
                      key={opt.id}
                      onClick={() => setSortBy(opt.id as any)}
                      className={`px-2 py-0.5 rounded border transition-colors ${sortBy === opt.id ? 'border-primary/40 bg-primary/5 text-primary font-bold' : 'border-transparent hover:text-foreground'}`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* List Results */}
            <div className="space-y-3">
              {filteredAndSortedRecords.length === 0 ? (
                <div className="h-64 rounded-2xl border border-border bg-card/10 flex flex-col items-center justify-center p-6 text-center gap-1">
                  <span className="text-sm font-bold text-foreground font-mono">No Matching Documents</span>
                  <span className="text-xs text-muted-foreground max-w-xs leading-relaxed">Modify your category filters or search inputs.</span>
                </div>
              ) : (
                filteredAndSortedRecords.map((r, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setSelectedRecord(r);
                      setRawMode(false);
                    }}
                    className={`w-full text-left p-4 rounded-2xl border transition-all flex flex-col gap-2 relative group shadow-sm ${selectedRecord?.relativePath === r.relativePath ? 'border-primary bg-secondary/30' : 'border-border/60 bg-card/20 hover:border-primary/20 hover:bg-secondary/10'}`}
                  >
                    {/* Header line */}
                    <div className="flex justify-between items-start gap-3">
                      <h4 className="text-xs font-bold text-foreground group-hover:text-primary transition-colors line-clamp-1">
                        {r.title}
                      </h4>
                      <span className="text-[8px] font-mono shrink-0 px-1.5 py-0.5 rounded bg-secondary/80 text-muted-foreground border border-border/40">
                        {r.category}
                      </span>
                    </div>

                    {/* Excerpt */}
                    {r.excerpt && (
                      <p className="text-[10px] text-muted-foreground line-clamp-2 leading-relaxed">
                        {r.excerpt}
                      </p>
                    )}

                    {/* Footer stats */}
                    <div className="flex items-center justify-between text-[8px] font-mono text-muted-foreground border-t border-border/20 pt-2 mt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3 w-3 text-primary/60" /> {r.readingTime} min ({r.wordCount} words)
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="h-3 w-3 text-primary/60" /> {r.updatedDate}
                      </span>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>

          {/* 3. RIGHT PREVIEW / DETAIL PANEL */}
          <div className="lg:col-span-4 rounded-2xl border border-border bg-card/35 p-5 flex flex-col gap-6 text-left shadow-lg shadow-black/5 sticky top-6 max-h-[85vh] overflow-y-auto">
            {selectedRecord ? (
              <>
                {/* Header title */}
                <div className="flex flex-col gap-2 border-b border-border/40 pb-4">
                  <div className="flex justify-between items-center gap-4">
                    <span className="text-3xs font-mono font-bold uppercase tracking-widest text-primary">{"// DOCUMENT PREVIEW"}</span>
                    
                    {/* Raw vs Render Toggle */}
                    <button
                      onClick={() => setRawMode(!rawMode)}
                      className="flex items-center gap-1 px-2.5 py-1 rounded bg-secondary/80 border border-border/60 hover:bg-accent text-muted-foreground hover:text-foreground font-mono text-[9px] transition-colors"
                    >
                      {rawMode ? <Eye className="h-3 w-3" /> : <Code className="h-3 w-3" />}
                      {rawMode ? 'PREVIEW RENDER' : 'RAW MARKDOWN'}
                    </button>
                  </div>

                  <h2 className="text-base font-black text-foreground mt-2 leading-tight">
                    {selectedRecord.title}
                  </h2>

                  {/* Metadata line */}
                  <div className="flex flex-wrap gap-1.5 font-mono text-[9px] text-muted-foreground mt-1">
                    <span className="flex items-center gap-1">
                      <Folder className="h-3 w-3 text-primary/60" /> {selectedRecord.category}
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3 text-primary/60" /> {selectedRecord.wordCount} words
                    </span>
                  </div>
                </div>

                {/* Path copy parameters */}
                <div className="p-3 rounded-xl border border-border/50 bg-secondary/15 font-mono text-[9px] space-y-2 text-muted-foreground">
                  <div className="flex justify-between items-center gap-3">
                    <span className="truncate">Path: {selectedRecord.relativePath}</span>
                    <button
                      onClick={() => triggerCopy('path', selectedRecord.relativePath)}
                      className="text-primary hover:underline font-bold shrink-0"
                    >
                      {copyStatus['path'] ? 'Copied' : 'Copy'}
                    </button>
                  </div>
                  <div className="flex justify-between items-center gap-3">
                    <span className="truncate">Slug: {selectedRecord.slug}</span>
                    <button
                      onClick={() => triggerCopy('slug', selectedRecord.slug)}
                      className="text-primary hover:underline font-bold shrink-0"
                    >
                      {copyStatus['slug'] ? 'Copied' : 'Copy'}
                    </button>
                  </div>
                </div>

                {/* Table of contents (Headings outline list) */}
                {selectedRecord.headings.length > 0 && (
                  <div className="space-y-2.5 border-b border-border/40 pb-4">
                    <span className="text-3xs font-mono font-bold uppercase tracking-widest text-muted-foreground block">{"// TABLE OF CONTENTS"}</span>
                    <div className="space-y-1 text-[10px] font-mono max-h-36 overflow-y-auto">
                      {selectedRecord.headings.map((h, hidx) => (
                        <div
                          key={hidx}
                          className="flex items-center gap-1.5 text-muted-foreground hover:text-primary transition-colors cursor-pointer"
                          style={{ paddingLeft: `${(h.level - 1) * 8}px` }}
                        >
                          <CornerDownRight className="h-3 w-3 text-primary/40 shrink-0" />
                          <span className="truncate">{h.text}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Main Content Render Panel */}
                <div className="flex-1 min-h-[250px] overflow-y-auto border-b border-border/40 pb-6 pr-1">
                  {rawMode ? (
                    <textarea
                      readOnly
                      value={selectedRecord.content}
                      className="w-full h-80 p-3 rounded-xl border border-border/40 bg-background/50 focus:outline-none text-[10px] font-mono leading-relaxed resize-none"
                    />
                  ) : (
                    <SafeMarkdownRenderer content={selectedRecord.content} />
                  )}
                </div>

                {/* Related files list */}
                {relatedRecords.length > 0 && (
                  <div className="space-y-3">
                    <span className="text-3xs font-mono font-bold uppercase tracking-widest text-muted-foreground block">{"// RELATED SYSTEM DOCUMENTS"}</span>
                    <div className="space-y-2 font-mono text-[9px]">
                      {relatedRecords.map((rel, rIdx) => (
                        <button
                          key={rIdx}
                          onClick={() => {
                            setSelectedRecord(rel);
                            setRawMode(false);
                          }}
                          className="w-full p-2.5 rounded-lg border border-border/40 bg-secondary/10 hover:border-primary/20 hover:bg-secondary/20 flex justify-between items-center gap-3 text-left text-muted-foreground hover:text-foreground transition-all"
                        >
                          <span className="truncate font-semibold">{rel.title}</span>
                          <ChevronRight className="h-3.5 w-3.5 shrink-0 text-primary/60" />
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="h-96 flex flex-col items-center justify-center text-center p-6 gap-2">
                <span className="text-sm font-bold font-mono text-muted-foreground uppercase tracking-wider">No Selected Document</span>
                <span className="text-xs text-muted-foreground">Select a file from the list explorer to view details.</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
