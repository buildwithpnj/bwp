# Iconography Guide (ICON_GUIDE.md)

This document defines the guidelines, stroke widths, alignments, and source configurations for the **BuildWithPNJ** brand icon system.

---

## 1. Icon Style Constraints
- **Format**: Vector-only format (using `lucide-react` library).
- **Style**: Minimal, technical line drawings.
- **Stroke Width**: Standardized on **`1.5px`** to maintain a crisp look across different resolutions.
- **Sizing**: Use a unified layout container:
  - `w-4 h-4` (16px) for inline text badges.
  - `w-5 h-5` (20px) for utility buttons and menu links.
  - `w-6 h-6` (24px) for status indicators.

---

## 2. Shared Icon Mappings

| Feature Area | Icon Component | Stroke | Rationale |
| :--- | :--- | :--- | :--- |
| **System Terminal** | `Terminal` | 1.5px | Technical presentation terminal. |
| **Notes Subsystem** | `FileText` | 1.5px | Classic file representation. |
| **Habits Checklist** | `CheckSquare` | 1.5px | Task check-offs. |
| **Finance Ledgers** | `CreditCard` | 1.5px | Transaction summaries. |
| **Storage Uploads** | `UploadCloud` | 1.5px | Cloud directories. |
| **Automation Crons** | `Cpu` | 1.5px | Background systems processing. |

---

## 3. Layout Best Practices
- Icons must always be centered inside their flex containers (`items-center justify-center`).
- Colors must be inherited from the parent text color (`stroke-current`) to ensure clean theme support.
- Avoid using filled, solid icons unless highlighting active or selected states.
