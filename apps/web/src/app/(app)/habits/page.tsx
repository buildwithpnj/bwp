'use client';

import { useState, useEffect } from 'react';
import {
  Target,
  Plus,
  Trash2,
  Calendar,
  Smile,
  Frown,
  Meh,
  Loader2,
  CheckCircle,
  AlertCircle,
  Clock,
  Flame,
  Award,
  Sparkles,
  Edit3,
  BookOpen,
  Filter,
  CheckSquare
} from 'lucide-react';
import { api } from '@/lib/api';

interface HabitLog {
  date: string;
  value: number;
}

interface Habit {
  id: string;
  name: string;
  cadence: 'daily' | 'weekly' | 'monthly';
  target: number;
  difficulty?: string;
  priority?: string;
  estimated_duration?: number;
  color_theme?: string;
  notes?: string;
  category?: string;
  routine?: string;
  created_at: string;
  updated_at: string;
  logs: HabitLog[];
}

interface JournalEntry {
  id: string;
  body_json: string;
  mood: number;
  created_at: string;
}

const moodEmojis: Record<number, string> = {
  1: '😢',
  2: '😕',
  3: '😐',
  4: '🙂',
  5: '😄',
};

const moodLabels: Record<number, string> = {
  1: 'Awful',
  2: 'Bad',
  3: 'Neutral',
  4: 'Good',
  5: 'Amazing',
};

