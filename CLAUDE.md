# CLAUDE.md - Claude Code Configuration for F1 Strategy Room

## 🎯 Project Context
**App:** F1 Strategy Room  
**Stack:** FastAPI (Python 3.11) + Next.js 14 (TypeScript)  
**Stage:** MVP Development  
**User Level:** Vibe-coder (AI does most coding, user guides and tests)  
**Goal:** Portfolio-ready demo in 2 weeks

---

## 📋 Directives
1. **Master Plan:** Always read `AGENTS.md` first—it has current phase and tasks
2. **Documentation:** Refer to `agent_docs/` for tech stack, code patterns, testing
3. **Plan-First:** Propose a brief plan and wait for approval before coding
4. **Incremental Build:** Build one small feature at a time. Test frequently.
5. **Verify Changes:** After each feature, test it works before moving on
6. **Explain Simply:** User is learning—explain what you're doing and why
7. **F1 Authenticity:** Use correct terminology, real data, proper compound colors

---

## 🛠 Commands

### Backend (Python/FastAPI)
```bash
cd backend
pip install -r requirements.txt          # Install dependencies
uvicorn app.main:app --reload --port 8000 # Run dev server
pytest                                     # Run tests
python -c "import fastf1; print('OK')"    # Verify FastF1 installed
```

### Frontend (Next.js)
```bash
cd frontend
npm install                               # Install dependencies
npm run dev                               # Run dev server (port 3000)
npm run build                             # Production build
npm run lint                              # Check code style
```

### Docker
```bash
docker-compose up --build                 # Run both services
docker-compose down                       # Stop services
```

### FastF1 Quick Test
```python
import fastf1
fastf1.Cache.enable_cache('./data/cache')
session = fastf1.get_session(2023, 'Monza', 'R')
session.load()
print(f"Loaded {len(session.laps)} laps")
```

---

## 🎨 Code Style

### Python (Backend)
- Use type hints on all functions
- Add docstrings explaining WHAT and WHY
- Keep functions small and focused
- Use Pydantic models for API request/response
- Async where beneficial (FastF1 loads are slow)

```python
# Example pattern
def calculate_deg_curve(stint_data: list[dict], compound: str) -> dict | None:
    """
    What: Fits polynomial regression to lap times vs tyre age
    Why: Predicts future lap times for strategy simulation
    
    Returns None if insufficient data for compound.
    """
    # Implementation...
```

### TypeScript (Frontend)
- Use TypeScript strict mode
- Define interfaces for all API responses
- Use React hooks (useState, useEffect)
- Recharts for all charts
- Tailwind for styling (no separate CSS files)

```typescript
// Example pattern
interface DegradationCurve {
  compound: 'SOFT' | 'MEDIUM' | 'HARD';
  coefficients: [number, number, number];
  deg_per_lap: number;
  r_squared: number;
}
```

---

## 🚦 F1 Constants

### Compound Colors (Use These Exactly)
```typescript
const COMPOUND_COLORS = {
  SOFT: '#FF0000',      // Red
  MEDIUM: '#FFFF00',    // Yellow
  HARD: '#FFFFFF',      // White
  INTERMEDIATE: '#00FF00',
  WET: '#00BFFF',
};
```

### Circuit Pit Loss Times
```python
PIT_LOSS = {
    "Monza": 22.5,
    "Monaco": 24.0,
    "Spa": 21.0,
    "Bahrain": 22.0,
    "Silverstone": 21.5,
    "default": 22.0,
}
```

### Fuel Effect
```python
FUEL_EFFECT_PER_LAP = 0.055  # ~55ms per lap of fuel burn
```

---

## ⚠️ What NOT To Do
- Do NOT delete files without explicit confirmation
- Do NOT skip error handling—FastF1 fails on some races
- Do NOT use placeholder data—real FastF1 data only
- Do NOT hardcode race names—accept multiple formats
- Do NOT return pandas DataFrames from API—serialize to dicts
- Do NOT claim model is "accurate"—say "model suggests"
- Do NOT add features outside current phase
- Do NOT forget CORS middleware in FastAPI

---

## 🔑 Critical FastF1 Rules
1. **Enable cache BEFORE any session loads:**
   ```python
   fastf1.Cache.enable_cache('./data/cache')  # FIRST!
   ```
2. **Use `pick_quicklaps()` to filter outliers**
3. **Race names vary:** Try "Monza", "Italian Grand Prix", round 14
4. **First load is slow:** 30-60 seconds, show loading state
5. **Some races have missing data:** Handle gracefully

---

## 📁 Key Files Reference

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI entry point, CORS config |
| `backend/app/services/fastf1_client.py` | Data extraction from FastF1 |
| `backend/app/services/degradation_model.py` | Tyre deg calculation |
| `backend/app/services/strategy_engine.py` | Strategy simulation |
| `backend/app/services/overtake_analyzer.py` | Overtake zone analysis |
| `backend/app/models/schemas.py` | Pydantic request/response models |
| `frontend/src/lib/api.ts` | API client for backend |
| `frontend/src/lib/types.ts` | TypeScript interfaces |
| `frontend/src/components/` | All React components |

---

## 🎯 Hero Race: Monza 2023
Use this race for all development and testing:
- Year: 2023
- Race: "Monza" (or "Italian Grand Prix" or round 14)
- Session: "R" (Race)
- Why: Good strategy variety, clean data, well-documented

---

## 🆘 If Something Breaks

**FastF1 won't load:**
```bash
pip install --upgrade fastf1
rm -rf backend/data/cache/*  # Clear cache
```

**CORS errors:**
```python
# Ensure this is in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Frontend can't reach API:**
```bash
# Check env variable
echo $NEXT_PUBLIC_API_URL
# Should be http://localhost:8000
```

---

## 💡 Tips for This User
- **Explain as you go:** User is learning, appreciate the "why"
- **Show progress:** Celebrate small wins ("✅ API endpoint working!")
- **Visual results early:** Get charts rendering ASAP for motivation
- **Keep it working:** Never leave the app in a broken state
- **Test with real data:** Always use Monza 2023, not mock data
