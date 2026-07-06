# UI Consistency Report (UI_CONSISTENCY_REPORT.md)

This audit report identifies design and UI discrepancies between the public website pages and the authenticated dashboard.

---

## 1. Audit Log of Inconsistencies

1. **Typography Mismatches**:
   - *Inconsistency*: Some markdown tables and journal sidebars use non-standard system fonts.
   - *Impact*: Breaks design consistency.
   - *Fix*: Standardize on `Geist` for all text blocks, descriptions, and lists.
2. **Hardcoded Colors**:
   - *Inconsistency*: Cards in the habits and finance pages use static HEX values (`#0F172A` or `#1E293B`) instead of referencing theme CSS variables.
   - *Impact*: Stalls theme transitions when switching modes.
   - *Fix*: Refactor classes to use Tailwind's `bg-surface` and `border-border` classes.
3. **Spacing Inconsistencies**:
   - *Inconsistency*: Public marketing pages use a compact spacing scale, while dashboard panels use a wider, high-density layout.
   - *Impact*: Creates a visual disconnect when navigating.
   - *Fix*: Standardize layouts on a 32px (2rem) gutter scale.
4. **Animation Variations**:
   - *Inconsistency*: Modal palettes transition instantly, while dashboard sidebar links use linear easing.
   - *Impact*: Interaction transitions feel inconsistent.
   - *Fix*: Apply standard spring curves (`cubic-bezier(0.16, 1, 0.3, 1)`) globally.
5. **Component Duplication**:
   - *Inconsistency*: Terminals and code-blocks are defined separately in `apps/web/src/components/ui/` instead of being imported from a shared package.
   - *Impact*: Multiplies code maintenance overhead.
   - *Fix*: Migrate all shared UI elements to `packages/ui`.
