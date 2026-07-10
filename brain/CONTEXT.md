# Context & Branding Guidelines

This document details the visual and core branding rules for the BuildWithPNJ operating system dashboard.

## Unified Brand Palette

Strictly adhere to the following color palette to maintain consistency across the entire website:

- **Primary Accent**: Engineering Red (`#E5484D`)
  * Hex: `#E5484D`
  * HSL: `358 76% 59%`
  * Use: Primary status signals, active navigation links, branding marks, and highlighted terminal outputs.
- **Secondary Accent**: Electric Blue (`#3B82F6`)
  * Hex: `#3B82F6`
  * HSL: `217 91% 60%`
  * Use: Subsystem traces, PCB pulse animations, hover highlights, and alternate status signals.
- **Base Neutrals**:
  * **White**: `#FFFFFF` / `hsl(0 0% 100%)` (Clear text and main buttons).
  * **Graphite**: `hsl(240 3.7% 15.9%)` (Inner borders, muted separators, dark cards).
  * **Dark Navy**: `#0A0F1D` (Core glass backdrops, dark gradients).

Do not introduce any extraneous colors.

## Typography

Maintain consistency using the existing typeface configurations:

- **Brand / Logo**: Pixel Font (`font-pixel`), tracking-widest.
- **Technical/Telemetry Logs**: Geist Mono (`font-mono`), lowercase tracking-wider, uppercase tracking-widest.
- **Headings & Body Copy**: Geist Sans (`font-sans`), clean letter-spacing and sharp contrast values.

## Grid & Alignment Rules

- All circuit backgrounds and line paths MUST snap to the **32px blueprint grid system**.
- Symmetrical packet lines must always align horizontally.
- Layout vertical margins (`leftTrunkX` and `rightTrunkX`) are calculated relative to viewport constraints (`width > 1280px ? (width - 1280)/2 : width * 0.08`) to ensure background elements never bleed over the main grid layout.

## Symmetrical Telemetry Layout & Pixel Composites

- **Nodes Parallelism**: Telemetry ribbon nodes must always align horizontally at flat Y coordinates (e.g. `yPct: 25` and `yPct: 75` in SVG layouts), avoiding wavy loops or crossings.
- **Pixel Consistency**: All dynamic elements — including the uvicorn online indicator, SVG data packet headers, collision pulses, and trailing dots — must be rendered as sharp square shapes (rectangles/squares with `rx="0"` or `rounded-sm`) to match the pixel-art design system. Circular visualizers are prohibited.
- **Automatic Fade-Outs**: Visual node collection signals must automatically fade out back to grey after exactly 1.5 seconds.

