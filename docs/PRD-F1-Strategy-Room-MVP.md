# Product Requirements Document: F1 Strategy Room MVP

## 🎯 Product Overview

**App Name:** F1 Strategy Room  
**Tagline:** Turn F1 telemetry into race-winning strategy insights—in minutes, not hours  
**Launch Goal:** Portfolio-ready demo with deployed app, hero race analysis, and backtest validation  
**Target Launch:** 1 week

---

## 👥 Who It's For

### Primary User: The Data-Driven F1 Fan

Hardcore Formula 1 enthusiasts who want to go beyond punditry and gut feelings. They care about *why* a strategy works, not just *what* happened. They're comfortable with data but don't want to maintain their own notebooks.

**Their Current Pain:**
- Spending hours wrangling FastF1 notebooks for basic insights
- YouTube strategy breakdowns are interesting but not interactive or customizable
- No easy way to generate shareable, credible visuals for race previews
- Fantasy F1 decisions feel like guesswork without accessible data

**What They Need:**
- Quick, reliable strategy recommendations with clear reasoning
- Visual outputs they can screenshot or share
- Confidence that the analysis is grounded in real telemetry

### Secondary Users

| User Type | Need | How We Help |
|-----------|------|-------------|
| Content Creators | Defensible analysis + shareable visuals for threads/videos | Export-ready charts, clear explanations |
| Fantasy F1 Players | Edge in predicting race outcomes | Strategy rankings, overtake difficulty insights |
| Aspiring Data Scientists | Learn F1 analytics patterns | Open-source, well-documented codebase |

### Example User Story

"Meet Aisha, a hardcore F1 fan who creates race-preview threads on Twitter. Every race week, she downloads session data, watches strategy breakdowns on YouTube, and sometimes opens a FastF1 notebook she found on GitHub—but it's time-consuming and inconsistent.

She finds F1 Strategy Room through a GitHub link. She selects 'Monza 2023', sets conditions to dry, and clicks Generate Strategy. The app shows tyre degradation curves, a pit window chart, and ranks strategies like M→H one-stop vs S→M→H two-stop—with a quick explanation of why the undercut matters here.

Then she opens the Overtake Map, sees the top passing zones visualized on the track, and uses that to argue: 'Track position matters—passing is concentrated into these braking zones.'

Now she's happy because she can create a data-driven preview in minutes, with visuals that look credible and a narrative she can explain."

---

## 🔧 The Problem We're Solving

**Core Problem:** F1 fans and creators who want data-backed strategy insights currently face a painful choice: spend hours in notebooks (high effort, inconsistent results) or rely on someone else's analysis (no customization, can't verify).

**Why It Matters Now:**
- F1's popularity has surged (Drive to Survive effect) → more fans want deeper analysis
- FastF1 has made telemetry accessible → but there's no good UI layer on top
- Content creation around F1 is booming → creators need faster workflows
- Fantasy F1 is growing → players want any analytical edge

**Why Existing Solutions Fall Short:**

| Solution | Problem |
|----------|---------|
| FastF1 notebooks (DIY) | High setup cost, requires Python skills, inconsistent quality |
| YouTube strategy breakdowns | Passive consumption, not interactive, can't customize for specific scenarios |
| F1 TV / official analytics | Limited depth, no strategy simulation, no "what if" scenarios |
| Paid tools (if any) | Cost barrier for hobbyists, often focused on teams not fans |

---

## 🎬 User Journey

### Discovery → First Use → Success

**1. Discovery Phase**
- **How they find us:** GitHub trending, Reddit r/F1Technical, Twitter/X F1 data community
- **What catches attention:** "Generate pit strategy recommendations from real telemetry"
- **Decision trigger:** Seeing a sample output (deg curves + strategy ranking) that looks legit

**2. Onboarding (First 2 Minutes)**
- Land on app → see clean, dark interface with race selector
- First action: Select a race (default: pre-loaded "hero race" like Monza 2023)
- Quick win: Immediately see tyre deg curves and strategy ranking without configuration

**3. Core Usage Loop**
- **Trigger:** Upcoming race weekend, want to preview strategy
- **Action:** Select circuit + conditions → generate strategy → explore overtake map
- **Reward:** Shareable insights, confidence in predictions
- **Investment:** Bookmark app, share outputs, return next race week

