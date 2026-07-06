# Homepage Optimization Plan (HOMEPAGE_OPTIMIZATION.md)

This document provides optimization recommendations for the landing layout, video pre-loading, scroll rhythm, and CTA paths of the **BuildWithPNJ** brand.

---

## 1. Hero Video Optimization
- **Asset**: A 24-second looping background video.
- **Optimization**:
  - Compress the video file to under 2MB.
  - Implement lazy loading or trigger the video payload only after the main page mounts.
  - Set a fallback background color `#050816` to ensure a clean visual experience while the video loads.

---

## 2. Scroll Rhythm & Visual Gaps
- Use generous vertical spacing (`py-24` or `py-32`) to establish a premium feel.
- Clean up borders between layout blocks to improve visual flow.
- Balance the distribution of text blocks and visual elements to guide the user's attention.

---

## 3. Telemetry Integration
- **Aesthetic**: Technical presentation terminal (`Terminal.tsx`) active in the Hero or Mission Control segment.
- **Optimization**:
  - Cache live database statistics and GitHub commit history.
  - Limit the frequency of data fetches (e.g. cache queries for 1 hour) to ensure fast initial page loads.
  - Wrap terminal rendering logic inside React Server Components where possible to minimize client-side bundle size.
