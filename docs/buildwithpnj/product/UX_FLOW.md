# BuildWithPNJ — UX Flow

> User journey maps and interaction flows for the BuildWithPNJ website.
> Every flow is designed to move visitors toward a conversion goal.

---

## 1. Core User Flows

### 1.1 Flow A — First-Time Visitor (Social Media → Explore)

The most common entry path: someone clicks a link from Twitter/X or LinkedIn.

```mermaid
graph TD
    A["🐦 Social Media Post"] --> B["🏠 Landing Page"]
    B --> C{"What catches their eye?"}
    C -->|Projects| D["📂 Projects Page"]
    C -->|Blog headline| E["📝 Blog Listing"]
    C -->|Curious about PNJ| F["👤 About Page"]

    D --> G["📋 Project Detail"]
    G --> H{"Impressed?"}
    H -->|Yes| I["⭐ Star on GitHub"]
    H -->|Yes| J["📬 Subscribe Newsletter"]
    H -->|Read more| E

    E --> K["📄 Blog Post"]
    K --> L{"Enjoyed it?"}
    L -->|Yes| M["📄 Related Post"]
    L -->|Yes| J
    L -->|Share| N["🔗 Share on Social"]

    F --> D
    F --> O["📧 Contact Page"]

    style A fill:#6366F1,color:#fff
    style J fill:#22C55E,color:#fff
    style I fill:#22C55E,color:#fff
    style N fill:#22C55E,color:#fff
```

**Conversion goals:** ⭐ GitHub star, 📬 Newsletter signup, 🔗 Social share

**Key design decisions:**
- Hero must communicate value in < 5 seconds
- Every page has a clear next action (never a dead end)
- Featured content is curated, not just chronological

---

### 1.2 Flow B — Hiring Manager (LinkedIn → Evaluate)

A recruiter or engineering manager evaluating PNJ's technical skills.

```mermaid
graph TD
    A["💼 LinkedIn Profile"] --> B["🏠 Landing Page"]
    B --> C["📂 Projects Page"]
    C --> D["📋 Project Detail: Personal OS"]

    D --> E{"Evaluating..."}
    E -->|Check code| F["🔗 GitHub Repo"]
    E -->|Read process| G["📝 Related Blog Post"]
    E -->|Learn more| H["👤 About Page"]

    G --> D
    H --> I["📧 Contact Page"]

    F --> J{"Impressed by code quality?"}
    J -->|Yes| I
    J -->|Yes| K["📩 Send Email / Schedule Call"]

    style A fill:#3B82F6,color:#fff
    style K fill:#22C55E,color:#fff
    style I fill:#22C55E,color:#fff
```

**Conversion goal:** 📩 Contact / reach out for opportunity

**Key design decisions:**
- Projects page is the centerpiece for this persona
- Every project page links to GitHub and has architecture detail
- About page positions PNJ as a senior-level thinker

---

### 1.3 Flow C — Fellow Builder (GitHub → Connect)

A developer discovers PNJ through GitHub or a technical blog post.

```mermaid
graph TD
    A["🐙 GitHub Repo"] --> B["📄 README"]
    B --> C{"Likes the project?"}
    C -->|Yes| D["⭐ Star Repo"]
    C -->|Curious| E["🔗 Website Link in README"]

    E --> F["🏠 Landing Page"]
    F --> G["📝 Blog"]
    G --> H["📄 Technical Blog Post"]

    H --> I{"Wants to connect?"}
    I -->|Yes| J["🐦 Follow on Twitter/X"]
    I -->|Yes| K["📧 Contact Page"]
    I -->|Keep reading| L["📄 Another Post"]

    D --> E

    style A fill:#8B5CF6,color:#fff
    style D fill:#22C55E,color:#fff
    style J fill:#22C55E,color:#fff
    style K fill:#22C55E,color:#fff
```

**Conversion goals:** ⭐ Star, 🐦 Social follow, 📧 Contact for collab

---

### 1.4 Flow D — Blog Reader (Search → Subscribe)

Organic traffic from Google landing on a specific blog post.

```mermaid
graph TD
    A["🔍 Google Search"] --> B["📄 Blog Post"]
    B --> C{"Content quality?"}
    C -->|Great| D["📄 Related Posts"]
    C -->|Great| E["📬 Newsletter CTA"]
    C -->|Meh| F["← Back to Google"]

    D --> G["📄 Another Blog Post"]
    G --> E
    G --> H["📂 Projects"]
    E --> I["✅ Subscribed!"]

    H --> J["📋 Project Detail"]
    J --> K["🐙 GitHub"]

    style A fill:#F59E0B,color:#000
    style I fill:#22C55E,color:#fff
    style F fill:#EF4444,color:#fff
```

**Conversion goal:** 📬 Newsletter subscription

**Key design decisions:**
- Blog posts must stand alone (no context required)
- Related posts keep readers on-site
- Newsletter CTA appears mid-post AND at bottom

---

## 2. Micro-Interactions

### 2.1 Page Load Sequence

```
T+0ms    ── Page shell renders (layout, nav, footer)
T+100ms  ── Hero background animation starts
T+200ms  ── Headline fades in from bottom
T+350ms  ── Subheadline fades in
T+500ms  ── CTA buttons fade in with subtle scale
T+700ms  ── Below-fold content begins loading
```

### 2.2 Scroll Interactions

| Trigger | Animation | Element |
|---|---|---|
| Section enters viewport | Fade up + slide (20px) | Section headings |
| Card enters viewport | Stagger fade-in (100ms delay each) | Project/blog cards |
| 50% scroll depth | Subtle parallax | Hero background |
| Scroll past hero | Nav background becomes solid | Navigation bar |
| Scroll to bottom | Newsletter CTA pulses once | Footer CTA |