**4. Success Moment**
- **"Aha!" moment:** "This matches what the top teams actually did—and I can see *why*"
- **Share trigger:** Screenshot-worthy charts, clear strategy explanations

---

## ✨ MVP Features

### 🔴 Must Have for Launch (P0)

#### 1. Tyre Degradation Model + Stint Pace Curves
- **What:** Visualize how lap times degrade over a stint by compound (Soft/Medium/Hard) and conditions (dry/wet)
- **User Story:** As an F1 fan, I want to see how each tyre compound degrades so I can understand why certain strategies work better
- **Success Criteria:**
  - [ ] Shows deg curves for each compound used in selected race
  - [ ] Displays predicted lap time vs. tyre age (lap number)
  - [ ] Handles at least dry conditions reliably
  - [ ] Clearly labels compounds with F1-standard colors (red/yellow/white)
- **Priority:** P0 (Critical) — foundational for strategy simulator

#### 2. Pit Strategy Simulator
- **What:** Compare and rank pit strategies (1-stop vs 2-stop), show optimal pit windows, explain undercut/overcut value
- **User Story:** As a content creator, I want to see which strategy is fastest and why so I can make informed race previews
- **Success Criteria:**
  - [ ] Ranks at least 3 strategy options (e.g., S→H, M→H, S→M→H)
  - [ ] Shows estimated total race time for each strategy
  - [ ] Displays pit window visualization (when to pit)
  - [ ] Provides brief text explanation of recommendation
  - [ ] Accounts for pit stop time loss (circuit-specific)
- **Priority:** P0 (Critical) — core value proposition

#### 3. Circuit Overtake Opportunity Map
- **What:** Highlight top passing zones on the circuit with explanations (DRS, braking intensity, historical data)
- **User Story:** As a fantasy F1 player, I want to know where overtakes happen so I can assess track position importance
- **Success Criteria:**
  - [ ] Shows track layout with highlighted zones
  - [ ] Ranks top 3-5 overtaking spots
  - [ ] Provides brief explanation per zone (e.g., "Long DRS zone into heavy braking")
  - [ ] Works for at least 5 circuits in MVP
- **Priority:** P0 (Critical) — key differentiator

#### 4. Race/Session Selector
- **What:** Dropdown to select year, race, and session (focus on race sessions for MVP)
- **User Story:** As a user, I want to select which race to analyze so I can explore different circuits
- **Success Criteria:**
  - [ ] Lists available races from FastF1 cache
  - [ ] Pre-loads a "hero race" by default (Monza 2023 or similar)
  - [ ] Handles loading states gracefully
- **Priority:** P0 (Critical) — required for any analysis

#### 5. Backtest/Validation Display
- **What:** Show model accuracy metrics (deg prediction error, strategy accuracy vs. actual results)
- **User Story:** As a hiring manager viewing this portfolio piece, I want to see validation metrics so I trust the methodology
- **Success Criteria:**
  - [ ] Displays MAE/RMSE for degradation predictions
  - [ ] Shows strategy accuracy proxy (e.g., "matched top-3 finisher strategy X%")
  - [ ] Available for at least the hero race
- **Priority:** P0 (Critical) — required for portfolio credibility

---

### 🟡 Nice to Have (If Time Allows)
- **Scenario toggles:** Dry/wet switch, safety car probability slider
- **Export buttons:** Download charts as PNG
- **Multiple hero races:** 2-3 pre-analyzed circuits instead of 1

### 🚫 NOT in MVP (Saving for V2)

| Feature | Why Wait |
|---------|----------|
| Live race integration | Complex real-time architecture, not needed for demo |
| Full SC/VSC probabilistic modeling | Adds significant complexity; simple toggle sufficient for MVP |
| Driver-specific personalization | "Generic car" model is sufficient to demonstrate value |
| Advanced overtake localization (multi-car telemetry) | Strong proxy sufficient; full implementation is research project |
| LLM assistant / chat UI | Nice UX but not core to F1 realism |
| Accounts + saved scenarios + sharing links | Requires auth infrastructure; screenshot sharing works for MVP |
| Multi-season model retraining automation | Manual retraining fine for demo |

*Why we're waiting: Keeps MVP focused and launchable in 1 week. These features add polish but don't prove the core concept.*

---

## 📊 How We'll Know It's Working

### Launch Success Criteria (Portfolio-Ready)

