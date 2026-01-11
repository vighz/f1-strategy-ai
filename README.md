# F1 Strategy Room

Turn F1 telemetry into race-winning strategy insights—in minutes, not hours.

## 🏁 Project Status

**Current Phase:** Phase 1 - Foundation ✅

- [x] Project structure and planning
- [x] Backend setup (FastAPI + FastF1)
- [x] Frontend setup (Next.js 14 + TypeScript + Tailwind)
- [x] Docker configuration
- [x] Pre-commit hooks
- [x] Monza 2023 data verified

## 🚀 Quick Start

### Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend runs on http://localhost:8000

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000

### Docker Compose (Both Services)

```bash
docker-compose up --build
```

## 📁 Project Structure

```
f1-strategy-room/
├── backend/                # FastAPI + Python
│   ├── app/
│   │   ├── main.py        # FastAPI entry point
│   │   ├── config.py      # Configuration
│   │   ├── services/      # Business logic
│   │   └── models/        # Data models
│   ├── data/cache/        # FastF1 cache
│   └── requirements.txt
├── frontend/              # Next.js + React
│   ├── app/               # Next.js App Router
│   ├── components/        # React components
│   └── lib/               # API client, types
├── docker-compose.yml
└── README.md
```

## 🎯 Tech Stack

- **Backend:** Python 3.11, FastAPI, FastF1, scikit-learn, pandas
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Recharts
- **Data:** FastF1 telemetry library
- **Deployment:** Docker, Docker Compose

## 🔧 Development

### Testing FastF1

```bash
cd backend
python test_fastf1.py
```

This loads Monza 2023 race data to verify FastF1 is working.

### Code Quality

Pre-commit hooks run automatically on `git commit`:
- Black (Python formatting)
- Flake8 (Python linting)
- isort (Import sorting)

## 📚 Documentation

See `agent_docs/` for detailed documentation:
- `tech_stack.md` - Tech stack details
- `code_patterns.md` - Code style and patterns
- `project_brief.md` - Project rules and conventions
- `product_requirements.md` - Full PRD

## 🏗 Roadmap

- [x] **Phase 1:** Foundation (Git, Docker, FastF1 setup)
- [ ] **Phase 2:** Backend Core (Degradation model, Strategy engine, API endpoints)
- [ ] **Phase 3:** Frontend Core (Components, charts, race selector)
- [ ] **Phase 4:** Polish & Deploy (Styling, deployment, demo)

## 📝 License

Private project - Portfolio piece
