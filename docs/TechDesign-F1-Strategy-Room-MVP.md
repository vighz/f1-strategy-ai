# Technical Design Document: F1 Strategy Room MVP

## 🎯 Executive Summary

**Project:** F1 Strategy Room  
**Approach:** FastAPI backend + Next.js frontend  
**Timeline:** 2 weeks  
**Budget:** $0 (free tiers only)  
**Builder:** AI-assisted (Claude Code in VS Code)  
**Goal:** Portfolio-ready demo with deployed app, hero race analysis, and backtest validation

---

## 🛠 How We'll Build It

### Recommended Stack: FastAPI + Next.js

Based on your requirements (portfolio polish, 2-week timeline, understanding what's built), here's the optimal path:

**Why this stack is perfect for you:**

| Factor | Why FastAPI + Next.js Wins |
|--------|---------------------------|
| Portfolio signal | Shows full-stack capability, not just "I used a template" |
| Separation of concerns | Backend logic (Python/FastF1) cleanly separated from frontend (React) |
| Industry relevance | Both are production-grade tools used by real companies |
| AI assistance | Claude Code excels at both Python and TypeScript |
| Free deployment | Vercel (frontend) + Render/Railway (backend) = $0 |
| Future extensibility | Easy to add features, swap components, or scale |

**Honest trade-offs:**

| Consideration | Reality |
|---------------|---------|
| More moving parts | Two codebases to maintain (but cleanly separated) |
| Deployment complexity | Two services to deploy (but both have one-click options) |
| Learning curve | More concepts than Streamlit (but you'll understand more) |

### Alternative Options (If You Need to Pivot)

| Option | Pros | Cons | Time to MVP | When to Choose |
|--------|------|------|-------------|----------------|
| **FastAPI + Next.js** ✓ | Professional, scalable, great portfolio signal | More complexity | 10-12 days | Default choice |
| **Streamlit** | Fastest, Python-only, built-in charts | Looks like a prototype, limited customization | 5-7 days | If behind by Day 7 |
| **FastAPI + React (Vite)** | Simpler than Next.js, still professional | No SSR, slightly less polished | 9-11 days | If Next.js feels too heavy |

**Fallback plan:** If by Day 7 you're significantly behind, pivot to Streamlit. The backend code (FastF1 + modeling) transfers directly.

---

## 📁 Project Structure

```
f1-strategy-room/
├── backend/                    # FastAPI + Python
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Environment variables, constants
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── races.py       # Race selection endpoints
│   │   │   ├── degradation.py # Tyre deg model endpoints
│   │   │   ├── strategy.py    # Strategy simulator endpoints
│   │   │   └── overtakes.py   # Overtake map endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── fastf1_client.py    # FastF1 data extraction
│   │   │   ├── degradation_model.py # Tyre deg calculations
│   │   │   ├── strategy_engine.py   # Strategy simulation
│   │   │   └── overtake_analyzer.py # Overtake zone analysis
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py     # Pydantic models for API
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── cache.py       # Data caching utilities
│   │       └── constants.py   # F1 constants (compounds, circuits)
│   ├── data/
│   │   └── cache/             # FastF1 cache directory
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_degradation.py
│   │   └── test_strategy.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # Next.js + React
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout (dark theme)
│   │   │   ├── page.tsx       # Home page
│   │   │   ├── globals.css    # Global styles
│   │   │   └── api/           # API route handlers (if needed)
│   │   ├── components/
│   │   │   ├── ui/            # Base components (Button, Card, etc.)
│   │   │   ├── RaceSelector.tsx
│   │   │   ├── DegradationChart.tsx
│   │   │   ├── StrategyRanking.tsx
│   │   │   ├── PitWindowChart.tsx
│   │   │   ├── OvertakeMap.tsx
│   │   │   └── BacktestDisplay.tsx
│   │   ├── lib/
│   │   │   ├── api.ts         # API client for backend
│   │   │   ├── types.ts       # TypeScript interfaces
│   │   │   └── constants.ts   # F1 colors, compound names
│   │   └── hooks/
│   │       └── useRaceData.ts # Custom hooks for data fetching
│   ├── public/
│   │   └── tracks/            # Track SVGs/images
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── Dockerfile
│
├── docker-compose.yml          # Local development setup
├── README.md                   # Setup instructions + screenshots
├── AGENTS.md                   # AI assistant instructions
└── .gitignore
```

**Why this structure:**
- **Separation:** Backend and frontend are independent — you can explain each clearly
- **Testability:** Services are isolated, making unit tests straightforward
- **AI-friendly:** Clear file purposes help Claude Code generate accurate code
- **Standard patterns:** Interviewers will recognize the organization immediately

---

## 🏗 Architecture Overview

### System Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER'S BROWSER                               │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    Next.js Frontend                          │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │    │
│  │  │  Race    │ │   Deg    │ │ Strategy │ │   Overtake   │   │    │
│  │  │ Selector │ │  Chart   │ │ Ranking  │ │     Map      │   │    │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └──────┬───────┘   │    │
│  └───────┼────────────┼────────────┼──────────────┼───────────┘    │
└──────────┼────────────┼────────────┼──────────────┼────────────────┘
           │            │            │              │
           ▼            ▼            ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend (Python)                        │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                        API Layer                             │    │
│  │   /api/races    /api/degradation   /api/strategy  /api/overtakes │
│  └─────────────────────────────────────────────────────────────┘    │
│                              │                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                     Service Layer                            │    │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐    │    │
│  │  │ Degradation │ │  Strategy   │ │  Overtake Analyzer  │    │    │
│  │  │    Model    │ │   Engine    │ │                     │    │    │
│  │  └──────┬──────┘ └──────┬──────┘ └──────────┬──────────┘    │    │
│  └─────────┼───────────────┼───────────────────┼───────────────┘    │
│            │               │                   │                     │
│  ┌─────────▼───────────────▼───────────────────▼───────────────┐    │
│  │                    FastF1 Client                             │    │
│  │              (Data extraction + caching)                     │    │
│  └─────────────────────────┬───────────────────────────────────┘    │
└────────────────────────────┼────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Local File System                                │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                    FastF1 Cache                              │    │
│  │              (Parquet files for race data)                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow (Request → Response)

**Example: User requests strategy for Monza 2023**

```
1. User selects "Monza 2023" in dropdown
   └─→ Frontend calls GET /api/strategy?year=2023&race=Monza

2. FastAPI receives request
   └─→ Router validates parameters with Pydantic

3. Strategy Engine service is invoked
   └─→ Checks if race data is cached
   └─→ If not cached: FastF1 Client fetches and caches

4. FastF1 Client extracts:
   └─→ Lap times, compounds, stint lengths, pit stop times

5. Degradation Model calculates:
   └─→ Deg curves per compound (polynomial regression)

6. Strategy Engine simulates:
   └─→ 1-stop strategies (S→H, M→H, S→M, M→S)
   └─→ 2-stop strategies (S→M→H, S→S→M, etc.)
   └─→ Ranks by total predicted race time

7. Response returned as JSON:
   └─→ strategy_ranking, pit_windows, explanation, backtest_metrics

8. Frontend renders:
   └─→ Strategy cards, pit window chart, explanation text
```

---

## 🔧 Component Deep Dive

### Component 1: FastF1 Data Client

**What it does:**  
Extracts race data from FastF1 library, handles caching, and provides clean data structures for other services.

**Why this approach:**  
FastF1 is the only free, comprehensive source of F1 telemetry. Caching is essential because raw data fetch takes 30-60 seconds.

**Inputs/Outputs:**

```python
# Input
race_request = {
    "year": 2023,
    "race": "Monza",    # GP name or round number
    "session": "R"      # R=Race, Q=Quali, FP1/FP2/FP3
}

# Output
race_data = {
    "laps": [...],           # All lap times with metadata
    "stints": [...],         # Grouped by driver + stint number
    "pit_stops": [...],      # Pit stop times and laps
    "weather": {...},        # Temperature, track temp, rain
    "session_info": {...}    # Circuit, date, total laps
}
```

**Key implementation details:**

```python
# backend/app/services/fastf1_client.py

import fastf1
from pathlib import Path
from functools import lru_cache

# CRITICAL: Set cache path BEFORE any fastf1 calls
CACHE_DIR = Path(__file__).parent.parent.parent / "data" / "cache"
fastf1.Cache.enable_cache(str(CACHE_DIR))

class FastF1Client:
    """
    What: Fetches and caches F1 session data from FastF1
    Why: Centralizes all FastF1 interactions, handles caching, 
         provides clean data structures for other services
    """
    
    def get_session(self, year: int, race: str, session: str = "R"):
        """
        Fetches a session. First call is slow (30-60s), subsequent calls instant.
        
        KNOWN QUIRK: Some older races have incomplete data.
        KNOWN QUIRK: Race names must match FastF1's naming (e.g., "Monza" not "Italian GP")
        """
        try:
            session = fastf1.get_session(year, race, session)
            session.load()  # This is the slow part - downloads if not cached
            return session
        except Exception as e:
            # FastF1 raises generic exceptions - log details for debugging
            raise FastF1DataError(f"Failed to load {year} {race}: {str(e)}")
    
    def extract_stint_data(self, session) -> list[dict]:
        """
        Extracts lap-by-lap data grouped by stint.
        
        What we get:
        - LapTime (timedelta) → convert to seconds
        - Compound (str): SOFT, MEDIUM, HARD, INTERMEDIATE, WET
        - TyreLife (int): laps on current set
        - Stint (int): stint number (1, 2, 3...)
        - Driver (str): 3-letter code
        
        What we DON'T get (and have to estimate):
        - Fuel load (estimate from lap number)
        - Traffic (have to infer from lap time outliers)
        - Push level (unknown)
        """
        laps = session.laps.pick_quicklaps()  # Removes outliers
        
        stints = []
        for driver in laps['Driver'].unique():
            driver_laps = laps[laps['Driver'] == driver]
            for stint_num in driver_laps['Stint'].unique():
                stint_laps = driver_laps[driver_laps['Stint'] == stint_num]
                stints.append({
                    'driver': driver,
                    'stint': stint_num,
                    'compound': stint_laps['Compound'].iloc[0],
                    'laps': [
                        {
                            'lap_number': row['LapNumber'],
                            'lap_time': row['LapTime'].total_seconds(),
                            'tyre_life': row['TyreLife'],
                        }
                        for _, row in stint_laps.iterrows()
                    ]
                })
        return stints
```

**FastF1 Known Quirks & Guardrails:**

| Quirk | What Happens | How We Handle It |
|-------|--------------|------------------|
| Race names vary | "Italian GP" vs "Monza" vs round number | Accept all, normalize internally |
| Missing data | Some laps have NaN times | Filter with `pick_quicklaps()` |
| Slow first load | 30-60 seconds per session | Show loading state, cache aggressively |
| Large cache | ~100MB per race weekend | Document disk requirements |
| API changes | FastF1 updates can break code | Pin version in requirements.txt |

---

### Component 2: Tyre Degradation Model

**What it does:**  
Models how lap times increase as tyres wear, producing degradation curves per compound.

**Why this approach:**  
Polynomial regression is the simplest model that captures the non-linear degradation pattern. More complex models (GP, neural nets) aren't worth the complexity for MVP.

**Inputs/Outputs:**

```python
# Input
stint_data = [
    {
        "compound": "MEDIUM",
        "laps": [
            {"tyre_life": 1, "lap_time": 82.5},
            {"tyre_life": 2, "lap_time": 82.7},
            # ...
        ]
    },
    # ... more stints
]

# Output
degradation_curves = {
    "SOFT": {
        "coefficients": [0.05, 0.001, 82.0],  # ax² + bx + c
        "deg_per_lap": 0.12,      # Average seconds lost per lap
        "optimal_stint_length": 18,
        "r_squared": 0.87,        # Model fit quality
    },
    "MEDIUM": {...},
    "HARD": {...}
}
```

**Key implementation:**

```python
# backend/app/services/degradation_model.py

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class DegradationModel:
    """
    What: Models tyre degradation as lap_time = f(tyre_life)
    Why: Predicts future lap times for strategy simulation
    
    Approach: 2nd-degree polynomial regression
    - Simple enough to implement and explain
    - Captures the non-linear "cliff" behavior
    - Interpretable coefficients
    
    Limitations (be honest about these):
    - Assumes fuel-corrected times (we estimate fuel effect)
    - Doesn't account for track evolution
    - Doesn't account for traffic
    - Different drivers have different deg characteristics
    """
    
    FUEL_EFFECT_PER_LAP = 0.055  # ~55ms per lap of fuel burn (F1 average)
    
    def fit_compound(self, stint_data: list[dict], compound: str) -> dict:
        """
        Fits degradation model for a single compound.
        
        Steps:
        1. Collect all laps for this compound across all drivers
        2. Fuel-correct the lap times
        3. Fit polynomial regression
        4. Calculate metrics
        """
        # Filter stints for this compound
        compound_stints = [s for s in stint_data if s['compound'] == compound]
        
        if len(compound_stints) < 2:
            return None  # Not enough data
        
        # Collect all lap data
        tyre_lives = []
        lap_times = []
        lap_numbers = []
        
        for stint in compound_stints:
            for lap in stint['laps']:
                tyre_lives.append(lap['tyre_life'])
                lap_times.append(lap['lap_time'])
                lap_numbers.append(lap.get('lap_number', lap['tyre_life']))
        
        # Fuel correction: subtract estimated fuel effect
        # Assumes full fuel at lap 1, linear burn
        fuel_corrected = [
            lt - (self.FUEL_EFFECT_PER_LAP * (max(lap_numbers) - ln))
            for lt, ln in zip(lap_times, lap_numbers)
        ]
        
        # Fit polynomial regression (degree 2)
        X = np.array(tyre_lives).reshape(-1, 1)
        y = np.array(fuel_corrected)
        
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        # Predictions for metrics
        y_pred = model.predict(X_poly)
        
        # Calculate degradation rate (slope at midpoint)
        midpoint = np.mean(tyre_lives)
        deg_per_lap = 2 * model.coef_[2] * midpoint + model.coef_[1]
        
        return {
            "compound": compound,
            "coefficients": [model.coef_[2], model.coef_[1], model.intercept_],
            "deg_per_lap": round(deg_per_lap, 3),
            "baseline_pace": round(model.intercept_, 3),
            "r_squared": round(r2_score(y, y_pred), 3),
            "rmse": round(np.sqrt(mean_squared_error(y, y_pred)), 3),
            "sample_size": len(tyre_lives),
        }
    
    def predict_lap_time(self, curve: dict, tyre_life: int) -> float:
        """Predicts lap time for a given tyre age using fitted curve."""
        a, b, c = curve['coefficients']
        return a * tyre_life**2 + b * tyre_life + c
```

**Model Limitations (Display in UI):**

```
⚠️ Model Assumptions:
• Fuel effect estimated at 0.055s/lap (may vary by circuit)
• Track evolution not modeled (early vs. late race pace differs)
• Traffic effects filtered but not perfectly
• Aggregates all drivers (individual deg varies)
• Weather assumed constant within session

Confidence: R² = {r_squared} | RMSE = {rmse}s
```

---

### Component 3: Strategy Simulator

**What it does:**  
Compares pit strategies, calculates total race time for each, ranks them, and explains recommendations.

**Why this approach:**  
Brute-force simulation of candidate strategies is straightforward and explainable. No complex optimization needed for MVP.

**Inputs/Outputs:**

```python
# Input
strategy_request = {
    "degradation_curves": {...},  # From DegradationModel
    "total_laps": 53,
    "pit_loss": 22.5,             # Seconds lost per pit stop (circuit-specific)
    "starting_compound": "MEDIUM",
    "min_stint_length": 10,       # Minimum laps per stint
}

# Output
strategy_result = {
    "ranking": [
        {
            "rank": 1,
            "strategy": "M→H",
            "stops": 1,
            "stints": [
                {"compound": "MEDIUM", "start_lap": 1, "end_lap": 28},
                {"compound": "HARD", "start_lap": 29, "end_lap": 53}
            ],
            "total_time": 5524.3,  # seconds
            "delta_to_best": 0.0,
            "pit_window": {"earliest": 24, "optimal": 28, "latest": 32}
        },
        {
            "rank": 2,
            "strategy": "S→M→H",
            "stops": 2,
            "total_time": 5538.7,
            "delta_to_best": 14.4,
            # ...
        }
    ],
    "explanation": "Low degradation favors 1-stop. M→H optimal because...",
    "backtest": {
        "matched_winner": True,
        "winner_strategy": "M→H",
        "prediction_error": 2.3  # seconds
    }
}
```

**Key implementation:**

```python
# backend/app/services/strategy_engine.py

from itertools import product
from typing import List, Dict

class StrategyEngine:
    """
    What: Simulates pit strategies and ranks by total race time
    Why: Core value proposition - answers "what strategy is fastest?"
    
    Approach:
    1. Generate candidate strategies (1-stop and 2-stop combinations)
    2. For each strategy, simulate lap-by-lap race time
    3. Add pit stop time loss
    4. Rank by total time
    5. Calculate optimal pit windows
    
    NOT modeled (V2):
    - Safety car probability
    - Undercut/overcut dynamics (tire temp on out-lap)
    - Track position effects
    - Weather changes
    """
    
    # Circuit-specific pit loss times (seconds)
    PIT_LOSS_BY_CIRCUIT = {
        "Monza": 22.5,
        "Monaco": 24.0,
        "Spa": 21.0,
        "Silverstone": 21.5,
        "Bahrain": 22.0,
        # ... add more as needed
        "default": 22.0
    }
    
    COMPOUNDS = ["SOFT", "MEDIUM", "HARD"]
    
    def __init__(self, deg_model: DegradationModel):
        self.deg_model = deg_model
    
    def generate_strategies(self, total_laps: int, available_compounds: List[str]) -> List[dict]:
        """
        Generates candidate strategies to evaluate.
        
        Rules:
        - Must use at least 2 compounds (F1 regulation)
        - Minimum stint length: 10 laps (realistic)
        - Maximum 2 stops for MVP
        """
        strategies = []
        min_stint = 10
        
        # 1-stop strategies
        for c1, c2 in product(available_compounds, repeat=2):
            if c1 != c2:  # Must use different compounds
                for pit_lap in range(min_stint, total_laps - min_stint + 1):
                    strategies.append({
                        "name": f"{c1[0]}→{c2[0]}",
                        "stops": 1,
                        "stints": [
                            {"compound": c1, "start": 1, "end": pit_lap},
                            {"compound": c2, "start": pit_lap + 1, "end": total_laps}
                        ],
                        "pit_laps": [pit_lap]
                    })
        
        # 2-stop strategies (simplified - key variants only)
        for c1, c2, c3 in product(available_compounds, repeat=3):
            if len(set([c1, c2, c3])) >= 2:  # At least 2 different compounds
                # Only test a few pit lap combinations to limit computation
                for p1 in range(min_stint, total_laps // 2, 5):
                    for p2 in range(p1 + min_stint, total_laps - min_stint, 5):
                        strategies.append({
                            "name": f"{c1[0]}→{c2[0]}→{c3[0]}",
                            "stops": 2,
                            "stints": [
                                {"compound": c1, "start": 1, "end": p1},
                                {"compound": c2, "start": p1 + 1, "end": p2},
                                {"compound": c3, "start": p2 + 1, "end": total_laps}
                            ],
                            "pit_laps": [p1, p2]
                        })
        
        return strategies
    
    def simulate_strategy(self, strategy: dict, deg_curves: dict, pit_loss: float) -> dict:
        """
        Simulates total race time for a strategy.
        
        For each stint:
        1. Get degradation curve for compound
        2. Sum predicted lap times for each lap in stint
        3. Add pit stop loss at end of stint (except last)
        """
        total_time = 0.0
        stint_details = []
        
        for i, stint in enumerate(strategy['stints']):
            compound = stint['compound']
            curve = deg_curves.get(compound)
            
            if not curve:
                return None  # Can't simulate without deg data
            
            stint_time = 0.0
            for lap in range(stint['start'], stint['end'] + 1):
                tyre_life = lap - stint['start'] + 1
                lap_time = self.deg_model.predict_lap_time(curve, tyre_life)
                stint_time += lap_time
            
            total_time += stint_time
            stint_details.append({
                **stint,
                "stint_time": round(stint_time, 2),
                "avg_lap": round(stint_time / (stint['end'] - stint['start'] + 1), 3)
            })
            
            # Add pit loss (except after last stint)
            if i < len(strategy['stints']) - 1:
                total_time += pit_loss
        
        return {
            **strategy,
            "stints": stint_details,
            "total_time": round(total_time, 2),
            "pit_time_total": round(pit_loss * strategy['stops'], 2)
        }
    
    def find_optimal_pit_window(self, strategy: dict, deg_curves: dict, pit_loss: float) -> dict:
        """
        Finds optimal pit lap(s) for a given compound sequence.
        Tests ±5 laps around default and returns best + window.
        """
        # Implementation details...
        pass
    
    def generate_explanation(self, ranking: List[dict], deg_curves: dict) -> str:
        """
        Generates rule-based explanation for the recommendation.
        
        Template approach - fill in computed values:
        """
        best = ranking[0]
        second = ranking[1] if len(ranking) > 1 else None
        
        # Determine key factors
        factors = []
        
        # 1-stop vs 2-stop reasoning
        if best['stops'] == 1:
            factors.append(f"Low degradation favors a 1-stop strategy")
        else:
            factors.append(f"High degradation makes 2-stop faster despite extra pit loss")
        
        # Compound choice reasoning
        hard_deg = deg_curves.get('HARD', {}).get('deg_per_lap', 0)
        medium_deg = deg_curves.get('MEDIUM', {}).get('deg_per_lap', 0)
        
        if hard_deg < medium_deg * 0.7:
            factors.append(f"Hard compound shows {((medium_deg - hard_deg) / medium_deg * 100):.0f}% less degradation than Medium")
        
        # Delta reasoning
        if second:
            delta = second['total_time'] - best['total_time']
            factors.append(f"Advantage over {second['name']}: {delta:.1f}s")
        
        return " | ".join(factors)
```

**Pit Loss Reference Table:**

| Circuit | Pit Loss (s) | Notes |
|---------|--------------|-------|
| Monaco | 24.0 | Slow pit lane, tight entry |
| Monza | 22.5 | Fast pit lane |
| Spa | 21.0 | Very fast pit lane |
| Singapore | 23.5 | Slow, tight |
| Bahrain | 22.0 | Average |
| Default | 22.0 | Use if circuit unknown |

---

### Component 4: Overtake Analyzer

**What it does:**  
Identifies and ranks overtaking opportunities on a circuit based on historical data and track characteristics.

**Why this approach:**  
Direct overtake labeling from telemetry is complex. We use a proxy: position changes between telemetry samples at key track sections, combined with DRS zone data.

**Inputs/Outputs:**

```python
# Input
circuit_request = {
    "year": 2023,
    "race": "Monza",
    "num_races_to_analyze": 3  # Historical data to aggregate
}

# Output
overtake_analysis = {
    "circuit": "Monza",
    "total_overtakes": 47,
    "zones": [
        {
            "rank": 1,
            "name": "Turn 1 (Variante del Rettifilo)",
            "corner_number": 1,
            "overtake_count": 18,
            "percentage": 38.3,
            "has_drs": True,
            "explanation": "Long DRS zone (950m) into heavy braking. Speed delta ~40 km/h.",
            "coordinates": {"x": 0.12, "y": 0.85}  # Normalized for track map
        },
        # ... more zones
    ],
    "track_characteristics": {
        "overtaking_difficulty": "Easy",  # Easy/Medium/Hard
        "drs_zones": 2,
        "key_factor": "Long straights favor DRS overtakes"
    }
}
```

**Key implementation:**

```python
# backend/app/services/overtake_analyzer.py

class OvertakeAnalyzer:
    """
    What: Identifies where overtakes happen on a circuit
    Why: Helps users understand track position importance
    
    Approach (MVP - proxy method):
    1. Load position data at mini-sectors or distance intervals
    2. Detect position changes between consecutive samples
    3. Map position changes to track sections
    4. Aggregate across multiple races for reliability
    
    Limitations:
    - Can't distinguish overtakes from mistakes/offs
    - Pit stop position changes filtered but not perfectly
    - DRS zones from static data, not telemetry
    
    Alternative (V2):
    - Use car telemetry + proximity to detect actual passes
    """
    
    # Pre-defined circuit data (MVP approach)
    CIRCUIT_DATA = {
        "Monza": {
            "corners": [
                {"number": 1, "name": "Variante del Rettifilo", "type": "chicane", "drs_before": True},
                {"number": 4, "name": "Variante della Roggia", "type": "chicane", "drs_before": True},
                {"number": 7, "name": "Lesmo 1", "type": "fast", "drs_before": False},
                # ...
            ],
            "drs_zones": [
                {"start_m": 0, "end_m": 950, "into_corner": 1},
                {"start_m": 1500, "end_m": 2200, "into_corner": 4},
            ],
            "total_length_m": 5793,
            "typical_overtaking": "Easy"
        },
        # ... more circuits
    }
    
    def analyze_overtakes(self, session) -> dict:
        """
        Analyzes position changes throughout the race.
        
        Method:
        1. Get position data at each distance marker
        2. Compare positions between consecutive markers
        3. A position gain = potential overtake
        4. Map to nearest corner
        5. Filter out pit stop effects
        """
        laps = session.laps
        
        # Get position changes
        position_changes = []
        
        for driver in laps['Driver'].unique():
            driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
            
            for i in range(1, len(driver_laps)):
                prev_pos = driver_laps.iloc[i-1]['Position']
                curr_pos = driver_laps.iloc[i]['Position']
                
                if curr_pos < prev_pos:  # Gained position
                    # Check if it's a pit stop lap (filter these out)
                    if not driver_laps.iloc[i-1].get('PitOutTime'):
                        position_changes.append({
                            'driver': driver,
                            'lap': driver_laps.iloc[i]['LapNumber'],
                            'positions_gained': prev_pos - curr_pos,
                        })
        
        # For MVP: Use pre-defined circuit data for zone mapping
        # Real implementation would use telemetry coordinates
        
        return self._aggregate_by_zone(position_changes, session.event['Location'])
    
    def _aggregate_by_zone(self, changes: list, circuit: str) -> dict:
        """Maps position changes to circuit zones using pre-defined data."""
        circuit_info = self.CIRCUIT_DATA.get(circuit, {})
        # Implementation...
        pass
    
    def generate_zone_explanation(self, zone: dict) -> str:
        """Generates human-readable explanation for an overtaking zone."""
        explanations = []
        
        if zone.get('drs_before'):
            explanations.append(f"DRS zone into corner")
        
        if zone.get('type') == 'chicane':
            explanations.append(f"Heavy braking zone")
        elif zone.get('type') == 'hairpin':
            explanations.append(f"Low-speed hairpin")
        
        if zone.get('overtake_percentage', 0) > 30:
            explanations.append(f"Accounts for {zone['overtake_percentage']:.0f}% of passes")
        
        return ". ".join(explanations) + "."
```

---

### Component 5: API Layer (FastAPI)

**What it does:**  
Exposes backend services as REST endpoints for the frontend to consume.

**Why FastAPI:**
- Type hints → automatic validation
- Auto-generated OpenAPI docs
- Async support (useful for slow FastF1 loads)
- Python-native (matches FastF1)

**API Endpoints:**

```python
# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="F1 Strategy Room API",
    description="Tyre degradation modeling and strategy simulation",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from app.routers import races, degradation, strategy, overtakes
app.include_router(races.router, prefix="/api/races", tags=["races"])
app.include_router(degradation.router, prefix="/api/degradation", tags=["degradation"])
app.include_router(strategy.router, prefix="/api/strategy", tags=["strategy"])
app.include_router(overtakes.router, prefix="/api/overtakes", tags=["overtakes"])
```

**Endpoint Reference:**

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/api/races` | GET | List available races | <100ms |
| `/api/races/{year}/{race}` | GET | Get race metadata | <100ms (cached) |
| `/api/degradation/{year}/{race}` | GET | Get deg curves | <500ms (cached) |
| `/api/strategy/{year}/{race}` | GET | Get strategy ranking | <1s (cached) |
| `/api/overtakes/{year}/{race}` | GET | Get overtake zones | <500ms (cached) |
| `/api/health` | GET | Health check | <50ms |

**Pydantic Models:**

```python
# backend/app/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Compound(str, Enum):
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INTERMEDIATE = "INTERMEDIATE"
    WET = "WET"

class DegradationCurve(BaseModel):
    compound: Compound
    coefficients: List[float]  # [a, b, c] for ax² + bx + c
    deg_per_lap: float
    baseline_pace: float
    r_squared: float
    rmse: float
    sample_size: int

class Stint(BaseModel):
    compound: Compound
    start_lap: int
    end_lap: int
    stint_time: Optional[float] = None

class Strategy(BaseModel):
    rank: int
    name: str  # e.g., "M→H"
    stops: int
    stints: List[Stint]
    total_time: float
    delta_to_best: float
    pit_window: Optional[dict] = None

class StrategyResponse(BaseModel):
    ranking: List[Strategy]
    explanation: str
    backtest: dict
    model_caveats: str

class OvertakeZone(BaseModel):
    rank: int
    name: str
    corner_number: int
    overtake_count: int
    percentage: float
    has_drs: bool
    explanation: str

class OvertakeResponse(BaseModel):
    circuit: str
    total_overtakes: int
    zones: List[OvertakeZone]
    track_characteristics: dict
```

---

### Component 6: Frontend (Next.js)

**What it does:**  
Renders the user interface, fetches data from the API, and displays interactive charts.

**Why Next.js:**
- React-based (huge ecosystem, AI knows it well)
- Server-side rendering (faster initial load)
- Easy deployment to Vercel
- TypeScript support (catches errors early)
- App Router (modern patterns)

**Key Components:**

```typescript
// frontend/src/components/DegradationChart.tsx

"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DegradationCurve } from '@/lib/types';

/**
 * What: Displays tyre degradation curves per compound
 * Why: Visual comparison of compound performance over stint
 * 
 * Props:
 * - curves: Array of degradation curve objects from API
 * - maxLaps: Maximum stint length to display (default: 40)
 */

const COMPOUND_COLORS = {
  SOFT: '#FF0000',      // F1 red
  MEDIUM: '#FFFF00',    // F1 yellow  
  HARD: '#FFFFFF',      // F1 white
  INTERMEDIATE: '#00FF00',
  WET: '#0000FF',
};

interface Props {
  curves: DegradationCurve[];
  maxLaps?: number;
}

export function DegradationChart({ curves, maxLaps = 40 }: Props) {
  // Generate chart data from coefficients
  const generateChartData = () => {
    const data = [];
    for (let lap = 1; lap <= maxLaps; lap++) {
      const point: any = { lap };
      curves.forEach(curve => {
        const [a, b, c] = curve.coefficients;
        point[curve.compound] = a * lap * lap + b * lap + c;
      });
      data.push(point);
    }
    return data;
  };

  const data = generateChartData();

  return (
    <div className="bg-gray-900 rounded-lg p-4">
      <h3 className="text-white text-lg font-semibold mb-4">Tyre Degradation</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="lap" 
            stroke="#9CA3AF"
            label={{ value: 'Tyre Age (laps)', position: 'bottom', fill: '#9CA3AF' }}
          />
          <YAxis 
            stroke="#9CA3AF"
            label={{ value: 'Lap Time (s)', angle: -90, position: 'left', fill: '#9CA3AF' }}
            domain={['dataMin - 0.5', 'dataMax + 0.5']}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1F2937', border: 'none' }}
            labelStyle={{ color: '#F3F4F6' }}
          />
          <Legend />
          {curves.map(curve => (
            <Line
              key={curve.compound}
              type="monotone"
              dataKey={curve.compound}
              stroke={COMPOUND_COLORS[curve.compound]}
              strokeWidth={2}
              dot={false}
              name={curve.compound}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
      
      {/* Model metrics */}
      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        {curves.map(curve => (
          <div key={curve.compound} className="text-center">
            <span 
              className="font-semibold"
              style={{ color: COMPOUND_COLORS[curve.compound] }}
            >
              {curve.compound}
            </span>
            <p className="text-gray-400">
              Deg: {curve.deg_per_lap}s/lap | R²: {curve.r_squared}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

**API Client:**

```typescript
// frontend/src/lib/api.ts

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * What: Typed API client for backend communication
 * Why: Centralizes API calls, handles errors consistently
 */

export async function fetchDegradation(year: number, race: string) {
  const res = await fetch(`${API_BASE}/api/degradation/${year}/${race}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch degradation: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchStrategy(year: number, race: string) {
  const res = await fetch(`${API_BASE}/api/strategy/${year}/${race}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch strategy: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchOvertakes(year: number, race: string) {
  const res = await fetch(`${API_BASE}/api/overtakes/${year}/${race}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch overtakes: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchRaces() {
  const res = await fetch(`${API_BASE}/api/races`);
  if (!res.ok) {
    throw new Error(`Failed to fetch races: ${res.statusText}`);
  }
  return res.json();
}
```

---

## 🎨 Design System

### Color Palette (F1 Authentic)

```css
/* frontend/src/app/globals.css */

:root {
  /* Background */
  --bg-primary: #0F0F0F;      /* Near black */
  --bg-secondary: #1A1A1A;    /* Card background */
  --bg-tertiary: #262626;     /* Hover states */
  
  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: #A3A3A3;
  --text-muted: #525252;
  
  /* F1 Compound Colors */
  --compound-soft: #FF0000;
  --compound-medium: #FFFF00;
  --compound-hard: #FFFFFF;
  --compound-inter: #00FF00;
  --compound-wet: #00BFFF;
  
  /* Accents */
  --accent-primary: #E10600;  /* F1 Red */
  --accent-success: #10B981;
  --accent-warning: #F59E0B;
  
  /* Borders */
  --border-default: #333333;
}
```

### Typography

```css
/* Use Inter for clean, modern look */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', system-ui, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

/* F1-style headers */
h1, h2, h3 {
  font-weight: 700;
  letter-spacing: -0.02em;
}
```

### Component Styling (Tailwind)

```typescript
// Example card component
<div className="bg-[#1A1A1A] border border-[#333333] rounded-lg p-6 hover:border-[#E10600] transition-colors">
  <h3 className="text-white text-lg font-semibold mb-2">Strategy Ranking</h3>
  <p className="text-gray-400 text-sm">Based on degradation model</p>
</div>
```

---

## 🗄 Data Management

### Caching Strategy

```
Layer 1: FastF1 Cache (Disk)
├── Stores raw session data
├── Location: backend/data/cache/
├── Size: ~100MB per race weekend
├── Lifetime: Permanent (data doesn't change)

Layer 2: Computed Results Cache (Memory/Redis)
├── Stores deg curves, strategy rankings
├── Location: In-memory dict (MVP) or Redis (production)
├── Lifetime: Until app restart
├── Key format: f"{year}_{race}_{endpoint}"

Layer 3: HTTP Cache Headers
├── Frontend caches API responses
├── Cache-Control: max-age=3600 (1 hour)
├── Invalidation: Manual or on new race data
```

**Implementation:**

```python
# backend/app/utils/cache.py

from functools import lru_cache
from typing import Dict, Any
import hashlib

# Simple in-memory cache for MVP
_cache: Dict[str, Any] = {}

def cache_key(year: int, race: str, endpoint: str) -> str:
    """Generates consistent cache key."""
    return f"{year}_{race.lower().replace(' ', '_')}_{endpoint}"

def get_cached(key: str) -> Any | None:
    """Returns cached value or None."""
    return _cache.get(key)

def set_cached(key: str, value: Any) -> None:
    """Stores value in cache."""
    _cache[key] = value

def clear_cache() -> None:
    """Clears all cached values."""
    _cache.clear()
```

### Pre-loading Hero Race

For instant demo experience, pre-compute and cache the hero race on startup:

```python
# backend/app/main.py

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Pre-load hero race
    print("Pre-loading Monza 2023...")
    try:
        # This triggers FastF1 cache and computes all derived data
        from app.services import fastf1_client, degradation_model, strategy_engine
        
        client = fastf1_client.FastF1Client()
        session = client.get_session(2023, "Monza", "R")
        
        # Pre-compute and cache
        stints = client.extract_stint_data(session)
        deg_model = degradation_model.DegradationModel()
        curves = {c: deg_model.fit_compound(stints, c) for c in ["SOFT", "MEDIUM", "HARD"]}
        
        # Cache results
        set_cached(cache_key(2023, "Monza", "degradation"), curves)
        print("Hero race pre-loaded successfully")
    except Exception as e:
        print(f"Warning: Could not pre-load hero race: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
```

---

## 🚀 Deployment

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         PRODUCTION                               │
│                                                                  │
│  ┌──────────────────┐          ┌──────────────────────────┐     │
│  │    Vercel        │          │    Render / Railway      │     │
│  │   (Frontend)     │  ──────► │      (Backend)           │     │
│  │                  │   API    │                          │     │
│  │  Next.js app     │  calls   │  FastAPI + FastF1        │     │
│  │  Static + SSR    │          │  + cached data           │     │
│  └──────────────────┘          └──────────────────────────┘     │
│         │                                 │                      │
│         │                                 │                      │
│         ▼                                 ▼                      │
│  yourdomain.vercel.app        yourapi.onrender.com              │
└─────────────────────────────────────────────────────────────────┘
```

### Frontend Deployment (Vercel)

**Steps:**
1. Push frontend code to GitHub
2. Connect repo to Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`
4. Deploy

**vercel.json** (optional):
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

### Backend Deployment (Render)

**Steps:**
1. Push backend code to GitHub
2. Create new Web Service on Render
3. Connect repo, set root directory to `backend/`
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables if needed

**render.yaml:**
```yaml
services:
  - type: web
    name: f1-strategy-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

**Important Render Considerations:**
- Free tier spins down after 15 min inactivity (first request is slow)
- 512MB RAM limit — FastF1 can be memory-hungry
- Disk is ephemeral — FastF1 cache resets on deploy

**Workaround for cold starts:**
- Use a cron job to ping the API every 10 minutes
- Or upgrade to paid tier ($7/month) for always-on

### Docker Setup (Local Demo)

```yaml
# docker-compose.yml

version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data/cache:/app/data/cache  # Persist FastF1 cache
    environment:
      - PYTHONUNBUFFERED=1

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
```

```dockerfile
# backend/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Create cache directory
RUN mkdir -p /app/data/cache

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile

FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

---

## 💰 Cost Breakdown

### Development Phase (2 Weeks)

| Service | Cost | Notes |
|---------|------|-------|
| Claude Code | $0 | Already have access |
| VS Code | $0 | Free |
| GitHub | $0 | Free tier |
| FastF1 | $0 | Open source |
| **Total** | **$0** | |

### Production Phase (After Launch)

| Service | Free Tier | Paid Option | You Need |
|---------|-----------|-------------|----------|
| Vercel (frontend) | 100GB bandwidth | $20/mo | Free OK |
| Render (backend) | 750 hrs/mo, spins down | $7/mo always-on | Free OK for demo |
| Domain (optional) | N/A | ~$12/year | Not required |
| **Total** | **$0** | **$27/mo** | **$0** |

### Scaling Costs (If Project Takes Off)

| Users | Monthly Cost | What Changes |
|-------|--------------|--------------|
| 0-100 | $0 | Free tiers handle it |
| 100-1000 | $20-30 | Upgrade Render to always-on |
| 1000+ | $50-100 | Add Redis, optimize caching |

---

## 📅 Development Roadmap

### Week 1: Core Functionality

| Day | Focus | Deliverable | Done Criteria |
|-----|-------|-------------|---------------|
| 1 | Project setup | Repos, Docker, FastF1 working | `docker-compose up` runs both services |
| 2 | Data pipeline | FastF1 client extracting data | Can print stint data for Monza 2023 |
| 3 | Deg model | Polynomial regression working | Deg curves render in terminal |
| 4 | Strategy engine | Simulation logic complete | Ranks 5+ strategies correctly |
| 5 | API layer | All endpoints working | Postman/curl returns valid JSON |
| 6 | Frontend shell | Next.js + API connected | Race selector loads real data |
| 7 | Deg + Strategy UI | Charts rendering | Deg curves + strategy ranking visible |

### Week 2: Polish + Deploy

| Day | Focus | Deliverable | Done Criteria |
|-----|-------|-------------|---------------|
| 8 | Overtake analyzer | Zone identification working | Top 3 zones display with explanations |
| 9 | Overtake UI | Track visualization | Map with highlighted zones |
| 10 | Backtest display | Validation metrics shown | MAE/RMSE + strategy accuracy visible |
| 11 | Styling | Dark theme, F1 aesthetic | Looks professional, not default |
| 12 | Deploy backend | Live on Render | API accessible from internet |
| 13 | Deploy frontend | Live on Vercel | Full app working end-to-end |
| 14 | Polish + docs | README, video, screenshots | Portfolio-ready |

### Milestone Checkpoints

**M1: Data Foundation (End of Day 2)**
- [ ] FastF1 installed and pulling data
- [ ] Can extract stint data, lap times, compounds
- [ ] Local cache working

**M2: Model Working (End of Day 4)**
- [ ] Deg curves calculate correctly
- [ ] Strategy simulation produces rankings
- [ ] Results match intuition for test race

**M3: API Complete (End of Day 5)**
- [ ] All endpoints return valid data
- [ ] Error handling in place
- [ ] Caching working

**M4: UI Functional (End of Day 9)**
- [ ] All charts render
- [ ] Data flows from API to UI
- [ ] Basic interactivity works

**M5: Portfolio-Ready (End of Day 14)**
- [ ] Deployed and accessible
- [ ] Styled professionally
- [ ] Documentation complete
- [ ] Demo video recorded

---

## 🤖 AI Assistant Strategy

### Claude Code Configuration

Create this file in your project root:

```markdown
# AGENTS.md

## Project: F1 Strategy Room

### Context
Building an F1 strategy analysis tool with FastAPI backend and Next.js frontend.
Data source: FastF1 library (Python).
Goal: Portfolio-ready demo in 2 weeks.

### Tech Stack
- Backend: Python 3.11, FastAPI, FastF1, scikit-learn, numpy, pandas
- Frontend: Next.js 14, TypeScript, Tailwind CSS, Recharts
- Deployment: Vercel (frontend), Render (backend), Docker

### Code Style
- Python: Use type hints, docstrings explaining what/why
- TypeScript: Strict mode, interfaces for all API responses
- Keep functions small and focused
- Comment non-obvious logic

### FastF1 Specifics
- ALWAYS reference FastF1 documentation: https://docs.fastf1.dev/
- Cache must be enabled BEFORE any session loads
- Use `pick_quicklaps()` to filter outliers
- Race names vary — handle "Monza", "Italian Grand Prix", round numbers

### API Patterns
- All endpoints return Pydantic models
- Use async where beneficial (FastF1 loads are slow)
- Cache computed results in memory

### Frontend Patterns
- Use Recharts for all charts
- F1 compound colors: SOFT=#FF0000, MEDIUM=#FFFF00, HARD=#FFFFFF
- Dark theme: bg-[#0F0F0F], text-white

### Testing
- Focus on service layer tests (degradation_model, strategy_engine)
- Use pytest with fixtures for session data
- Mock FastF1 calls in tests

### What NOT to do
- Don't use pandas DataFrames in API responses (serialize to dicts)
- Don't hardcode race data — always pull from FastF1
- Don't skip error handling — FastF1 fails on some races
```

### Effective Prompts for Claude Code

**Starting a new feature:**
```
I need to implement the tyre degradation model for F1 Strategy Room.

Context:
- FastF1 stint data is already extracted (see fastf1_client.py)
- Need polynomial regression (degree 2) on lap_time vs tyre_life
- Must fuel-correct using 0.055s/lap estimate
- Output needs coefficients, deg_per_lap, r_squared

Requirements from PRD:
- Shows deg curves for each compound
- Displays predicted lap time vs. tyre age
- Handles dry conditions

Please:
1. Explain the approach first
2. Then implement degradation_model.py
3. Include docstrings explaining what/why
```

**Debugging:**
```
Error in strategy simulation:

File: backend/app/services/strategy_engine.py
Error: KeyError: 'MEDIUM' when accessing deg_curves

Context:
- Some races don't use all compounds
- Need to handle missing compound data gracefully

Current code: [paste relevant section]

Please:
1. Explain why this is happening
2. Fix the issue
3. Add appropriate error handling
```

**Understanding generated code:**
```
You just generated this function:
[paste function]

Please explain:
1. What does each section do?
2. Why did you choose this approach?
3. What are the edge cases?
4. How would I explain this in an interview?
```

---

## ⚠️ Risk Mitigation

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| FastF1 data missing for some races | Medium | High | Test hero race early, have fallback races ready |
| Render free tier too slow | Medium | Medium | Optimize caching, consider Railway |
| Deg model accuracy poor | Low | High | Validate against actual race results early |
| Frontend charts not responsive | Low | Medium | Test on mobile by Day 10 |

### FastF1 Known Quirks

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Race name mismatch | `NoSessionError` | Try GP name, circuit name, and round number |
| Missing laps | NaN values in DataFrame | Use `pick_quicklaps()`, filter NaN |
| Slow first load | 30-60 second hang | Show loading state, pre-cache on startup |
| Memory usage | Process killed on Render | Limit concurrent sessions, clear unused data |
| API changes | Code breaks after FastF1 update | Pin version in requirements.txt |

### Debugging Playbook

**"API returns empty data"**
1. Check FastF1 cache exists: `ls backend/data/cache/`
2. Test FastF1 directly: `python -c "import fastf1; s = fastf1.get_session(2023, 'Monza', 'R'); s.load(); print(len(s.laps))"`
3. Check API logs for errors
4. Verify race name spelling

**"Deg curves look wrong"**
1. Print raw stint data: are lap times reasonable?
2. Check fuel correction: is it too aggressive?
3. Plot raw data points alongside fitted curve
4. Check R² value — if < 0.5, data quality issue

**"Strategy ranking doesn't match reality"**
1. Compare pit loss assumption to actual
2. Check if safety car affected real race
3. Verify deg model isn't extrapolating beyond data
4. Display as "model suggests" not "will happen"

**"Frontend not connecting to API"**
1. Check CORS settings in FastAPI
2. Verify `NEXT_PUBLIC_API_URL` is set
3. Test API directly with curl
4. Check browser network tab for errors

---

## 📚 Learning Resources

### FastF1

| Resource | Link | Use For |
|----------|------|---------|
| Official Docs | https://docs.fastf1.dev/ | API reference |
| Examples | https://docs.fastf1.dev/examples/ | Code patterns |
| GitHub | https://github.com/theOehrly/Fast-F1 | Source, issues |

### FastAPI

| Resource | Link | Use For |
|----------|------|---------|
| Official Tutorial | https://fastapi.tiangolo.com/tutorial/ | Learn basics |
| Pydantic Docs | https://docs.pydantic.dev/ | Data validation |

### Next.js

| Resource | Link | Use For |
|----------|------|---------|
| Official Docs | https://nextjs.org/docs | App Router patterns |
| Recharts | https://recharts.org/en-US/ | Chart components |
| Tailwind | https://tailwindcss.com/docs | Styling reference |

### F1 Analytics Community

| Resource | Link | Use For |
|----------|------|---------|
| r/F1Technical | reddit.com/r/F1Technical | Domain knowledge |
| F1 Discord | Various | Community help |
| f1-tempo | github.com/f1-tempo | Inspiration |

---

## ✅ Pre-Flight Checklist

### Before Starting Development
- [ ] Git repo created
- [ ] Docker installed and working
- [ ] VS Code + Claude Code configured
- [ ] FastF1 test: can load a session
- [ ] Read AGENTS.md to Claude Code

### Before Deployment
- [ ] All 3 core features working
- [ ] Hero race (Monza 2023) fully analyzed
- [ ] Backtest metrics display
- [ ] Dark theme applied
- [ ] Error states handled
- [ ] Loading states shown
- [ ] Mobile responsive (basic)

### Before Sharing
- [ ] README with setup instructions
- [ ] Screenshots of key outputs
- [ ] Methodology explanation
- [ ] 2-3 minute demo video
- [ ] GitHub repo is public
- [ ] Live link works in incognito

---

## 🎯 Definition of Technical Success

Your technical implementation succeeds when:

1. **It works:** All features produce valid output for the hero race
2. **It's honest:** Model limitations are clearly stated
3. **It's deployed:** Anyone can access via URL
4. **It's runnable:** Fresh clone + Docker works
5. **It's explainable:** You can walk through any component in an interview
6. **It looks professional:** Dark theme, F1 aesthetic, no placeholder content
7. **It's validated:** Backtest metrics prove the model isn't random

---

*Technical Design for: F1 Strategy Room MVP*  
*Stack: FastAPI + Next.js*  
*Timeline: 2 weeks*  
*Budget: $0*  
*Created: January 10, 2026*
