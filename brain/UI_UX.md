# UI/UX Specifications

## BuildWithPNJ Design Language

The visual layer of Warborn OS uses the BuildWithPNJ design language. It focuses on premium, grid-aligned, typography-driven operating system experiences.

### 1. Color Palette
- **Primary Accent**: Engineering Red (`#E5484D`)
- **Secondary Accent**: Electric Blue (`#3B82F6`)
- **Backgrounds**: High-contrast, theme-responsive backdrops (light blueprint elements on white glass for light mode, dark graphite layers on navy glass for dark mode).

### 2. Spacing & Blueprint Grid
- All animated elements (packet traces, square pixels background rain, snapping structures) are snapped to a unified **32px blueprint grid system**.
- Sidebar controls, cards, and modal components align precisely with grid spacing.

### 3. V2 Navigation Sidebar
- Located on the left side with a responsive collapsing toggle state.
- Integrated keyboard sequence routing allows navigating anywhere within 2 keystrokes.

### 4. Cockpit Dashboards
- **Mission Control**: Aggregates today's checklists, calendars, recovery progress, and AI coaching summaries.
- **Quit Addiction**: Combines counting timers, reclaimed indicators, and relapse logs.
- **Apple Books Shelf**: Organizes media and books as shelves.

### 5. Telemetry & Composition Refinement
- **Parallel Grid Nodes**: Telemetry nodes in the footer are aligned in parallel rows at `yPct: 25` (top row) and `yPct: 75` (bottom row), resolving crossing lines.
- **Compositor Compositing**: Replaced circles with sharp pixel squares for the packet head, trail, status indicator, and collection ripples.
- **Self-Clearing Traces**: Node highlights turn red on collection and fade back to grey after exactly 1.5 seconds.
- **Regional Timezone Clocks**: Automatically detects client location to display regional clock widgets and local currencies.

