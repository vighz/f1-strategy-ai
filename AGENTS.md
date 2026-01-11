# AGENTS.md - Master Plan for F1 Strategy Room

## 🎯 Project Overview
**App:** F1 Strategy Room
**Tagline:** Turn F1 telemetry into race-winning strategy insights—in minutes, not hours
**Stack:** FastAPI (Python) + Next.js (TypeScript)
**Timeline:** 2 weeks
**Budget:** $0 (free tiers only)
**Current Phase:** Phase 1 - Foundation

---

## 🧠 How I Should Think
1. **Understand Intent First**: Before coding, identify what the user actually needs
2. **Ask If Unsure**: If critical information is missing, ask before proceeding
3. **Plan Before Coding**: Propose a brief plan, wait for approval, then implement
4. **Verify After Changes**: Run tests/linters or manual checks after each change
5. **Explain Trade-offs**: When recommending something, mention alternatives
6. **Be F1-Authentic**: Use correct terminology, compound colors, and data sources

---

## 🔁 Plan → Execute → Verify
1. **Plan:** Outline approach and ask for approval before coding
2. **Execute:** Implement one feature at a time
3. **Verify:** Run tests or manual checks after each feature; fix before moving on
4. **Commit:** Create checkpoints after milestones

---

## 📁 Context Files
Refer to these for details (load only when needed):
- `agent_docs/tech_stack.md` - Tech stack, libraries, versions
- `agent_docs/code_patterns.md` - Code style, patterns, examples
- `agent_docs/project_brief.md` - Persistent project rules and conventions
- `agent_docs/product_requirements.md` - Full PRD with user stories
- `agent_docs/testing.md` - Verification strategy and commands

---

## 🏗 Project Structure
```
f1-strategy-room/
├── backend/                    # FastAPI + Python
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Environment variables
│   │   ├── routers/           # API endpoints
│   │   │   ├── races.py
│   │   │   ├── degradation.py
│   │   │   ├── strategy.py
│   │   │   └── overtakes.py
│   │   ├── services/          # Business logic
│   │   │   ├── fastf1_client.py
│   │   │   ├── degradation_model.py
│   │   │   ├── strategy_engine.py
│   │   │   └── overtake_analyzer.py
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic models
│   │   └── utils/
│   ├── data/cache/            # FastF1 cache
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Next.js + React
│   ├── src/
│   │   ├── app/               # Next.js App Router
│   │   ├── components/        # React components
│   │   │   ├── DegradationChart.tsx
│   │   │   ├── StrategyRanking.tsx
│   │   │   ├── PitWindowChart.tsx
│   │   │   ├── OvertakeMap.tsx
│   │   │   └── BacktestDisplay.tsx
│   │   ├── lib/               # API client, types
│   │   └── hooks/
│   ├── public/tracks/         # Track SVGs
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── AGENTS.md                  # This file
├── CLAUDE.md                  # Claude Code config
└── README.md
```

---

## 🔄 Current State (Update This!)
**Last Updated:** January 11, 2026
**Working On:** Phase 4 - Polish & Deploy (next up)
**Recently Completed:** Phase 3 - Frontend Core (React components, API integration, data visualization)
**Blocked By:** None

---

## 🚀 Roadmap

### Phase 1: Foundation (Days 1-2) ✅
- [x] Initialize Git repo
- [x] Set up Docker Compose for backend + frontend
- [x] Install FastF1 and verify data fetching
- [x] Create FastF1 client service
- [x] Test data extraction for Monza 2023 (hero race)
- [x] Set up local caching (parquet files)

### Phase 2: Backend Core (Days 3-5) ✅
- [x] Implement DegradationModel service (polynomial regression)
- [x] Implement StrategyEngine service (simulate & rank strategies)
- [x] Implement OvertakeAnalyzer service (zone identification)
- [x] Create all API endpoints (/api/degradation, /api/strategy, /api/overtakes, /api/races)
- [x] Add Pydantic schemas for request/response validation
- [x] Implement caching for computed results

### Phase 3: Frontend Core (Days 6-9) ✅
- [x] Set up Next.js with TypeScript + Tailwind
- [x] Create API client (lib/api.ts)
- [x] Build RaceSelector component
- [x] Build DegradationChart component (Recharts)
- [x] Build StrategyRanking component
- [x] Integrated all components in main page with loading/error states
- [ ] Build PitWindowChart component (deferred to Phase 4)
- [ ] Build OvertakeMap component (deferred to Phase 4)
- [ ] Build BacktestDisplay component (deferred to Phase 4)

