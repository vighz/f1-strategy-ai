# Code Patterns & Style Guide

## General Principles
- Keep functions small and focused
- Add comments explaining WHY, not just WHAT
- Handle errors gracefully—never crash silently
- Use type hints everywhere (Python) and strict TypeScript

---

## Python Patterns (Backend)

### Service Class Pattern
All business logic lives in services, not routers.

```python
# backend/app/services/degradation_model.py

import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class DegradationModel:
    """
    What: Models tyre degradation as lap_time = f(tyre_life)
    Why: Predicts future lap times for strategy simulation
    
    Approach: 2nd-degree polynomial regression
    - Simple enough to implement and explain
    - Captures the non-linear "cliff" behavior
    - Interpretable coefficients
    """
    
    FUEL_EFFECT_PER_LAP = 0.055  # ~55ms per lap of fuel burn
    
    def fit_compound(self, stint_data: list[dict], compound: str) -> dict | None:
        """
        Fits degradation model for a single compound.
        
        Args:
            stint_data: List of stint objects from FastF1 client
            compound: One of SOFT, MEDIUM, HARD
            
        Returns:
            Dict with coefficients and metrics, or None if insufficient data
        """
        # Filter stints for this compound
        compound_stints = [s for s in stint_data if s['compound'] == compound]
        
        if len(compound_stints) < 2:
            return None  # Not enough data
        
        # Collect all lap data
        tyre_lives = []
        lap_times = []
        
        for stint in compound_stints:
            for lap in stint['laps']:
                tyre_lives.append(lap['tyre_life'])
                lap_times.append(lap['lap_time'])
        
        # Fit polynomial regression
        X = np.array(tyre_lives).reshape(-1, 1)
        y = np.array(lap_times)
        
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        
        model = LinearRegression()
        model.fit(X_poly, y)
        
        y_pred = model.predict(X_poly)
        
        return {
            "compound": compound,
            "coefficients": [model.coef_[2], model.coef_[1], model.intercept_],
            "deg_per_lap": round(2 * model.coef_[2] * np.mean(tyre_lives) + model.coef_[1], 3),
            "baseline_pace": round(model.intercept_, 3),
            "r_squared": round(r2_score(y, y_pred), 3),
            "sample_size": len(tyre_lives),
        }
    
    def predict_lap_time(self, curve: dict, tyre_life: int) -> float:
        """Predicts lap time for a given tyre age using fitted curve."""
        a, b, c = curve['coefficients']
        return a * tyre_life**2 + b * tyre_life + c
```

### Router Pattern
Routers handle HTTP, services handle logic.

```python
# backend/app/routers/degradation.py

from fastapi import APIRouter, HTTPException
from app.services.fastf1_client import FastF1Client
from app.services.degradation_model import DegradationModel
from app.models.schemas import DegradationResponse

router = APIRouter()
f1_client = FastF1Client()
deg_model = DegradationModel()

@router.get("/{year}/{race}", response_model=DegradationResponse)
async def get_degradation(year: int, race: str):
    """
    Get tyre degradation curves for a race.
    
    - **year**: Season year (e.g., 2023)
    - **race**: Race name (e.g., "Monza") or round number
    """
    try:
        session = f1_client.get_session(year, race, "R")
        stint_data = f1_client.extract_stint_data(session)
        
        curves = {}
        for compound in ["SOFT", "MEDIUM", "HARD"]:
            curve = deg_model.fit_compound(stint_data, compound)
            if curve:
                curves[compound] = curve
        
        if not curves:
            raise HTTPException(status_code=404, detail="No degradation data available")
        
        return DegradationResponse(
            year=year,
            race=race,
            curves=list(curves.values()),
            model_caveats="Fuel-corrected at 0.055s/lap. Traffic and track evolution not modeled."
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Pydantic Schema Pattern
Always use Pydantic for API models.

```python
# backend/app/models/schemas.py

from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Compound(str, Enum):
    SOFT = "SOFT"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    INTERMEDIATE = "INTERMEDIATE"
    WET = "WET"

class DegradationCurve(BaseModel):
    compound: Compound
    coefficients: list[float]  # [a, b, c] for ax² + bx + c
    deg_per_lap: float
    baseline_pace: float
    r_squared: float
    sample_size: int

class DegradationResponse(BaseModel):
    year: int
    race: str
    curves: list[DegradationCurve]
    model_caveats: str

class Strategy(BaseModel):
    rank: int
    name: str  # e.g., "M→H"
    stops: int
    total_time: float
    delta_to_best: float

class StrategyResponse(BaseModel):
    ranking: list[Strategy]
    explanation: str
    backtest: dict
    model_caveats: str
```

### Error Handling Pattern
Catch specific errors, provide helpful messages.

```python
class FastF1DataError(Exception):
    """Raised when FastF1 fails to load data."""
    pass

def get_session(self, year: int, race: str, session_type: str = "R"):
    """
    Load a session, trying multiple name formats.
    """
    # Try different race name formats
    names_to_try = [race, f"{race} Grand Prix", race.replace(" ", "")]
    
    for name in names_to_try:
        try:
            session = fastf1.get_session(year, name, session_type)
            session.load()
            return session
        except Exception:
            continue
    
    raise FastF1DataError(
        f"Could not load {year} {race}. "
        f"Tried: {names_to_try}. "
        f"Check race name spelling or use round number."
    )