### 2.3 Hover & Click States

| Element | Hover | Active/Click |
|---|---|---|
| **Project card** | Scale 1.02, border glow (indigo), shadow lift | Scale 0.98, navigate |
| **Blog card** | Background lighten, title color → accent | Navigate to post |
| **CTA button** | Gradient shift, subtle glow | Scale 0.95, ripple |
| **Nav link** | Underline slide in from left | Color → accent |
| **Social icon** | Scale 1.15, color → brand color | Open in new tab |
| **Code block** | Copy button appears | "Copied!" tooltip |
| **Tag pill** | Background fill | Filter by tag |

---

## 3. Key Interaction Patterns

### 3.1 Newsletter Signup Flow

```
┌────────────────────────────────────────────────────┐
│                                                    │
│  🚀 Stay in the loop                              │
│                                                    │
│  AI engineering insights, build updates,           │
│  and things I wish I knew earlier.                 │
│                                                    │
│  ┌──────────────────────────┐  ┌───────────────┐  │
│  │ your@email.com           │  │  Subscribe ▶  │  │
│  └──────────────────────────┘  └───────────────┘  │
│                                                    │
│  No spam. Unsubscribe anytime.                     │
│                                                    │
└────────────────────────────────────────────────────┘

         ↓ On submit (success)

┌────────────────────────────────────────────────────┐
│                                                    │
│  ✅ You're in!                                     │
│                                                    │
│  Check your inbox for a confirmation.              │
│  Welcome to the builder crew.                      │
│                                                    │
└────────────────────────────────────────────────────┘
```

### 3.2 Contact Form Flow

```
Step 1: Fill form
┌────────────────────────────────────┐
│  Name        [________________]   │
│  Email       [________________]   │
│  Subject     [▼ Select one    ]   │
│              ├─ Collaboration     │
│              ├─ Freelance/Hire    │
│              ├─ Question          │
│              └─ Other             │
│  Message     [                ]   │
│              [                ]   │
│              [________________]   │
│                                   │
│         [ Send Message ▶ ]        │
└────────────────────────────────────┘

Step 2: Sending
┌────────────────────────────────────┐
│        [⟳ Sending...]             │
└────────────────────────────────────┘

Step 3: Success
┌────────────────────────────────────┐
│  ✅ Message sent!                  │
│                                    │
│  I'll get back to you within       │
│  48 hours. In the meantime,        │
│  check out my latest blog post →   │
└────────────────────────────────────┘
```

### 3.3 Blog Post Reading Experience

```
┌─────────────────────────────────────────────────┐
│  [← Back to Blog]                               │
│                                                  │
│  Building a Personal OS with FastAPI             │
│  ───────────────────────────────────             │
│  Jul 4, 2026  ·  8 min read  ·  #fastapi #ai    │
│                                                  │
│  [Cover Image]                                   │
│                                                  │
│  ┌─────────────────┐                             │
│  │ TABLE OF         │  Body content...           │
│  │ CONTENTS         │                            │
│  │ ─────────────    │  ## Section Heading        │
│  │ 1. Introduction  │                            │
│  │ 2. Architecture  │  Paragraph text with       │
│  │ 3. Database  ◄── │  inline `code` and         │
│  │ 4. Learnings     │  [links](#).               │
│  └─────────────────┘                             │
│                                                  │
│  ```python                          [📋 Copy]   │
│  async def get_dashboard():                      │
│      return await db.fetch_all()                 │
│  ```                                             │
│                                                  │
│  ─────────────────────────────────────           │
│                                                  │
│  📬 Enjoyed this? Subscribe for more.            │
│  [your@email.com]  [Subscribe ▶]                 │
│                                                  │
│  ─────────────────────────────────────           │
│                                                  │
│  Related Posts                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ Post 1   │ │ Post 2   │ │ Post 3   │         │
│  └──────────┘ └──────────┘ └──────────┘         │
│                                                  │
│  [Share: 🐦 Twitter  💼 LinkedIn  🔗 Copy]       │
└─────────────────────────────────────────────────┘
```

---

## 4. Navigation Flow States

### 4.1 Active Page Indicators

| State | Visual Treatment |
|---|---|
| **Current page** | Nav link has accent underline + bold weight |
| **Hovered** | Underline slides in from left, color shift |
| **Default** | Muted text color, no underline |

### 4.2 Page Transitions

| Transition | Animation |
|---|---|
| Page → Page | Content crossfade (200ms ease-out) |
| List → Detail | Card expands into page (shared layout animation) |
| Back navigation | Reverse of entry animation |

---

## 5. Error & Empty States

| State | Content | CTA |
|---|---|---|
| **404 Page** | "Looks like this page drifted into the void." | "Go Home" / "Browse Projects" |
| **No blog posts for tag** | "No posts tagged with [tag] yet." | "View all posts" |
| **Contact form error** | "Something went wrong. Try again or email me directly." | "Retry" / email link |
| **Newsletter already subscribed** | "You're already on the list! 🎉" | "Browse the blog" |
| **Offline** | "You're offline. Some content may be cached." | None (graceful degradation) |

---

## 6. Conversion Funnel Summary

```
AWARENESS ──────► INTEREST ──────► ENGAGEMENT ──────► CONVERSION
                                                       
Social post       Hero impresses   Reads blog post    ⭐ GitHub star
Google search     Browses projects  Views project      📬 Subscribes
GitHub repo       Clicks "About"   Clicks GitHub       📧 Contacts
Referral link     Reads tagline    Shares content      🐦 Follows
                                   Returns next week   💼 Hires
```

---

*Last updated: 2026-07-04*
