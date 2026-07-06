---
title: "Acreages: Real Estate Showcase"
tagline: "Premium real estate portal featuring touch swipes and a local AI chatbot reading custom parsed .docx data."
status: "complete"
featured: true
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["html5", "css3", "javascript", "vite", "python"]
category: "experiment"
liveUrl: "https://realestatedemo-five.vercel.app/"
githubUrl: "https://github.com/buildwithpnj/realestatedemo"
startDate: "2026-04-20"
publishDate: "2026-05-04"
timeline: ["Sprint 1: Landing page layout & tabbed sliders", "Sprint 2: Word document parser script", "Sprint 3: Client-side chatbot search & local storage logs"]
challenges:
  - title: "Local Knowledge Base Scrapes"
    content: "Building an agent capable of recommending villas from official brochures without cloud AI APIs. Solved by writing a Python script to parse .docx profiles into a structured knowledge base, loaded as local client JSON."
  - title: "Responsive Slider Jitters"
    content: "Tabbed sliders experienced page layout shifts on dynamic screens. Solved by implementing touch-swipe event handlers and standardizing layout aspect bounds."
---

## Problem
E-commerce and real estate portfolios often struggle to display complex villa specifications, while users get frustrated with slow form submissions and unresponsive image carousels.

## Solution
We built the **Acreages Real Estate Showcase**:
- **Acreages Assistant**: A floating client-side chatbot running search algorithms over a compiled local JSON knowledge base. The knowledge base is generated from raw project Word documents using `/scripts/build-chatbot-kb.py`.
- **Swipe-Ready Slider**: Autoplays every 5.2s, pauses on hover, and supports touch swiping.
- **Offline Lead Engine**: Saves callback requests, villa preferences, and NRI user queries directly into the client's localStorage log files.
