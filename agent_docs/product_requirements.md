# Product Requirements

## App Overview
**Name:** F1 Strategy Room  
**Tagline:** Turn F1 telemetry into race-winning strategy insights—in minutes, not hours  
**Timeline:** 2 weeks  
**Budget:** $0

---

## Target Users

### Primary: Data-Driven F1 Fan
Hardcore Formula 1 enthusiasts who want to go beyond punditry and gut feelings. They care about *why* a strategy works, not just *what* happened.

**Current Pain Points:**
- Spending hours wrangling FastF1 notebooks for basic insights
- YouTube strategy breakdowns are interesting but not interactive
- No easy way to generate shareable, credible visuals
- Fantasy F1 decisions feel like guesswork

**What They Need:**
- Quick, reliable strategy recommendations with clear reasoning
- Visual outputs they can screenshot or share
- Confidence that analysis is grounded in real telemetry

### Secondary Users
| User Type | Need | How We Help |
|-----------|------|-------------|
| Content Creators | Defensible analysis + shareable visuals | Export-ready charts, clear explanations |
| Fantasy F1 Players | Edge in predicting race outcomes | Strategy rankings, overtake difficulty insights |
| Aspiring Data Scientists | Learn F1 analytics patterns | Open-source, well-documented codebase |

---

## Primary User Story

> "Meet Aisha, a hardcore F1 fan who creates race-preview threads on Twitter. Every race week, she downloads session data, watches strategy breakdowns on YouTube, and sometimes opens a FastF1 notebook she found on GitHub—but it's time-consuming and inconsistent.
>
> She finds F1 Strategy Room through a GitHub link. She selects 'Monza 2023', sets conditions to dry, and clicks Generate Strategy. The app shows tyre degradation curves, a pit window chart, and ranks strategies like M→H one-stop vs S→M→H two-stop—with a quick explanation of why the undercut matters here.
>
> Then she opens the Overtake Map, sees the top passing zones visualized on the track, and uses that to argue: 'Track position matters—passing is concentrated into these braking zones.'
>
> Now she's happy because she can create a data-driven preview in minutes, with visuals that look credible and a narrative she can explain."

---

## Features

### 🔴 Must Have (P0)

#### 1. Tyre Degradation Model + Stint Pace Curves
**What:** Visualize how lap times degrade over a stint by compound (Soft/Medium/Hard)

**User Story:** As an F1 fan, I want to see how each tyre compound degrades so I can understand why certain strategies work better

**Success Criteria:**
- [ ] Shows deg curves for each compound used in selected race
- [ ] Displays predicted lap time vs. tyre age (lap number)
- [ ] Handles dry conditions reliably
- [ ] Clearly labels compounds with F1-standard colors (red/yellow/white)

---

#### 2. Pit Strategy Simulator
**What:** Compare and rank pit strategies (1-stop vs 2-stop), show optimal pit windows

**User Story:** As a content creator, I want to see which strategy is fastest and why so I can make informed race previews

**Success Criteria:**
- [ ] Ranks at least 3 strategy options (e.g., S→H, M→H, S→M→H)
- [ ] Shows estimated total race time for each strategy
- [ ] Displays pit window visualization (when to pit)
- [ ] Provides brief text explanation of recommendation
- [ ] Accounts for pit stop time loss (circuit-specific)

---

#### 3. Circuit Overtake Opportunity Map
**What:** Highlight top passing zones on the circuit with explanations

**User Story:** As a fantasy F1 player, I want to know where overtakes happen so I can assess track position importance

**Success Criteria:**
- [ ] Shows track layout with highlighted zones
- [ ] Ranks top 3-5 overtaking spots
- [ ] Provides brief explanation per zone (e.g., "Long DRS zone into heavy braking")
- [ ] Works for at least 5 circuits in MVP

---

#### 4. Race/Session Selector
**What:** Dropdown to select year, race, and session

**User Story:** As a user, I want to select which race to analyze

