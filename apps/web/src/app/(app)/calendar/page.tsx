'use client';

import { useState, useEffect } from 'react';
import {
  Calendar as CalendarIcon,
  Clock,
  Plus,
  Trash2,
  Loader2,
  X,
  ChevronLeft,
  ChevronRight,
  Globe
} from 'lucide-react';
import { api } from '@/lib/api';

interface CalendarEvent {
  id: string;
  google_event_id?: string;
  title: string;
  description?: string;
  start_time: string;
  end_time: string;
  timezone?: string;
}

export default function CalendarPage() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);

  // Month navigation state
  const [currentDate, setCurrentDate] = useState(new Date());

  // Event modal states
  const [showModal, setShowModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newStart, setNewStart] = useState('');
  const [newEnd, setNewEnd] = useState('');
  const [newTimezone, setNewTimezone] = useState('UTC');
  const [saving, setSaving] = useState(false);

  const loadEvents = async () => {
    setLoading(true);
    try {
      const data = await api<CalendarEvent[]>('/api/gcalendar/events');
      setEvents(data || []);
    } catch (err) {
      console.error('Failed to load calendar events:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  const handleCreateEvent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newStart || !newEnd) return;

    setSaving(true);
    try {
      await api('/api/gcalendar/events', {
        method: 'POST',
        body: {
          title: newTitle,
          description: newDesc,
          start_time: new Date(newStart).toISOString(),
          end_time: new Date(newEnd).toISOString(),
          timezone: newTimezone,
        },
      });
      setShowModal(false);
      setNewTitle('');
      setNewDesc('');
      setNewStart('');
      setNewEnd('');
      await loadEvents();
    } catch (err) {
      alert('Failed to save calendar event.');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteEvent = async (id: string) => {
    if (confirm('Are you sure you want to delete this event?')) {
      try {
        await api(`/api/gcalendar/events/${id}`, { method: 'DELETE' });
        await loadEvents();
      } catch (err) {
        alert('Failed to delete event.');
        console.error(err);
      }
    }
  };

  // Get start day of month and number of days
  const getMonthDetails = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDay = new Date(year, month, 1).getDay();
    const numDays = new Date(year, month + 1, 0).getDate();
    return { firstDay, numDays };
  };

  const { firstDay, numDays } = getMonthDetails();
  const daysArray = Array.from({ length: numDays }, (_, i) => i + 1);

  // Month navigation helpers
  const prevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };
  const nextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const getEventsForDay = (dayNum: number) => {
    return events.filter((e) => {
      const eDate = new Date(e.start_time);
      return (
        eDate.getDate() === dayNum &&
        eDate.getMonth() === currentDate.getMonth() &&
        eDate.getFullYear() === currentDate.getFullYear()
      );
    });
  };

  const formatTime = (isoString: string) => {
    const d = new Date(isoString);
    return d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', hour12: false });
  };

  return (
    <div className="flex flex-col gap-6 p-6 animate-fade-in text-foreground h-[calc(100vh-80px)] overflow-hidden">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Timeline Engine</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <CalendarIcon className="h-7 w-7 text-primary" />
            Calendar & Synchronizations
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Bi-directional calendar synchronization tracking system tasks, time blocking, and events.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="rounded-lg bg-primary hover:bg-primary/90 px-4 py-2 text-xs font-semibold text-primary-foreground flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <Plus className="h-3.5 w-3.5" /> Block Time
        </button>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
        {/* Calendar visualizer month grid */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 lg:col-span-2 flex flex-col overflow-hidden h-full">
          <div className="flex items-center justify-between text-xs font-semibold pb-4 flex-shrink-0">
            <h3 className="font-mono text-sm uppercase tracking-wider text-foreground">
              {currentDate.toLocaleString(undefined, { month: 'long', year: 'numeric' })}
            </h3>
            <div className="flex items-center gap-2">
              <button
                onClick={prevMonth}
                className="p-1 border border-border rounded hover:bg-muted transition-all"
              >
                <ChevronLeft className="h-3.5 w-3.5" />
              </button>
              <button
                onClick={nextMonth}
                className="p-1 border border-border rounded hover:bg-muted transition-all"
              >
                <ChevronRight className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-7 gap-1 text-center text-3xs font-mono font-bold text-muted-foreground pb-2 border-b border-border/40 flex-shrink-0">
            <span>SUN</span>
            <span>MON</span>
            <span>TUE</span>
            <span>WED</span>
            <span>THU</span>
            <span>FRI</span>
            <span>SAT</span>
          </div>

          <div className="grid grid-cols-7 gap-1.5 text-xs font-mono flex-1 overflow-y-auto pt-2">
            {/* Blank leading days */}
            {Array.from({ length: firstDay }).map((_, i) => (
              <span key={`blank-${i}`} className="opacity-0 py-2"></span>
            ))}

            {daysArray.map((day) => {
              const dayEvents = getEventsForDay(day);
              const isToday =
                day === new Date().getDate() &&
                currentDate.getMonth() === new Date().getMonth() &&
                currentDate.getFullYear() === new Date().getFullYear();

              return (
                <div
                  key={day}
                  className={`min-h-[70px] p-1.5 rounded-lg border text-left flex flex-col justify-between transition-all ${
                    isToday
                      ? 'bg-primary/10 border-primary shadow-[0_0_8px_rgba(59,130,246,0.1)]'
                      : 'border-border/60 hover:border-primary/20 bg-muted/5'
                  }`}
                >
                  <span className={`text-2xs font-bold ${isToday ? 'text-primary' : 'text-muted-foreground'}`}>
                    {day}
                  </span>

                  {/* Day Events list */}
                  <div className="flex-1 space-y-1 mt-1 overflow-y-auto max-h-[60px]">
                    {dayEvents.slice(0, 3).map((e) => (
                      <div
                        key={e.id}
                        className="px-1.5 py-0.5 rounded text-[8px] bg-primary/20 border border-primary/20 text-foreground truncate"
                        title={e.title}
                      >
                        {e.title}
                      </div>
                    ))}
                    {dayEvents.length > 3 && (
                      <span className="text-[7px] text-muted-foreground font-mono block">
                        +{dayEvents.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Schedule timeline lists */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 flex flex-col overflow-hidden h-full">
          <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2 pb-3 border-b border-border flex-shrink-0">
            <Clock className="h-4 w-4 text-primary" />
            Schedules Registry
          </h3>

          <div className="flex-1 overflow-y-auto space-y-3 py-4 pr-1">
            {loading ? (
              <div className="py-12 flex flex-col items-center justify-center gap-2 text-muted-foreground">
                <Loader2 className="h-5 w-5 animate-spin text-primary" />
                <span className="text-2xs">Checking schedule registries...</span>
              </div>
            ) : events.length === 0 ? (
              <p className="text-xs text-muted-foreground italic text-center py-8">No scheduled logs registered.</p>
            ) : (
              <div className="space-y-3 font-mono">
                {events.map((evt) => (
                  <div
                    key={evt.id}
                    className="p-3.5 rounded-xl border border-border bg-muted/20 hover:border-primary/20 transition-all flex flex-col justify-between gap-2 group"
                  >
                    <div className="flex justify-between items-start gap-2">
                      <div className="min-w-0">
                        <span className="text-2xs font-bold text-primary flex items-center gap-1">
                          <Globe className="h-3 w-3" />
                          {formatTime(evt.start_time)} - {formatTime(evt.end_time)}
                        </span>
                        <h4 className="font-semibold text-xs text-foreground truncate mt-1">{evt.title}</h4>
                        {evt.description && (
                          <p className="text-[10px] text-muted-foreground mt-1 truncate">{evt.description}</p>
                        )}
                      </div>
                      <button
                        onClick={() => handleDeleteEvent(evt.id)}
                        className="p-1 text-muted-foreground hover:text-destructive transition-colors opacity-0 group-hover:opacity-100"
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Block Time Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
          <div className="w-full max-w-md rounded-2xl border border-border bg-card/90 backdrop-blur-md p-6 shadow-2xl overflow-hidden">
            <div className="flex justify-between items-center pb-3 border-b border-border">
              <h3 className="text-sm font-bold text-foreground flex items-center gap-2">
                <CalendarIcon className="h-4.5 w-4.5 text-primary" /> Create Time Block event
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className="p-1 text-muted-foreground hover:text-foreground transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            <form onSubmit={handleCreateEvent} className="mt-4 space-y-4">
              <input
                type="text"
                placeholder="Event summary..."
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                required
                className="w-full rounded-md border border-border bg-background px-3 py-1.5 text-xs outline-none focus:border-primary text-foreground"
              />

              <textarea
                placeholder="Description details..."
                value={newDesc}
                onChange={(e) => setNewDesc(e.target.value)}
                className="w-full h-16 bg-background border border-border rounded-lg p-2.5 text-xs outline-none focus:border-primary text-foreground resize-none"
              />

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="flex flex-col gap-1">
                  <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Start Time</span>
                  <input
                    type="datetime-local"
                    value={newStart}
                    onChange={(e) => setNewStart(e.target.value)}
                    required
                    className="rounded border border-border bg-background px-2.5 py-1 text-xs text-foreground focus:outline-none"
                  />
                </div>

                <div className="flex flex-col gap-1">
                  <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">End Time</span>
                  <input
                    type="datetime-local"
                    value={newEnd}
                    onChange={(e) => setNewEnd(e.target.value)}
                    required
                    className="rounded border border-border bg-background px-2.5 py-1 text-xs text-foreground focus:outline-none"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-1 text-xs">
                <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Timezone</span>
                <select
                  value={newTimezone}
                  onChange={(e) => setNewTimezone(e.target.value)}
                  className="rounded border border-border bg-background px-2.5 py-1 text-xs text-foreground focus:outline-none"
                >
                  <option value="UTC">UTC</option>
                  <option value="Asia/Kolkata">Asia/Kolkata</option>
                  <option value="America/New_York">America/New_York</option>
                  <option value="Europe/London">Europe/London</option>
                </select>
              </div>

              <div className="flex justify-end gap-2 text-xs font-semibold mt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/95 transition-colors flex items-center gap-1.5"
                >
                  {saving && <Loader2 className="h-3 w-3 animate-spin" />}
                  Save Event
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