| Criterion | Target | How to Verify |
|-----------|--------|---------------|
| Deployed & accessible | App loads for anyone with link | Test from incognito browser |
| Runs locally | Docker setup works | Fresh clone + `docker-compose up` succeeds |
| Hero race complete | Monza 2023 (or similar) fully analyzed | All 3 core features produce output |
| Deg model validated | MAE/RMSE displayed | Backtest page shows metrics |
| Strategy accuracy shown | Proxy metric displayed | "Matched top-3 finisher strategy X%" |
| README quality | Clear setup, screenshots, methodology | Could onboard a new dev in 10 min |
| Demo video | 2-3 min walkthrough | Recorded and linked in README |

### Stretch Goals (Nice to Have)
| Goal | Target |
|------|--------|
| External feedback | 5-10 comments from F1 Reddit/Discord |
| Social proof | 1 share/retweet from F1 content creator |

---

## 🎨 Look & Feel

**Design Vibe:** Clean, data-dense, race-engineer tool

**Visual Principles:**
1. **Dark mode by default** — matches F1 TV aesthetic, easier on eyes for data-dense screens
2. **Data density over whitespace** — race engineers pack info tight; embrace that
3. **F1-authentic colors** — use official compound colors (red/yellow/white), team colors where relevant
4. **Professional, not flashy** — this is a tool, not a game; credibility matters