**Success Criteria:**
- [ ] Lists available races from FastF1 cache
- [ ] Pre-loads a "hero race" by default (Monza 2023)
- [ ] Handles loading states gracefully

---

#### 5. Backtest/Validation Display
**What:** Show model accuracy metrics

**User Story:** As a hiring manager viewing this portfolio piece, I want to see validation metrics so I trust the methodology

**Success Criteria:**
- [ ] Displays MAE/RMSE for degradation predictions
- [ ] Shows strategy accuracy proxy (e.g., "matched top-3 finisher strategy X%")
- [ ] Available for at least the hero race

---

### 🟡 Nice to Have (If Time Allows)
- Scenario toggles: Dry/wet switch, safety car probability slider
- Export buttons: Download charts as PNG
- Multiple hero races: 2-3 pre-analyzed circuits instead of 1

---

### 🚫 NOT in MVP

| Feature | Why Wait |
|---------|----------|
| Live race integration | Complex real-time architecture |
| Full SC/VSC probabilistic modeling | Significant complexity |
| Driver-specific personalization | "Generic car" model sufficient |
| Advanced overtake localization | Proxy approach sufficient |
| LLM assistant / chat UI | Not core to F1 realism |
| Accounts + saved scenarios | Requires auth infrastructure |
| Multi-season model retraining | Manual retraining fine for demo |

---

## Success Metrics

### Launch Success (Portfolio-Ready)
| Criterion | Target | How to Verify |
|-----------|--------|---------------|
| Deployed & accessible | App loads for anyone | Test from incognito browser |
| Runs locally | Docker setup works | Fresh clone + `docker-compose up` |
| Hero race complete | Monza 2023 fully analyzed | All 3 features produce output |
| Deg model validated | MAE/RMSE displayed | Backtest page shows metrics |
| Strategy accuracy shown | Proxy metric displayed | "Matched top-3 strategy X%" |
| README quality | Clear setup, screenshots | Could onboard new dev in 10 min |
| Demo video | 2-3 min walkthrough | Recorded and linked |

### Stretch Goals
| Goal | Target |
|------|--------|
| External feedback | 5-10 comments from F1 Reddit/Discord |
| Social proof | 1 share/retweet from F1 content creator |

---

## UI/UX Requirements

### Design Vibe
Clean, data-dense, race-engineer tool

### Visual Principles
1. **Dark mode by default** - matches F1 TV aesthetic
2. **Data density over whitespace** - race engineers pack info tight
3. **F1-authentic colors** - official compound colors (red/yellow/white)
4. **Professional, not flashy** - this is a tool, not a game

### Color Palette
- Background: #0F0F0F (near-black)
- Cards: #1A1A1A
- Text: White/light gray
- Accents: F1 red (#E10600)
- Soft: #FF0000
- Medium: #FFFF00
- Hard: #FFFFFF

### Key Screens
| Screen | Purpose | Key Elements |
|--------|---------|--------------|
| Home / Race Selector | Entry point | Race dropdown, "Analyze" button |
| Strategy Dashboard | Core analysis | Deg curves, strategy ranking, pit window |
| Overtake Map | Passing analysis | Track layout, ranked zones |
| Backtest / Validation | Model credibility | Error metrics, methodology notes |

---

## Performance Targets
- Initial load: < 5 seconds (with cached data)
- Strategy generation: < 10 seconds
- Chart rendering: < 2 seconds

---

## Quality Standards

### What F1 Strategy Room Will NOT Accept
| Anti-Pattern | Why It Matters |
|--------------|----------------|
| Placeholder data | Portfolio piece must show real outputs |
| Features that half-work | Complete or cut—no broken experiences |
| Unstyled default look | Dark theme + F1 aesthetic required |
| Claims without caveats | Model limitations must be visible |
| Skipping backtest display | Validation is core to portfolio value |

### Model Honesty Requirements
- Display confidence intervals or error ranges
- Clearly state what model doesn't account for
- Frame recommendations as "analysis suggests" not "guaranteed optimal"
