# Theme Architecture Spec (THEME_ARCHITECTURE.md)

This document outlines the context variables, global theme providers, and configuration files of the **BuildWithPNJ** design system.

---

## 1. Unified ThemeProvider Config

We configure a single theme context at the root of the React app using `next-themes`. This enables clean dark/light mode toggling across all marketing and dashboard pages:

```typescript
import { ThemeProvider } from 'next-themes';

export default function AppProvider({ children }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false}>
      {children}
    </ThemeProvider>
  );
}
```

---

## 2. Dynamic CSS Variables Schema

Colors are mapped to CSS variables using custom HSL values:

```css
@layer base {
  :root {
    --background: 210 20% 98%;
    --surface: 210 20% 95%;
    --text-primary: 222 47% 11%;
    --text-muted: 215 16% 47%;
    --border: 214 32% 91%;
    --accent: 221 83% 53%; /* Electric Blue */
  }

  .dark {
    --background: 230 63% 5%;    /* #050816 */
    --surface: 222 47% 11%;        /* #0F172A */
    --text-primary: 210 40% 96%;   /* #F1F5F9 */
    --text-muted: 215 16% 62%;     /* #8E9CAE */
    --border: 217 33% 17%;         /* #1E293B */
    --accent: 221 83% 53%;         /* Electric Blue */
  }
}
```

---

## 3. Tailwind Configuration Integration

To ensure Tailwind classes adapt dynamically to active theme changes, link the variables in `tailwind.config.ts`:

```typescript
module.exports = {
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        surface: 'hsl(var(--surface))',
        primary: 'hsl(var(--text-primary))',
        muted: 'hsl(var(--text-muted))',
        border: 'hsl(var(--border))',
      }
    }
  }
}
```
This configuration ensures that theme adjustments apply globally across the codebase automatically.
