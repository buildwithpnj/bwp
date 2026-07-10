'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import {
  BookOpen,
  Search,
  Plus,
  Trash2,
  Star,
  Bookmark,
  BookMarked,
  Tag,
  Loader2,
  CheckCircle,
  AlertCircle,
  Clock,
  Filter,
  X,
  FileText
} from 'lucide-react';
import { api } from '@/lib/api';

interface Highlight {
  id: string;
  book_id: string;
  text: string;
  location?: string;
  tags?: string;
  created_at: string;
}

interface Book {
  id: string;
  title: string;
  author: string;
  status: 'to-read' | 'reading' | 'finished' | 'DNF';
  rating?: number | null;
  cover_url?: string | null;
  created_at: string;
  updated_at: string;
}

interface BookDetail extends Book {
  highlights: Highlight[];
}

export default function BooksPage() {
  const [books, setBooks] = useState<Book[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [selectedBookId, setSelectedBookId] = useState<string | null>(null);
  const [bookDetail, setBookDetail] = useState<BookDetail | null>(null);
  const [loadingList, setLoadingList] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);
  const [showDrawer, setShowDrawer] = useState(false);

  // Book Edit States
  const [editTitle, setEditTitle] = useState('');
  const [editAuthor, setEditAuthor] = useState('');
  const [editStatus, setEditStatus] = useState<'to-read' | 'reading' | 'finished' | 'DNF'>('to-read');
  const [editRating, setEditRating] = useState<number | null>(null);
  const [editCoverUrl, setEditCoverUrl] = useState('');
  const [saveStatus, setSaveStatus] = useState<'saved' | 'saving' | 'error' | null>(null);

  // New Highlight States
  const [newHlText, setNewHlText] = useState('');
  const [newHlLocation, setNewHlLocation] = useState('');
  const [newHlTags, setNewHlTags] = useState('');
  const [addingHl, setAddingHl] = useState(false);

  const isFirstLoad = useRef(true);

  // Load books
  const loadBooks = useCallback(async (selectId: string | null = null, showLoader = true) => {
    if (showLoader) setLoadingList(true);
    try {
      const endpoint = searchQuery
        ? `/api/books?q=${encodeURIComponent(searchQuery)}`
        : '/api/books';
      const data = await api<Book[]>(endpoint);
      setBooks(data || []);

      if (data && data.length > 0 && !selectedBookId && !selectId) {
        // do not auto-select if we want clean state
      } else if (selectId) {
        setSelectedBookId(selectId);
      }
    } catch (error) {
      console.error('Failed to load books:', error);
    } finally {
      if (showLoader) setLoadingList(false);
    }
  }, [searchQuery, selectedBookId]);

  useEffect(() => {
    loadBooks();
  }, [searchQuery, loadBooks]);

  // Load details
  const loadBookDetail = useCallback(async (id: string) => {
    setLoadingDetail(true);
    isFirstLoad.current = true;
    setSaveStatus(null);
    try {
      const data = await api<BookDetail>(`/api/books/${id}`);
      setBookDetail(data);
      setEditTitle(data.title || '');
      setEditAuthor(data.author || '');
      setEditStatus(data.status || 'to-read');
      setEditRating(data.rating || null);
      setEditCoverUrl(data.cover_url || '');
    } catch (error) {
      console.error('Failed to load book details:', error);
    } finally {
      setLoadingDetail(false);
    }
  }, []);

  useEffect(() => {
    if (selectedBookId) {
      loadBookDetail(selectedBookId);
    } else {
      setBookDetail(null);
    }
  }, [selectedBookId, loadBookDetail]);

  // Auto-save details
  useEffect(() => {
    if (!selectedBookId) return;
    if (isFirstLoad.current) {
      isFirstLoad.current = false;
      return;
    }

    setSaveStatus('saving');
    const timer = setTimeout(async () => {
      try {
        await api(`/api/books/${selectedBookId}`, {
          method: 'PUT',
          body: {
            title: editTitle || 'Untitled Book',
            author: editAuthor || 'Unknown Author',
            status: editStatus,
            rating: editRating,
            cover_url: editCoverUrl || null,
          },
        });
        setSaveStatus('saved');
        loadBooks(selectedBookId, false);
      } catch (error) {
        console.error('Auto-save failed:', error);
        setSaveStatus('error');
      }
    }, 850);

    return () => clearTimeout(timer);
  }, [editTitle, editAuthor, editStatus, editRating, editCoverUrl, selectedBookId, loadBooks]);

  const handleCreateBook = async () => {
    try {
      const newBook = await api<Book>('/api/books', {
        method: 'POST',
        body: {
          title: 'New Book',
          author: 'Unknown Author',
          status: 'to-read',
        },
      });
      await loadBooks(newBook.id);
      setSelectedBookId(newBook.id);
      setShowDrawer(true);
    } catch (error) {
      alert('Failed to create book');
      console.error(error);
    }
  };

  const handleDeleteBook = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (confirm('Are you sure you want to delete this book?')) {
      try {
        await api(`/api/books/${id}`, { method: 'DELETE' });
        if (selectedBookId === id) {
          setSelectedBookId(null);
          setShowDrawer(false);
        }
        await loadBooks();
      } catch (error) {
        alert('Failed to delete book');
        console.error(error);
      }
    }
  };

  const handleAddHighlight = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBookId || !newHlText.trim()) return;

    setAddingHl(true);
    try {
      await api(`/api/books/${selectedBookId}/highlights`, {
        method: 'POST',
        body: {
          text: newHlText,
          location: newHlLocation || null,
          tags: newHlTags || null,
        },
      });
      setNewHlText('');
      setNewHlLocation('');
      setNewHlTags('');
      await loadBookDetail(selectedBookId);
    } catch (error) {
      alert('Failed to save highlight.');
      console.error(error);
    } finally {
      setAddingHl(false);
    }
  };

  const handleDeleteHighlight = async (hlId: string) => {
    if (confirm('Delete this highlight?')) {
      try {
        await api(`/api/books/highlights/${hlId}`, { method: 'DELETE' });
        if (selectedBookId) await loadBookDetail(selectedBookId);
      } catch (error) {
        alert('Failed to delete highlight.');
        console.error(error);
      }
    }
  };

  const filteredBooks = books.filter((book) => {
    if (statusFilter !== 'all' && book.status !== statusFilter) return false;
    return true;
  });

  return (
    <div className="flex flex-col gap-6 p-6 animate-fade-in text-foreground h-[calc(100vh-80px)] overflow-hidden relative">
      {/* ─── SYSTEM HEADER ────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Library Catalog</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <BookOpen className="h-7 w-7 text-primary animate-pulse" />
            Book Shelf
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Organize personal reading lists, cover visuals, annotations, and highlights.
          </p>
        </div>

        {/* Search & Actions */}
        <div className="flex flex-wrap items-center gap-3">
          <div className="relative w-full sm:w-60">
            <input
              type="text"
              placeholder="Search library..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-md border border-border bg-background py-1.5 pl-8 pr-3 text-xs outline-none focus:border-primary text-foreground"
            />
            <Search className="absolute left-2.5 top-2.5 h-3.5 w-3.5 text-muted-foreground" />
          </div>

          <button
            onClick={handleCreateBook}
            className="rounded-lg bg-primary hover:bg-primary/90 px-4 py-2 text-xs font-semibold text-primary-foreground flex items-center gap-1.5 transition-colors"
          >
            <Plus className="h-3.5 w-3.5" />
            New Book
          </button>
        </div>
      </div>

      {/* ─── FILTER CONTROLS ──────────────────────────────────── */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-border/60">
        <Filter className="h-3.5 w-3.5 text-muted-foreground flex-shrink-0" />
        {[
          { id: 'all', label: 'All Books' },
          { id: 'reading', label: 'Reading' },
          { id: 'to-read', label: 'To Read' },
          { id: 'finished', label: 'Finished' },
          { id: 'DNF', label: 'DNF' },
        ].map((btn) => (
          <button
            key={btn.id}
            onClick={() => setStatusFilter(btn.id)}
            className={`rounded px-3 py-1 text-2xs font-semibold transition-all flex-shrink-0 ${
              statusFilter === btn.id
                ? 'bg-primary/10 text-primary border border-primary/20'
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            {btn.label}
          </button>
        ))}
      </div>

      {/* ─── BOOKSHELF SHELVES GRID ───────────────────────────── */}
      <div className="flex-1 overflow-y-auto pr-2 pb-12">
        {loadingList && books.length === 0 ? (
          <div className="flex h-[40vh] items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
          </div>
        ) : filteredBooks.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 text-center text-muted-foreground">
            <BookOpen className="h-12 w-12 mb-3 text-muted-foreground/35" />
            <p className="text-sm font-semibold">Bookshelf empty</p>
            <p className="text-xs mt-1">Try creating a new book or adjusting filters.</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-x-6 gap-y-12">
            {filteredBooks.map((book) => (
              <div
                key={book.id}
                onClick={() => {
                  setSelectedBookId(book.id);
                  setShowDrawer(true);
                }}
                className="group relative cursor-pointer flex flex-col items-center text-center space-y-3"
              >
                {/* Book Jacket Visualizer */}
                <div className="relative w-32 h-44 bg-muted border border-border rounded-lg shadow-md overflow-hidden flex items-center justify-center group-hover:scale-105 group-hover:-translate-y-1 transition-all duration-300">
                  {book.cover_url ? (
                    <img src={book.cover_url} alt="" className="w-full h-full object-cover" />
                  ) : (
                    <div className="flex flex-col items-center justify-center p-3 text-muted-foreground/40">
                      <BookOpen className="h-8 w-8 mb-1.5" />
                      <span className="text-3xs font-mono font-bold leading-tight line-clamp-3 px-1">{book.title}</span>
                    </div>
                  )}

                  {/* Bookmark symbol */}
                  {book.status === 'reading' && (
                    <div className="absolute top-0 right-3 w-3 h-5 bg-amber-500 rounded-b-sm shadow-sm" />
                  )}
                  {book.status === 'finished' && (
                    <div className="absolute top-0 right-3 w-3 h-5 bg-emerald-500 rounded-b-sm shadow-sm" />
                  )}
                </div>

                {/* Info */}
                <div className="w-full px-1">
                  <h3 className="text-xs font-bold truncate text-foreground group-hover:text-primary transition-colors">
                    {book.title || 'Untitled Book'}
                  </h3>
                  <p className="text-3xs text-muted-foreground mt-0.5 truncate">{book.author || 'Unknown Author'}</p>
                </div>

                {/* Rating / Actions Overlay */}
                <button
                  onClick={(e) => handleDeleteBook(book.id, e)}
                  className="absolute -top-2 -right-2 opacity-0 group-hover:opacity-100 p-1.5 rounded-full bg-card border border-border text-muted-foreground hover:text-destructive shadow-sm hover:scale-110 transition-all z-10"
                >
                  <Trash2 className="h-3 w-3" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ─── SLIDE DRAWER DETAIL PANEL ───────────────────────── */}
      {showDrawer && bookDetail && (
        <div className="absolute inset-y-0 right-0 z-40 w-full sm:w-[480px] bg-card/95 border-l border-border shadow-2xl backdrop-blur-md flex flex-col animate-slide-in">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-border px-6 py-4 bg-muted/40">
            <h2 className="text-sm font-bold uppercase tracking-wider text-foreground flex items-center gap-1.5">
              <Bookmark className="h-4 w-4 text-primary" />
              Book Annotations
            </h2>
            <button
              onClick={() => {
                setShowDrawer(false);
                setSelectedBookId(null);
              }}
              className="p-1 rounded hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
            >
              <X className="h-4.5 w-4.5" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {/* Book Meta Grid */}
            <div className="flex gap-4">
              <div className="w-20 h-28 bg-muted border border-border rounded shadow-sm overflow-hidden flex-shrink-0 flex items-center justify-center">
                {editCoverUrl ? (
                  <img src={editCoverUrl} alt="" className="w-full h-full object-cover" />
                ) : (
                  <BookOpen className="h-6 w-6 text-muted-foreground/30" />
                )}
              </div>
              <div className="flex-1 flex flex-col gap-2 min-w-0">
                <input
                  type="text"
                  placeholder="Book Title..."
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  className="w-full text-sm font-bold bg-transparent border-none outline-none text-foreground focus:ring-0"
                />
                <input
                  type="text"
                  placeholder="Author..."
                  value={editAuthor}
                  onChange={(e) => setEditAuthor(e.target.value)}
                  className="w-full text-xs bg-transparent border-none outline-none text-muted-foreground focus:ring-0"
                />
                <input
                  type="text"
                  placeholder="Cover Image URL..."
                  value={editCoverUrl}
                  onChange={(e) => setEditCoverUrl(e.target.value)}
                  className="w-full border-b border-border text-3xs font-mono py-0.5 outline-none focus:border-primary text-foreground bg-transparent"
                />
              </div>
            </div>

            {/* Status & Rating dropdowns */}
            <div className="grid grid-cols-2 gap-3 text-xs bg-muted/20 border border-border rounded-xl p-3">
              <div className="flex flex-col gap-1">
                <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Status</span>
                <select
                  value={editStatus}
                  onChange={(e) => setEditStatus(e.target.value as any)}
                  className="rounded border border-border bg-background px-2.5 py-1 text-xs text-foreground focus:border-primary focus:outline-none"
                >
                  <option value="to-read">To Read</option>
                  <option value="reading">Reading</option>
                  <option value="finished">Finished</option>
                  <option value="DNF">DNF</option>
                </select>
              </div>

              <div className="flex flex-col gap-1">
                <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Rating</span>
                <select
                  value={editRating || ''}
                  onChange={(e) => setEditRating(e.target.value ? parseInt(e.target.value) : null)}
                  className="rounded border border-border bg-background px-2.5 py-1 text-xs text-foreground focus:border-primary focus:outline-none"
                >
                  <option value="">Unrated</option>
                  <option value="5">5 Stars</option>
                  <option value="4">4 Stars</option>
                  <option value="3">3 Stars</option>
                  <option value="2">2 Stars</option>
                  <option value="1">1 Star</option>
                </select>
              </div>
            </div>

            {/* Highlights Catalog */}
            <div className="space-y-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                <BookMarked className="h-4 w-4 text-primary" />
                Highlights ({bookDetail.highlights?.length || 0})
              </h3>

              <div className="space-y-3">
                {bookDetail.highlights?.length === 0 ? (
                  <p className="text-center text-xs text-muted-foreground py-6 italic border border-dashed border-border rounded-xl">
                    No highlights added yet.
                  </p>
                ) : (
                  bookDetail.highlights.map((hl) => (
                    <div key={hl.id} className="p-3 border border-border bg-card/45 rounded-xl flex gap-3 text-left">
                      <div className="flex-1 space-y-1.5">
                        <p className="text-[13px] leading-relaxed text-foreground italic font-serif">
                          &quot;{hl.text}&quot;
                        </p>
                        <div className="flex items-center gap-2 text-3xs text-muted-foreground font-mono">
                          {hl.location && (
                            <span className="text-primary font-bold">Loc: {hl.location}</span>
                          )}
                          <span>{new Date(hl.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDeleteHighlight(hl.id)}
                        className="p-1 rounded hover:bg-destructive/15 text-muted-foreground hover:text-destructive flex-shrink-0 self-start"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Add annotation input */}
          <form onSubmit={handleAddHighlight} className="p-4 border-t border-border bg-muted/30 flex flex-col gap-2">
            <textarea
              placeholder="Paste highlight from book..."
              value={newHlText}
              onChange={(e) => setNewHlText(e.target.value)}
              className="w-full rounded-md border border-border bg-background p-2 text-xs outline-none focus:border-primary text-foreground resize-none h-14"
              required
            />
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Loc (e.g. 12%)"
                value={newHlLocation}
                onChange={(e) => setNewHlLocation(e.target.value)}
                className="flex-1 rounded-md border border-border bg-background px-2.5 py-1 text-xs outline-none focus:border-primary text-foreground"
              />
              <button
                type="submit"
                disabled={addingHl}
                className="rounded-md bg-primary hover:bg-primary/95 text-primary-foreground font-semibold px-4 text-xs inline-flex items-center gap-1"
              >
                {addingHl ? (
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                ) : (
                  <Plus className="h-3.5 w-3.5" />
                )}
                Save Highlight
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
