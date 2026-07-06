---
id: "EXP-08"
title: "CSS Glow Effects & Hardware Acceleration"
tagline: "Measuring page load and scroll delays across different rendering properties."
status: "completed"
category: "Design Experiments"
tags: ["css", "performance", "design-system"]
hypothesis: "Utilizing hardware-accelerated transforms instead of standard box-shadow properties reduces render latency."
publishDate: "2026-07-08"
---

## Objective
To build high-performance glowing cards and UI grids without introducing layout shifts or frame drops.

## Methodology
- Test two approaches for container glow animations:
  1. Traditional `box-shadow` transitions.
  2. Hardware-accelerated `opacity` transforms on pseudo-elements.
- Monitor rendering performance and frame rates during page scroll.

## Findings
- Box-shadow transitions caused significant frame drops on mobile devices.
- Pseudo-element transforms maintained a smooth **60 FPS** scroll rate.
