# Tech Stack & Tools

## Overview
F1 Strategy Room uses a modern full-stack architecture with Python backend and React frontend.

---

## Backend Stack

### Core Framework
- **FastAPI** (latest) - Modern Python web framework
  - Why: Type hints, auto-docs, async support, fast
  - Docs: https://fastapi.tiangolo.com/

### Python Version
- **Python 3.11** - Required for FastF1 compatibility

### Key Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `fastf1` | latest | F1 telemetry data extraction |
| `fastapi` | latest | REST API framework |
| `uvicorn` | latest | ASGI server |
| `pydantic` | v2 | Data validation & serialization |
| `numpy` | latest | Numerical operations |
| `pandas` | latest | Data manipulation (internal only) |
| `scikit-learn` | latest | Polynomial regression |
| `python-dotenv` | latest | Environment variables |

### requirements.txt
```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
fastf1>=3.3.0
numpy>=1.26.0
pandas>=2.2.0
scikit-learn>=1.4.0
pydantic>=2.5.0
python-dotenv>=1.0.0
pytest>=8.0.0
httpx>=0.26.0
```

---

## Frontend Stack

### Core Framework
- **Next.js 14** - React framework with App Router
  - Why: SSR, file-based routing, excellent DX
  - Docs: https://nextjs.org/docs

### Language
- **TypeScript** - Strict mode enabled

### Key Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| `next` | 14.x | React framework |
| `react` | 18.x | UI library |
| `recharts` | latest | Charting library |
| `tailwindcss` | 3.x | Utility-first CSS |
| `@types/react` | latest | TypeScript types |

### package.json dependencies
```json
{
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.12.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0",
    "@types/react": "^18.2.0",
    "@types/node": "^20.0.0",
    "eslint": "^8.56.0",
    "eslint-config-next": "^14.1.0"
  }
}
```

---

## Data Source: FastF1

### What It Provides
- Lap times (per driver, per lap)
- Tyre compounds used
- Stint information
- Pit stop data
- Weather conditions
- Session metadata

### What It Doesn't Provide (We Estimate)
- Fuel load (estimate from lap number)
- Traffic effects (filter outliers)
- Push level (unknown)
- Setup differences (unknown)

### Cache Location
```
backend/data/cache/
```
- ~100MB per race weekend
- First load: 30-60 seconds
- Subsequent loads: <1 second

### Quick Start
```python
import fastf1

# CRITICAL: Enable cache BEFORE loading any session
fastf1.Cache.enable_cache('./data/cache')

# Load a session
session = fastf1.get_session(2023, 'Monza', 'R')
session.load()

# Access lap data
laps = session.laps
quicklaps = laps.pick_quicklaps()  # Filter outliers
```

---

## Deployment Stack

### Frontend: Vercel
- Free tier: 100GB bandwidth
- Auto-deploy from GitHub
- Environment: `NEXT_PUBLIC_API_URL`

### Backend: Render
- Free tier: 750 hours/month
- Spins down after 15 min (cold starts)
- Consider Railway as alternative

### Local: Docker Compose
```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    volumes: ["./backend/data/cache:/app/data/cache"]
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Development Tools

### IDE
- **VS Code** with Claude Code extension
- Extensions: Python, Pylance, ESLint, Prettier

### Version Control
- **Git** + **GitHub**
- Commit after each milestone
- Use clear commit messages

### Testing
- Backend: `pytest`
- Frontend: Built-in Next.js testing
- Manual: Browser DevTools

---

## Environment Variables

### Backend (.env)
```
FASTF1_CACHE_DIR=./data/cache
DEBUG=true
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production
```
# Vercel
NEXT_PUBLIC_API_URL=https://your-api.onrender.com

# Render
PYTHON_VERSION=3.11
```

---

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `GET /api/races` | GET | List available races |
| `GET /api/races/{year}/{race}` | GET | Race metadata |
| `GET /api/degradation/{year}/{race}` | GET | Tyre deg curves |
| `GET /api/strategy/{year}/{race}` | GET | Strategy ranking |
| `GET /api/overtakes/{year}/{race}` | GET | Overtake zones |
| `GET /api/health` | GET | Health check |
