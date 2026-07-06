---
title: "WeddingClient: Curation Agency Platform"
tagline: "A premium responsive wedding curation portal built with smooth Lenis scrolls and GSAP timelines."
status: "complete"
featured: false
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["nextjs", "typescript", "gsap", "framer-motion", "lenis"]
category: "tool"
liveUrl: "https://weddingclient-steel.vercel.app/"
githubUrl: "https://github.com/buildwithpnj/weddingclient"
startDate: "2026-04-10"
publishDate: "2026-04-30"
timeline: ["Sprint 1: Page scroll interactions & Lenis mapping", "Sprint 2: Form validator & client layout", "Sprint 3: Mobile responsiveness pass"]
challenges:
  - title: "Animation Stuttering"
    content: "Concurrent Framer Motion and GSAP page slide animations clashed, causing frame drops on mobile. Fixed by standardizing Lenis smooth-scroll triggers and offloading canvas layers."
---

## Problem
Luxury curation and photography agencies need immersive visual storytelling layouts that maintain smooth, high-fps performance on both modern desktop displays and mobile viewports.

## Solution
We engineered a high-performance portfolio page featuring:
- **GSAP Scroll-Triggered Timelines**: Smooth parallax transitions mapping text content over high-definition photos.
- **Lenis Smooth Scroll**: Eliminates browser default scroll-jumping, providing inertia-based scrolling.
- **Radix UI Accordions & Dialogs**: Light and fully accessible UI overlays.