```

---

## TypeScript Patterns (Frontend)

### API Client Pattern
Centralize all API calls with proper typing.

```typescript
// frontend/src/lib/api.ts

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DegradationCurve {
  compound: 'SOFT' | 'MEDIUM' | 'HARD';
  coefficients: [number, number, number];
  deg_per_lap: number;
  baseline_pace: number;
  r_squared: number;
  sample_size: number;
}

export interface DegradationResponse {
  year: number;
  race: string;
  curves: DegradationCurve[];
  model_caveats: string;
}

export async function fetchDegradation(year: number, race: string): Promise<DegradationResponse> {
  const res = await fetch(`${API_BASE}/api/degradation/${year}/${race}`);
  
  if (!res.ok) {
    throw new Error(`Failed to fetch degradation: ${res.statusText}`);
  }
  
  return res.json();
}
```

### React Component Pattern
Function components with TypeScript props.

```typescript
// frontend/src/components/DegradationChart.tsx

"use client";

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { DegradationCurve } from '@/lib/api';

const COMPOUND_COLORS: Record<string, string> = {
  SOFT: '#FF0000',
  MEDIUM: '#FFFF00',
  HARD: '#FFFFFF',
};

interface DegradationChartProps {
  curves: DegradationCurve[];
  maxLaps?: number;
}

export function DegradationChart({ curves, maxLaps = 40 }: DegradationChartProps) {
  // Generate chart data from polynomial coefficients
  const generateChartData = () => {
    const data = [];
    for (let lap = 1; lap <= maxLaps; lap++) {
      const point: Record<string, number> = { lap };
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
    <div className="bg-[#1A1A1A] rounded-lg p-4">
      <h3 className="text-white text-lg font-semibold mb-4">Tyre Degradation</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="lap" stroke="#888" />
          <YAxis stroke="#888" domain={['dataMin - 0.5', 'dataMax + 0.5']} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #333' }}
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
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

### Custom Hook Pattern
Encapsulate data fetching logic.

```typescript
// frontend/src/hooks/useRaceData.ts

import { useState, useEffect } from 'react';
import { fetchDegradation, fetchStrategy, DegradationResponse, StrategyResponse } from '@/lib/api';

interface UseRaceDataResult {
  degradation: DegradationResponse | null;
  strategy: StrategyResponse | null;
  loading: boolean;
  error: string | null;
}

export function useRaceData(year: number, race: string): UseRaceDataResult {
  const [degradation, setDegradation] = useState<DegradationResponse | null>(null);
  const [strategy, setStrategy] = useState<StrategyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      setError(null);
      
      try {
        const [degData, stratData] = await Promise.all([
          fetchDegradation(year, race),
          fetchStrategy(year, race),
        ]);
        
        setDegradation(degData);
        setStrategy(stratData);
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    }
    
    loadData();
  }, [year, race]);

  return { degradation, strategy, loading, error };
}
```

### Loading State Pattern
Always show loading and error states.

```typescript
// Example usage in page component

export default function StrategyPage() {
  const [year, setYear] = useState(2023);
  const [race, setRace] = useState('Monza');
  const { degradation, strategy, loading, error } = useRaceData(year, race);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-400">Loading race data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500 rounded-lg p-4">
        <p className="text-red-400">Error: {error}</p>
      </div>
    );
  }

  return (
    <div>
      {degradation && <DegradationChart curves={degradation.curves} />}
      {strategy && <StrategyRanking ranking={strategy.ranking} />}
    </div>
  );
}
```

---

## Naming Conventions

### Python
- **Files:** snake_case (`degradation_model.py`)
- **Classes:** PascalCase (`DegradationModel`)
- **Functions:** snake_case (`fit_compound()`)
- **Constants:** UPPER_SNAKE_CASE (`FUEL_EFFECT_PER_LAP`)

### TypeScript
- **Files:** PascalCase for components (`DegradationChart.tsx`), camelCase for utils (`api.ts`)
- **Components:** PascalCase (`DegradationChart`)
- **Functions:** camelCase (`fetchDegradation`)
- **Interfaces:** PascalCase (`DegradationResponse`)
- **Constants:** UPPER_SNAKE_CASE or camelCase (`COMPOUND_COLORS`)

---

## Commenting Style

### Python Docstrings
```python
def calculate_strategy(deg_curves: dict, total_laps: int) -> list[dict]:
    """
    What: Simulates and ranks pit strategies
    Why: Core value proposition - tells user optimal strategy
    
    Args:
        deg_curves: Degradation data per compound
        total_laps: Race length
        
    Returns:
        List of strategies ranked by total time
        
    Limitations:
        - Does not account for safety car
        - Does not model undercut/overcut dynamics
    """
```

### TypeScript JSDoc
```typescript
/**
 * Renders tyre degradation curves for visual comparison.
 * 
 * @param curves - Array of curve data from API
 * @param maxLaps - Maximum stint length to display (default: 40)
 */
```

---

## File Organization

### Keep Related Code Together
```
backend/app/services/
├── __init__.py
├── fastf1_client.py      # All FastF1 interactions
├── degradation_model.py  # Deg calculation only
├── strategy_engine.py    # Strategy simulation only
└── overtake_analyzer.py  # Overtake analysis only
```

### One Component Per File
```
frontend/src/components/
├── DegradationChart.tsx
├── StrategyRanking.tsx
├── PitWindowChart.tsx
├── OvertakeMap.tsx
└── BacktestDisplay.tsx
```
