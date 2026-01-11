# Project Brief (Persistent)

## Product Vision
**F1 Strategy Room** turns F1 telemetry into race-winning strategy insights—in minutes, not hours.

Target users: Hardcore F1 fans, content creators, and fantasy F1 players who want data-backed strategy analysis without maintaining their own notebooks.

---

## Core Value Proposition
1. **Tyre Degradation Visualization** - See how each compound degrades over a stint
2. **Strategy Simulation** - Compare 1-stop vs 2-stop, get optimal pit windows
3. **Overtake Mapping** - Know where passes happen on each circuit

---

## Quality Gates

### Before Any PR/Merge
- [ ] Feature works with Monza 2023 data
- [ ] No TypeScript errors (`npm run build` passes)
- [ ] No Python syntax errors
- [ ] API returns valid JSON
- [ ] UI doesn't crash on load

### Before Deployment
- [ ] All 3 core features functional
- [ ] Dark theme applied (not default styling)
- [ ] Model caveats displayed in UI
- [ ] Error states handled gracefully
- [ ] Loading states shown

### Portfolio Standards
- [ ] No placeholder data
- [ ] No Lorem ipsum
- [ ] Real FastF1 data only
- [ ] Professional appearance

---

## Coding Conventions

### Architecture
- **Routers** handle HTTP request/response only
- **Services** contain all business logic
- **No database calls from routers**
- **No pandas DataFrames in API responses**

### Naming
- Python: snake_case for files/functions, PascalCase for classes
- TypeScript: PascalCase for components, camelCase for functions
- Clear, descriptive names over abbreviations

### Error Handling
- Never crash silently
- Provide helpful error messages
- Log errors for debugging
- Show user-friendly errors in UI

### Comments
- Explain WHY, not just WHAT
- Use docstrings in Python
- Document limitations and assumptions

---

## Key Commands

### Development
```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev

# Both (Docker)
docker-compose up --build
```

### Testing
```bash
# Backend tests
cd backend && pytest

# Frontend lint
cd frontend && npm run lint

# Quick FastF1 test
python -c "import fastf1; print('FastF1 OK')"
```

### Deployment
```bash
# Frontend to Vercel
vercel --prod

# Backend to Render
git push origin main  # Auto-deploys
```

---

## Critical Constraints

### FastF1 Rules
1. Enable cache BEFORE loading sessions
2. Use `pick_quicklaps()` to filter outliers
3. Handle race name variations gracefully
4. Expect 30-60s load time for new sessions

### Model Honesty
- Always display R² and RMSE values
- State what the model doesn't account for
- Use "model suggests" not "will happen"
- Show confidence intervals where possible

### Design Requirements
- Dark theme (#0F0F0F background)
- F1 compound colors (red/yellow/white)
- Professional, data-dense aesthetic
- No flashy animations

---

## Update Cadence

### Update AGENTS.md When:
- Completing a phase milestone
- Encountering a blocker
- Making architectural decisions
- Adding new dependencies

### Update This Brief When:
- Changing coding conventions
- Adding new quality gates
- Modifying deployment process

---

## Hero Race Reference

**Monza 2023 (Italian Grand Prix)**
- Year: 2023
- Race: "Monza" or "Italian Grand Prix" or Round 14
- Session: "R" (Race)
- Total Laps: 51
- Known characteristics: Low degradation, 1-stop favored
- Good for testing: Multiple compound strategies used

---

## Contact & Resources

### FastF1 Documentation
https://docs.fastf1.dev/

### FastAPI Tutorial
https://fastapi.tiangolo.com/tutorial/

### Next.js Docs
https://nextjs.org/docs

### Project Repository
(To be created)

### Deployment URLs
- Frontend: (Vercel - TBD)
- Backend: (Render - TBD)
