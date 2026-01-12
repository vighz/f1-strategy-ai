# 🏎️ F1 Strategy Room

**Turn F1 telemetry into race-winning strategy insights—in minutes, not hours.**

A full-stack data science application that analyzes Formula 1 race telemetry to predict optimal pit strategies using machine learning and real-world data from the FastF1 library.

[![Tech Stack](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)

---

## 🎯 Features

### 🔬 Tyre Degradation Analysis
- **Polynomial regression model** (2nd degree) to predict lap time degradation
- **Fuel correction** (~0.055s/lap) to isolate pure tyre wear
- **R² goodness-of-fit** metrics for model confidence
- **Interactive charts** showing degradation curves by compound (Soft/Medium/Hard)

### 🏁 Strategy Simulation
- **Exhaustive search** across 0-stop, 1-stop, 2-stop strategies
- **Lap-by-lap prediction** using fitted degradation curves
- **Circuit-specific pit loss** modeling (21-24 seconds)
- **Ranked strategies** by predicted race time with deltas

### 📊 Data Visualization
- **Recharts-powered** degradation curves with F1-authentic compound colors
- **Strategy comparison** with stint breakdowns and lap counts
- **Real-time loading states** for 30-60 second FastF1 data fetching
- **Model caveats** clearly displayed to set expectations

### 🎨 F1-Authentic Design
- **Dark theme** with F1 red (#E10600) accents
- **Official compound colors:** Red (Soft), Yellow (Medium), White (Hard)
- **Responsive layout** built with Tailwind CSS
- **Clean UX** optimized for portfolio demonstration

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd f1-strategy-room

# Start both backend and frontend
docker-compose up --build

# Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Access frontend at `http://localhost:3000`

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- **FastAPI** - Modern Python API framework
- **FastF1** - Official F1 telemetry library
- **scikit-learn** - Polynomial regression for degradation modeling
- **pandas** - Time series data processing
- **uvicorn** - ASGI server

**Frontend:**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe frontend development
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization library

**Data & ML:**
- **Polynomial Regression** (2nd degree) for tyre degradation
- **Monte Carlo-style enumeration** for strategy optimization
- **Time series feature engineering** (stint segmentation, fuel correction)
- **R² validation** for model quality assessment

### Project Structure

```
f1-strategy-room/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── config.py                  # Environment config & F1 constants
│   │   ├── routers/                   # API endpoints
│   │   │   ├── races.py               # GET /api/races/{year}
│   │   │   ├── degradation.py         # POST /api/degradation
│   │   │   ├── strategy.py            # POST /api/strategy
│   │   │   └── overtakes.py           # POST /api/overtakes
│   │   ├── services/                  # Business logic
│   │   │   ├── fastf1_client.py       # FastF1 data extraction
│   │   │   ├── degradation_model.py   # ML model for tyre deg
│   │   │   ├── strategy_engine.py     # Strategy simulation
│   │   │   └── overtake_analyzer.py   # Overtake zone analysis
│   │   └── models/
│   │       └── schemas.py             # Pydantic request/response models
│   ├── data/cache/                    # FastF1 parquet cache (~100MB/race)
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx                   # Main race analysis page
│   │   └── layout.tsx                 # Root layout with metadata
│   ├── components/
│   │   ├── RaceSelector.tsx           # 2023 season race grid
│   │   ├── DegradationChart.tsx       # Recharts line chart
│   │   └── StrategyRanking.tsx        # Top 5 strategies display
│   ├── lib/
│   │   ├── api.ts                     # Backend API client
│   │   └── types.ts                   # TypeScript interfaces
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .pre-commit-config.yaml            # Black, Flake8, isort hooks
├── AGENTS.md                          # Development roadmap & status
├── CLAUDE.md                          # AI assistant configuration
└── README.md
```

---

## 📊 Data Science Approach

### 1. Tyre Degradation Model

**Algorithm:** 2nd-degree polynomial regression

```python
lap_time = a * (tyre_age)² + b * (tyre_age) + c
```

**Features:**
- Fuel correction: Subtracts ~0.055s/lap to isolate tyre wear
- Outlier filtering: Uses FastF1's `pick_quicklaps()` to remove traffic
- Minimum sample size: Requires ≥5 laps per compound
- Quality metric: R² coefficient of determination

**Example Output (Monza 2023):**
- MEDIUM: 0.35s/lap degradation (R² = 0.89)
- HARD: 0.04s/lap degradation (R² = 0.76)

### 2. Strategy Simulation Engine

**Algorithm:** Exhaustive search with lap-by-lap simulation

- Generates all viable compound combinations (0-3 stops)
- Predicts lap time at each tyre age using degradation curves
- Adds circuit-specific pit loss (22-24 seconds)
- Ranks by total predicted race time

**Search Space:** ~20-30 viable strategies per race

### 3. Data Pipeline

```
Raw Telemetry (FastF1)
    ↓
Lap Filtering (traffic, flags)
    ↓
Stint Segmentation (by compound)
    ↓
Fuel Correction (0.055s/lap)
    ↓
Polynomial Fitting (R² validation)
    ↓
Strategy Simulation (lap-by-lap)
    ↓
Ranked Results (by race time)
```

---

## 🧪 Testing & Validation

### Hero Race: Monza 2023

All development and testing uses **Italian Grand Prix 2023** as the reference race:
- Good strategy variety (0-stop, 1-stop, 2-stop all viable)
- Clean telemetry data
- Well-documented real-world strategies for comparison

### Test the Backend

```bash
cd backend
python test_fastf1.py
```

Expected output:
- Loads 879 quick laps from Monza 2023
- Shows Verstappen's 2-stop strategy (MEDIUM 19L, HARD 30L)
- Validates FastF1 cache is working

### Run Pre-commit Hooks

```bash
pre-commit run --all-files
```

Checks:
- Black code formatting
- Flake8 linting
- isort import sorting

---

## 🌐 Deployment

### Backend (Render)

1. Create new Web Service on [Render](https://render.com)
2. Connect GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `PYTHON_VERSION=3.11`
     - `CORS_ORIGINS=https://your-frontend-url.vercel.app`

### Frontend (Vercel)

1. Import project on [Vercel](https://vercel.com)
2. Set **Root Directory:** `frontend`
3. Configure:
   - **Framework Preset:** Next.js
   - **Environment Variables:**
     - `NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com`

---

## ⚠️ Model Limitations

The UI prominently displays these caveats:

- **Fuel effect** estimated at 0.055s/lap (may vary by circuit)
- **Track evolution** not modeled (grip increases over session)
- **Traffic effects** filtered but not perfectly removed
- **Driver aggregation** assumes homogeneous degradation (ignores driving style)
- **Weather** assumed constant within session
- **Predictive value** for future races is suggestive, not exact

---

## 🎥 Demo

**Live Demo:** https://f1-strategy-ai-lyart.vercel.app

**Backend API:** https://f1-strategy-ai-oqtg.onrender.com/docs

**Usage:**
1. Select a race from the 2023 season grid
2. Wait 30-60 seconds for FastF1 to load telemetry (first load only, then cached)
3. View degradation curves for each compound
4. See top 5 optimal strategies ranked by predicted race time
5. Compare stint breakdowns with lap counts and time deltas

---

## 📸 Screenshots

### Race Selection
![Race Selection](https://via.placeholder.com/800x400?text=Add+Screenshot+Here)
*Select from 22 races in the 2023 F1 season*

### Degradation Analysis
![Degradation Chart](https://via.placeholder.com/800x400?text=Add+Screenshot+Here)
*Polynomial regression curves showing tyre degradation by compound*

### Strategy Ranking
![Strategy Ranking](https://via.placeholder.com/800x400?text=Add+Screenshot+Here)
*Top 5 optimal strategies with stint breakdowns and time deltas*

---

## 🔑 Key Learnings

### Technical Highlights

- **Full-stack TypeScript/Python** integration with FastAPI + Next.js
- **Real-world ML application** with regression, validation, and visualization
- **Production-ready architecture** with Docker, CORS, error handling
- **Memory-optimized deployment** - selective data loading to run within 512MB Render free tier
- **Data engineering** with time series processing and feature extraction
- **Domain-specific modeling** using F1 racing physics and constraints

### Potential Enhancements

Future improvements could include:
1. **Gradient Boosting (XGBoost)** with track temperature, driver style features
2. **Bayesian Optimization** for strategy search instead of exhaustive enumeration
3. **Driver clustering** (K-means) to segment aggressive vs smooth driving styles
4. **Ensemble methods** combining polynomial + exponential decay models
5. **Uncertainty quantification** with bootstrap confidence intervals

---

## 🤝 Contributing

This is a portfolio project, but feedback is welcome! Feel free to:
- Open issues for bugs or suggestions
- Star ⭐ the repo if you find it interesting
- Share with F1 or data science enthusiasts

---

## 📚 References

- **FastF1 Documentation:** https://docs.fastf1.dev/
- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Next.js Documentation:** https://nextjs.org/docs
- **Recharts Examples:** https://recharts.org/en-US/examples

---

## 📝 License

MIT License - Free to view and reference for educational/portfolio purposes

---

**Built with ☕ by Vighnesh Prabhu**
