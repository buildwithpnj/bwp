---
title: "PricePilot: E-Commerce Price Intelligence"
tagline: "A Python system analyzing market pricing deltas and automating inventory rule updates."
status: "complete"
featured: true
thumbnail: "/images/projects/placeholder.jpg"
techStack: ["python", "pandas", "numpy", "scraper"]
category: "tool"
githubUrl: "https://github.com/buildwithpnj/pricepilot"
startDate: "2026-04-25"
publishDate: "2026-05-12"
timeline: ["Sprint 1: Competitor price aggregator scripts", "Sprint 2: Elastic pricing formulas & webhook actions"]
challenges:
  - title: "Anti-Scraping Mitigations"
    content: "Frequent product catalog sweeps triggered strict cloudflare captcha pages. We solved this by using proxy rotators, mimicking browser footprints, and spreading cycles."
---

## Problem
E-commerce brands lose revenue by failing to react in real-time to competitor price drops or stock depletion, resulting in either uncompetitive pricing or missed premium margins.

## Solution
We built **PricePilot**, an automated rule-based SKU manager that scrapes pricing indices, models pricing elasticity based on current inventory, and triggers inventory system webhooks to adjust active prices dynamically.

## Tech Details
- **Python Pandas & Numpy**: Used for data preparation, normalization, and outlier detection.
- **BeautifulSoup & Playwright**: Direct page parsers extracting catalog listings.
