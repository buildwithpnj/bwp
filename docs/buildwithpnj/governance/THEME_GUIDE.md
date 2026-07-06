# Theme Guide (THEME_GUIDE.md)

This document describes the unified theme provider setup, local CSS variables mappings, and light/dark theme variables for the **BuildWithPNJ** brand website and the **Warborn OS** dashboard.

---

## 1. Unified ThemeProvider Configurations
We use `next-themes` to provide a single, global theme context across the entire route directory (both public marketing pages and authenticated workspace panels).

```typescript
import { ThemeProvider } from 'next-themes';

export default function Providers({ children }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
      {children}
    </ThemeProvider>
  );
}
```

---

## 2. CSS Variables Mapping Schema

Define variables inside `globals.css` using custom HSL colors:

```css
@layer base {
  :root {
    /* Light Mode Variables */
    --background: 210 20% 98%;
    --surface: 210 20% 95%;
    --text-primary: 222 47% 11%;
    --text-muted: 215 16% 47%;
    --border: 214 32% 91%;
    --accent: 221 83% 53%; /* Electric Blue */
  }

  .dark {
    /* Dark Mode Variables */
    --background: 230 63% 5%; /* #050816 */
    --surface: 222 47% 11%;     /* #0F172A */
    --text-primary: 210 40% 96%; /* #F1F5F9 */
    --text-muted: 215 16% 62%;   /* #8E9CAE */
    --border: 217 33% 17%;       /* #1E293B */
    --accent: 221 83% 53%;       /* Electric Blue */
  }
}
```

By mapping Tailwind classes directly to these variables (e.g. `bg-[hsl(var(--background))]`), we ensure pages automatically adapt when the theme changes.