### Phase 4: Polish & Deploy (Days 10-14)
- [ ] Apply dark theme + F1 styling
- [ ] Add loading states and error handling
- [ ] Display model caveats/limitations in UI
- [ ] Deploy backend to Render
- [ ] Deploy frontend to Vercel
- [ ] Create README with setup instructions
- [ ] Record 2-3 minute demo video
- [ ] Take screenshots for portfolio

---

## ✅ Success Criteria (Definition of Done)

### Core Functionality
- [ ] All 3 features working (deg model, strategy sim, overtake map)
- [ ] Monza 2023 fully analyzed end-to-end
- [ ] Backtest/validation metrics displayed

### Quality
- [ ] Dark mode styling (not default Streamlit/Next.js look)
- [ ] F1-authentic compound colors (red/yellow/white)
- [ ] Model limitations clearly stated in UI
- [ ] No placeholder content

### Deployment
- [ ] Live on Vercel (frontend) + Render (backend)
- [ ] Docker Compose works locally
- [ ] Can be demoed in interview setting

### Documentation
- [ ] README with clear setup instructions
- [ ] Screenshots of key outputs
- [ ] Brief methodology explanation
- [ ] Demo video linked

---

## ⚠️ What NOT To Do
- Do NOT delete files without explicit confirmation
- Do NOT modify database/cache schemas without backup plan
- Do NOT add features not in the current phase
- Do NOT skip verification for "simple" changes
- Do NOT use placeholder/fake data (real FastF1 data only)
- Do NOT hardcode race data—always pull from FastF1
- Do NOT use pandas DataFrames in API responses (serialize to dicts)
- Do NOT claim the model is "accurate"—frame as "model suggests"

---

## 🔧 Key Technical Decisions

### FastF1 Quirks to Remember
| Issue | Solution |
|-------|----------|
| Race names vary ("Italian GP" vs "Monza") | Try GP name, circuit name, round number |
| Missing laps (NaN values) | Use `pick_quicklaps()` to filter |
| Slow first load (30-60s) | Show loading state, cache aggressively |
| Large cache (~100MB/race) | Document disk requirements |

### Model Limitations (Display in UI)
```
⚠️ Model Assumptions:
• Fuel effect estimated at 0.055s/lap (may vary by circuit)
• Track evolution not modeled
• Traffic effects filtered but not perfectly
• Aggregates all drivers (individual deg varies)
• Weather assumed constant within session
```

### API Response Times
| Endpoint | Target |
|----------|--------|
| /api/races | <100ms |
| /api/degradation | <500ms (cached) |
| /api/strategy | <1s (cached) |
| /api/overtakes | <500ms (cached) |

---

## 🎨 Design Requirements

### Color Palette
- **Background:** #0F0F0F (near black)
- **Cards:** #1A1A1A
- **Text:** #FFFFFF / #A3A3A3
- **F1 Red accent:** #E10600
- **Compound SOFT:** #FF0000
- **Compound MEDIUM:** #FFFF00
- **Compound HARD:** #FFFFFF

### Typography
- Font: Inter (or system sans-serif)
- Headers: Bold, tight letter-spacing
- Data/numbers: Consider monospace

---

## 📚 Reference Documentation
- **FastF1 Docs:** https://docs.fastf1.dev/
- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Next.js Docs:** https://nextjs.org/docs
- **Recharts:** https://recharts.org/en-US/
- **Tailwind:** https://tailwindcss.com/docs

---

## 🆘 Debugging Playbook

**"API returns empty data"**
1. Check FastF1 cache exists: `ls backend/data/cache/`
2. Test FastF1 directly: `python -c "import fastf1; s = fastf1.get_session(2023, 'Monza', 'R'); s.load(); print(len(s.laps))"`
3. Check API logs for errors
4. Verify race name spelling

**"Deg curves look wrong"**
1. Print raw stint data—are lap times reasonable?
2. Check fuel correction—is it too aggressive?
3. Plot raw data points alongside fitted curve
4. Check R² value—if < 0.5, data quality issue

**"Strategy ranking doesn't match reality"**
1. Compare pit loss assumption to actual
2. Check if safety car affected real race
3. Verify deg model isn't extrapolating beyond data

**"Frontend not connecting to API"**
1. Check CORS settings in FastAPI
2. Verify `NEXT_PUBLIC_API_URL` is set correctly
3. Test API directly with curl
4. Check browser network tab for errors

---

*Last updated: January 10, 2026*