**Color Palette:**
- Background: Dark gray/near-black (#1a1a1a or similar)
- Text: White/light gray
- Accents: F1 red (#e10600) for highlights
- Compounds: Soft (red), Medium (yellow), Hard (white)

**Typography:**
- Clean sans-serif (Inter, IBM Plex Sans, or system fonts)
- Monospace for data/numbers where appropriate

### Key Screens

| Screen | Purpose | Key Elements |
|--------|---------|--------------|
| **Home / Race Selector** | Entry point, select race to analyze | Race dropdown, conditions toggle, "Analyze" button |
| **Strategy Dashboard** | Core analysis view | Deg curves chart, strategy ranking table, pit window viz |
| **Overtake Map** | Passing zone analysis | Track layout SVG, ranked zones list, zone explanations |
| **Backtest / Validation** | Model credibility | Error metrics, accuracy summary, methodology notes |

### Simple Wireframe

```
┌─────────────────────────────────────────────────────────────┐
│  F1 STRATEGY ROOM                    [Race: Monza 2023 ▼]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐  ┌─────────────────────────────┐  │
│  │   TYRE DEGRADATION  │  │     STRATEGY RANKING        │  │
│  │                     │  │                             │  │
│  │   [Deg Curves       │  │  1. M→H (1-stop)   1:32:04  │  │
│  │    Chart]           │  │  2. S→M→H (2-stop) 1:32:18  │  │
│  │                     │  │  3. S→H (1-stop)   1:32:31  │  │
│  │   ● Soft ● Med ● Hd │  │                             │  │
│  └─────────────────────┘  │  WHY: Low deg favors 1-stop │  │
│                           └─────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  PIT WINDOW                          │   │
│  │  [==========|████████|=============] Lap 20-28      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [View Overtake Map]                    [View Backtest]     │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ Technical Considerations

**Platform:** Web (desktop-first, mobile-responsive nice-to-have)  
**Stack Direction:** Python-based (Streamlit recommended for speed-to-MVP)  
**Data Source:** FastF1 library → local cache  

**Performance Targets:**
- Initial load: < 5 seconds (with cached data)
- Strategy generation: < 10 seconds
- Chart rendering: < 2 seconds

**Browser Support:** Chrome, Firefox, Safari (latest versions)

**Deployment:**
- Primary: Streamlit Cloud (free tier)
- Backup: Render or Railway free tier
- Local: Docker Compose for portfolio demo

---

## 🛡️ Quality Standards

### What F1 Strategy Room Will NOT Accept

| Anti-Pattern | Why It Matters |
|--------------|----------------|
| Placeholder data ("Lorem ipsum", fake charts) | Portfolio piece must show real outputs |
| Features that half-work | Complete or cut — no broken experiences |
| Unstyled/default Streamlit look | Dark theme + F1 aesthetic required for credibility |
| Claims without caveats | Model limitations must be visible |
| Skipping the backtest display | Validation is core to portfolio value |

### Model Honesty Requirements
- Display confidence intervals or error ranges where possible
- Clearly state what the model *doesn't* account for (traffic, driver skill, setup)
- Frame recommendations as "analysis suggests" not "guaranteed optimal"

---

## 💰 Budget & Constraints

| Category | Budget | Notes |
|----------|--------|-------|
| Development tools | $0 | FastF1 (free), Python (free), Streamlit (free) |
| Hosting | $0 | Streamlit Cloud free tier |
| Data | $0 | FastF1 pulls from public F1 timing data |
| Timeline | 1 week | Aggressive but achievable with focused scope |
| Team | Solo | Using AI coding assistants (Claude, Cursor) |

---

## ❓ Open Questions & Assumptions

### Open Questions
- Which race makes the best "hero race"? (Monza 2023 has strategy variety; needs validation)
- How accurate can the deg model be with simple regression? (Will know after first implementation)
- Can overtake zones be reliably identified from position change data? (May need proxy approach)

### Key Assumptions
- FastF1 data is sufficient for MVP-quality analysis
- Users will accept "directionally correct" over "perfectly accurate"
- Dark mode + clean charts = sufficient design for portfolio credibility
- 1 hero race is enough to demonstrate capability

---

## 🚀 MVP Development Roadmap

### Suggested Build Order

| Day | Focus | Deliverable | Complexity |
|-----|-------|-------------|------------|
| 1 | Data pipeline | FastF1 setup, data extraction, local cache working | Medium |
| 2 | Tyre deg model | Basic regression model, deg curves visualization | Medium |
| 3 | Strategy simulator | Strategy comparison logic, ranking output | Hard |
| 4 | Strategy UI | Pit window viz, strategy explanations, polish | Medium |
| 5 | Overtake map | Zone identification, track visualization | Medium |
| 6 | Backtest + validation | Error metrics, accuracy display, methodology docs | Medium |
| 7 | Polish + deploy | Styling, README, demo video, deployment | Medium |

### Milestones

**M1: Data Foundation (End of Day 1)**
- [ ] FastF1 installed and pulling data
- [ ] Can extract stint data, lap times, compounds for a race
- [ ] Local cache working (parquet or SQLite)

**M2: Deg Model Working (End of Day 2)**
- [ ] Deg curves render for each compound
- [ ] Model produces reasonable predictions
- [ ] Basic Streamlit app shows the chart

**M3: Strategy Simulator Working (End of Day 4)**
- [ ] Compares at least 3 strategies
- [ ] Ranks by total race time
- [ ] Shows pit window visualization
- [ ] Displays explanation text

**M4: Overtake Map Working (End of Day 5)**
- [ ] Top passing zones identified
- [ ] Track visualization renders
- [ ] Zone explanations display

**M5: Portfolio-Ready (End of Day 7)**
- [ ] Backtest metrics displayed
- [ ] Full dark-mode styling applied
- [ ] Deployed to Streamlit Cloud
- [ ] Docker setup working
- [ ] README complete with screenshots
- [ ] Demo video recorded

---

## ✅ Definition of Done for MVP

The MVP is ready to launch when:

### Core Functionality
- [ ] All 3 core features working (deg model, strategy sim, overtake map)
- [ ] At least 1 hero race fully analyzed end-to-end
- [ ] Backtest/validation metrics displayed

### Quality
- [ ] Dark mode styling applied (not default Streamlit)
- [ ] F1-authentic compound colors used
- [ ] Model limitations clearly stated in UI
- [ ] No placeholder content

### Deployment
- [ ] Live on Streamlit Cloud (or equivalent free host)
- [ ] Docker Compose setup working locally
- [ ] Can be demoed in interview setting

### Documentation
- [ ] README with clear setup instructions
- [ ] Screenshots of key outputs
- [ ] Brief methodology explanation
- [ ] 2-3 minute demo video linked

---

## 📝 Next Steps

After this PRD is approved:

1. **Create Technical Design Document (Part III)** — data schema, architecture, tech stack decisions
2. **Set up development environment** — Python, FastF1, Streamlit, Git repo
3. **Build Day 1: Data pipeline** — get FastF1 pulling and caching data
4. **Iterate through roadmap** — follow the 7-day plan
5. **Deploy and document** — Streamlit Cloud + README + video
6. **Share for feedback** — Reddit r/F1Technical, F1 Discord communities

---

*Document created: January 10, 2026*  
*Status: Draft — Ready for Technical Design*  
*Timeline: 1 week to portfolio-ready MVP*