export default function HabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [journals, setJournals] = useState<JournalEntry[]>([]);
  const [selectedJournalId, setSelectedJournalId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // New Habit Modal states
  const [showModal, setShowModal] = useState(false);
  const [newName, setNewName] = useState('');
  const [newCadence, setNewCadence] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [newDifficulty, setNewDifficulty] = useState('medium');
  const [newPriority, setNewPriority] = useState('medium');
  const [newDuration, setNewDuration] = useState(15);
  const [newCategory, setNewCategory] = useState('health');
  const [newRoutine, setNewRoutine] = useState('morning');
  const [newColor, setNewColor] = useState('blue');
  const [newNotes, setNewNotes] = useState('');

  // Daily Journal editor states
  const [selectedEntry, setSelectedEntry] = useState<JournalEntry | null>(null);
  const [editMood, setEditMood] = useState<number>(3);
  const [editContent, setEditContent] = useState('');
  const [savingJournal, setSavingJournal] = useState(false);

  // Load habits and journals
  const loadData = async () => {
    setLoading(true);
    try {
      const hData = await api<Habit[]>('/api/habits');
      setHabits(hData || []);

      const jData = await api<JournalEntry[]>('/api/habits/journal/list');
      setJournals(jData || []);
      if (jData && jData.length > 0) {
        selectJournal(jData[0]);
      }
    } catch (err) {
      console.error('Failed to load Life OS data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const selectJournal = (entry: JournalEntry) => {
    setSelectedEntry(entry);
    setEditMood(entry.mood || 3);
    try {
      const parsed = JSON.parse(entry.body_json);
      setEditContent(parsed.text || '');
    } catch {
      setEditContent(entry.body_json || '');
    }
  };

  const handleCreateHabit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;

    try {
      await api('/api/habits', {
        method: 'POST',
        body: {
          name: newName,
          cadence: newCadence,
          target: 1,
          difficulty: newDifficulty,
          priority: newPriority,
          estimated_duration: newDuration,
          category: newCategory,
          routine: newRoutine,
          color_theme: newColor,
          notes: newNotes,
        },
      });
      setShowModal(false);
      setNewName('');
      setNewNotes('');
      await loadData();
    } catch (err) {
      alert('Failed to save habit.');
      console.error(err);
    }
  };

  const handleDeleteHabit = async (id: string) => {
    if (confirm('Delete this habit?')) {
      try {
        await api(`/api/habits/${id}`, { method: 'DELETE' });
        await loadData();
      } catch (err) {
        alert('Failed to delete habit.');
        console.error(err);
      }
    }
  };

  const toggleLogToday = async (habit: Habit) => {
    const todayStr = new Date().toISOString().split('T')[0];
    const logged = habit.logs?.find((l) => l.date === todayStr);

    try {
      await api(`/api/habits/${habit.id}/log`, {
        method: 'POST',
        body: {
          date: todayStr,
          value: logged ? 0.0 : 1.0,
        },
      });
      await loadData();
    } catch (err) {
      console.error('Failed to toggle log:', err);
    }
  };

  const handleCreateJournal = async () => {
    try {
      const entry = await api<JournalEntry>('/api/habits/journal', { method: 'POST' });
      await loadData();
      selectJournal(entry);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveJournal = async () => {
    if (!selectedEntry) return;
    setSavingJournal(true);
    try {
      await api(`/api/habits/journal/${selectedEntry.id}`, {
        method: 'PUT',
        body: {
          body_json: JSON.stringify({ text: editContent }),
          mood: editMood,
        },
      });
      await loadData();
    } catch (err) {
      console.error(err);
    } finally {
      setSavingJournal(false);
    }
  };

  const getStreak = (habit: Habit) => {
    if (!habit.logs || habit.logs.length === 0) return 0;
    const sorted = [...habit.logs].sort((a, b) => b.date.localeCompare(a.date));
    let streak = 0;
    let current = new Date();
    current.setHours(0, 0, 0, 0);

    for (let i = 0; i < sorted.length; i++) {
      const logDate = new Date(sorted[i].date);
      logDate.setHours(0, 0, 0, 0);
      const diff = (current.getTime() - logDate.getTime()) / 86400000;

      if (diff <= 1) {
        streak++;
        current = logDate;
      } else {
        break;
      }
    }
    return streak;
  };

  const getWeekDays = () => {
    const days = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      days.push(d);
    }
    return days;
  };
  const weekDays = getWeekDays();

  return (
    <div className="flex flex-col gap-6 p-6 animate-fade-in text-foreground h-[calc(100vh-80px)] overflow-hidden">
      {/* System Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between border border-border/80 rounded-2xl bg-card/45 p-6 grid-dots gap-4">
        <div>
          <span className="text-3xs font-bold uppercase tracking-[0.25em] text-primary">Wellbeing Engine</span>
          <h1 className="text-2xl font-bold tracking-tight mt-1 flex items-center gap-2">
            <Target className="h-7 w-7 text-primary animate-pulse" />
            Life OS Manager
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Optimize your cognitive streaks, routines, habit metrics, and daily reflections.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="rounded-lg bg-primary hover:bg-primary/90 px-4 py-2 text-xs font-semibold text-primary-foreground flex items-center gap-1.5 transition-colors self-start md:self-auto"
        >
          <Plus className="h-3.5 w-3.5" /> New Habit
        </button>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
        {/* Habits Dashboard & Routines */}
        <div className="lg:col-span-2 overflow-y-auto space-y-6 pr-2">
          {/* routines sections */}
          {['morning', 'evening', 'none'].map((routineType) => {
            const list = habits.filter((h) => (h.routine || 'none') === routineType);
            if (list.length === 0 && routineType !== 'none') return null;

            return (
              <div key={routineType} className="rounded-2xl border border-border bg-card/30 p-5 space-y-4">
                <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-2">
                  <Clock className="h-4 w-4 text-primary" />
                  {routineType === 'none' ? 'General Habits' : `${routineType} routine`}
                </h3>

                <div className="space-y-3">
                  {list.map((habit) => {
                    const streak = getStreak(habit);
                    const todayStr = new Date().toISOString().split('T')[0];
                    const completedToday = habit.logs?.some((l) => l.date === todayStr);

                    return (
                      <div
                        key={habit.id}
                        className="p-4 rounded-xl border border-border/80 bg-muted/20 hover:border-primary/20 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
                      >
                        <div className="flex items-start gap-3 min-w-0">
                          <button
                            onClick={() => toggleLogToday(habit)}
                            className={`mt-0.5 rounded border p-1 flex-shrink-0 transition-all ${
                              completedToday
                                ? 'bg-primary/10 border-primary text-primary'
                                : 'border-border text-muted-foreground hover:border-primary/50'
                            }`}
                          >
                            <CheckSquare className="h-4.5 w-4.5" />
                          </button>
                          <div className="min-w-0">
                            <span className={`text-xs font-semibold truncate block ${completedToday ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                              {habit.name}
                            </span>
                            <div className="flex items-center gap-2 mt-1.5 text-3xs text-muted-foreground font-mono">
                              <span className="capitalize">{habit.cadence}</span>
                              <span>·</span>
                              <span className="uppercase">{habit.priority} Priority</span>
                              {habit.estimated_duration && (
                                <>
                                  <span>·</span>
                                  <span>{habit.estimated_duration} mins</span>
                                </>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Right stats / streak */}
                        <div className="flex items-center justify-between sm:justify-end gap-4">
                          {streak > 0 && (
                            <span className="text-3xs font-mono font-bold text-amber-500 bg-amber-500/10 border border-amber-500/20 px-2.5 py-0.5 rounded-full flex items-center gap-1">
                              <Flame className="h-3.5 w-3.5 fill-amber-500/10" />
                              {streak} days
                            </span>
                          )}

                          <button
                            onClick={() => handleDeleteHabit(habit.id)}
                            className="p-1 text-muted-foreground hover:text-destructive rounded transition-colors opacity-0 group-hover:opacity-100"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>

        {/* Daily Journal / Reflections */}
        <div className="rounded-2xl border border-border bg-card/30 p-5 flex flex-col overflow-hidden h-full">
          <div className="flex items-center justify-between border-b border-border/80 pb-3 flex-shrink-0">
            <h3 className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
              <BookOpen className="h-4 w-4 text-primary" />
              Daily Reflections
            </h3>
            <button
              onClick={handleCreateJournal}
              className="rounded p-1 hover:bg-accent text-muted-foreground hover:text-foreground transition-colors"
              title="Add reflection log"
            >
              <Plus className="h-4 w-4" />
            </button>
          </div>

          <div className="flex-1 overflow-y-auto py-4 space-y-4">
            {journals.length === 0 ? (
              <p className="text-center text-xs text-muted-foreground py-10 italic">
                No logs recorded yet. Create a daily reflection page to track your mindfulness progress.
              </p>
            ) : (
              <div className="space-y-4">
                {/* Journal entries selector list */}
                <div className="flex gap-2 overflow-x-auto pb-2">
                  {journals.map((j) => (
                    <button
                      key={j.id}
                      onClick={() => selectJournal(j)}
                      className={`px-3 py-1.5 rounded-lg border text-xs font-semibold font-mono flex-shrink-0 transition-colors ${
                        selectedEntry?.id === j.id
                          ? 'bg-primary/10 border-primary text-primary'
                          : 'border-border text-muted-foreground hover:border-foreground'
                      }`}
                    >
                      {new Date(j.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })} {moodEmojis[j.mood || 3]}
                    </button>
                  ))}
                </div>

                {/* Editor page */}
                {selectedEntry && (
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <span className="text-3xs font-bold uppercase tracking-wider text-muted-foreground">Select Mood:</span>
                      <div className="flex justify-between gap-1.5">
                        {[1, 2, 3, 4, 5].map((m) => (
                          <button
                            key={m}
                            type="button"
                            onClick={() => setEditMood(m)}
                            className={`flex-1 py-1.5 border rounded-lg text-lg transition-all ${
                              editMood === m
                                ? 'bg-primary/10 border-primary scale-105'
                                : 'border-border bg-card/40 hover:bg-muted'
                            }`}
                            title={moodLabels[m]}
                          >
                            {moodEmojis[m]}
                          </button>
                        ))}
                      </div>
                    </div>

                    <textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      placeholder="Write your logs or mood triggers here..."
                      className="w-full h-40 bg-background border border-border rounded-xl p-3 text-xs outline-none focus:border-primary text-foreground resize-none font-mono"
                    />

                    <button
                      onClick={handleSaveJournal}
                      disabled={savingJournal}
                      className="w-full rounded-lg bg-primary hover:bg-primary/95 text-primary-foreground font-semibold py-2 text-xs transition-all flex items-center justify-center gap-1.5"
                    >
                      {savingJournal && <Loader2 className="h-3 w-3 animate-spin" />}
                      Save Log
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* New Habit Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-md rounded-2xl border border-border bg-card/90 backdrop-blur-md p-6 shadow-2xl overflow-hidden">
            <h3 className="text-sm font-bold text-foreground flex items-center gap-2 pb-3 border-b border-border">
              <Plus className="h-4.5 w-4.5 text-primary" /> Create Routine Habit
            </h3>

            <form onSubmit={handleCreateHabit} className="mt-4 space-y-4">
              <input
                type="text"
                placeholder="Habit name (e.g. 30 min cardio)"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                required
                className="w-full rounded-md border border-border bg-background px-3 py-1.5 text-xs outline-none focus:border-primary text-foreground"
              />

              <div className="grid grid-cols-2 gap-3 text-xs">
                <div className="flex flex-col gap-1">
                  <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Cadence</span>
                  <select
                    value={newCadence}
                    onChange={(e) => setNewCadence(e.target.value as any)}
                    className="rounded border border-border bg-background px-2 py-1 text-xs text-foreground focus:outline-none"
                  >
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                  </select>
                </div>

                <div className="flex flex-col gap-1">
                  <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Priority</span>
                  <select
                    value={newPriority}
                    onChange={(e) => setNewPriority(e.target.value)}
                    className="rounded border border-border bg-background px-2 py-1 text-xs text-foreground focus:outline-none"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <div className="flex flex-col gap-1">
                  <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Routine</span>
                  <select
                    value={newRoutine}
                    onChange={(e) => setNewRoutine(e.target.value)}
                    className="rounded border border-border bg-background px-2 py-1 text-xs text-foreground focus:outline-none"
                  >
                    <option value="morning">Morning Routine</option>
                    <option value="evening">Evening Routine</option>
                    <option value="none">None (General)</option>
                  </select>
                </div>

                <div className="flex flex-col gap-1">
                  <span className="text-3xs uppercase tracking-wider text-muted-foreground font-bold">Est Duration (m)</span>
                  <input
                    type="number"
                    value={newDuration}
                    onChange={(e) => setNewDuration(parseInt(e.target.value))}
                    className="rounded border border-border bg-background px-2.5 py-1 text-xs text-foreground focus:outline-none"
                  />
                </div>
              </div>

              <textarea
                placeholder="Optional notes or guidelines..."
                value={newNotes}
                onChange={(e) => setNewNotes(e.target.value)}
                className="w-full h-16 bg-background border border-border rounded-lg p-2.5 text-xs outline-none focus:border-primary text-foreground resize-none"
              />

              <div className="flex justify-end gap-2 text-xs font-semibold">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="rounded-lg border border-border px-4 py-2 text-muted-foreground hover:bg-accent transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/95 transition-colors"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
