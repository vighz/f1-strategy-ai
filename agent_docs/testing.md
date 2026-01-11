# Testing Strategy

## Overview
Focus on testing the core business logic (services layer). Mock FastF1 in unit tests to avoid slow data loads.

---

## Test Types

### Unit Tests (Backend)
**Tool:** pytest  
**Focus:** Services layer (degradation_model, strategy_engine, overtake_analyzer)

```bash
cd backend
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_degradation.py  # Single file
pytest -k "test_fit"      # Tests matching pattern
```

### Integration Tests (Backend)
**Tool:** pytest + httpx  
**Focus:** API endpoints return correct data

```bash
pytest tests/test_api.py
```

### Manual Testing (Frontend)
**Focus:** Visual output, user interactions

**Checklist:**
- [ ] Race selector loads options
- [ ] Deg chart renders with correct colors
- [ ] Strategy ranking shows reasonable results
- [ ] Loading states appear
- [ ] Error states display correctly

### End-to-End (Optional)
**Tool:** Playwright or manual browser testing  
**Focus:** Full user journey

---

## Test File Structure

```
backend/tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_degradation.py   # DegradationModel tests
├── test_strategy.py      # StrategyEngine tests
├── test_overtakes.py     # OvertakeAnalyzer tests
└── test_api.py           # API endpoint tests
```

---

## Example Tests

### Testing DegradationModel

```python
# backend/tests/test_degradation.py

import pytest
from app.services.degradation_model import DegradationModel

@pytest.fixture
def sample_stint_data():
    """Mock stint data for testing without FastF1."""
    return [
        {
            "driver": "VER",
            "stint": 1,
            "compound": "MEDIUM",
            "laps": [
                {"lap_number": 1, "lap_time": 82.5, "tyre_life": 1},
                {"lap_number": 2, "lap_time": 82.6, "tyre_life": 2},
                {"lap_number": 3, "lap_time": 82.8, "tyre_life": 3},
                {"lap_number": 4, "lap_time": 83.0, "tyre_life": 4},
                {"lap_number": 5, "lap_time": 83.3, "tyre_life": 5},
            ]
        },
        {
            "driver": "HAM",
            "stint": 1,
            "compound": "MEDIUM",
            "laps": [
                {"lap_number": 1, "lap_time": 82.4, "tyre_life": 1},
                {"lap_number": 2, "lap_time": 82.5, "tyre_life": 2},
                {"lap_number": 3, "lap_time": 82.7, "tyre_life": 3},
            ]
        }
    ]

class TestDegradationModel:
    def test_fit_compound_returns_dict(self, sample_stint_data):
        """Model should return dict with expected keys."""
        model = DegradationModel()
        result = model.fit_compound(sample_stint_data, "MEDIUM")
        
        assert result is not None
        assert "compound" in result
        assert "coefficients" in result
        assert "deg_per_lap" in result
        assert "r_squared" in result
    
    def test_fit_compound_missing_data_returns_none(self, sample_stint_data):
        """Should return None if compound not in data."""
        model = DegradationModel()
        result = model.fit_compound(sample_stint_data, "SOFT")
        
        assert result is None
    
    def test_predict_lap_time_increases(self, sample_stint_data):
        """Lap times should increase with tyre age."""
        model = DegradationModel()
        curve = model.fit_compound(sample_stint_data, "MEDIUM")
        
        time_lap_1 = model.predict_lap_time(curve, 1)
        time_lap_10 = model.predict_lap_time(curve, 10)
        
        assert time_lap_10 > time_lap_1
    
    def test_r_squared_reasonable(self, sample_stint_data):
        """R² should be between 0 and 1."""
        model = DegradationModel()
        curve = model.fit_compound(sample_stint_data, "MEDIUM")
        
        assert 0 <= curve["r_squared"] <= 1
```

### Testing StrategyEngine

```python
# backend/tests/test_strategy.py

import pytest
from app.services.strategy_engine import StrategyEngine
from app.services.degradation_model import DegradationModel

@pytest.fixture
def mock_deg_curves():
    """Pre-computed deg curves for testing."""
    return {
        "MEDIUM": {
            "compound": "MEDIUM",
            "coefficients": [0.005, 0.05, 82.0],
            "deg_per_lap": 0.1,
            "baseline_pace": 82.0,
            "r_squared": 0.9,
        },
        "HARD": {
            "compound": "HARD",
            "coefficients": [0.003, 0.03, 82.5],
            "deg_per_lap": 0.06,
            "baseline_pace": 82.5,
            "r_squared": 0.85,
        }
    }

class TestStrategyEngine:
    def test_generate_strategies_creates_options(self, mock_deg_curves):
        """Should generate multiple strategy options."""
        engine = StrategyEngine(DegradationModel())
        strategies = engine.generate_strategies(
            total_laps=50,
            available_compounds=["MEDIUM", "HARD"]
        )
        
        assert len(strategies) > 0
        assert any(s["stops"] == 1 for s in strategies)
    
    def test_simulate_strategy_returns_total_time(self, mock_deg_curves):
        """Simulation should return total race time."""
        engine = StrategyEngine(DegradationModel())
        strategy = {
            "name": "M→H",
            "stops": 1,
            "stints": [
                {"compound": "MEDIUM", "start": 1, "end": 25},
                {"compound": "HARD", "start": 26, "end": 50}
            ],
            "pit_laps": [25]
        }
        
        result = engine.simulate_strategy(strategy, mock_deg_curves, pit_loss=22.0)
        
        assert result is not None
        assert "total_time" in result
        assert result["total_time"] > 0
    
    def test_ranking_orders_by_time(self, mock_deg_curves):
        """Strategies should be ranked fastest first."""
        engine = StrategyEngine(DegradationModel())
        # Run full ranking logic
        # Assert ranking[0]["total_time"] <= ranking[1]["total_time"]
```

### Testing API Endpoints

```python
# backend/tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/api/health")
        assert response.status_code == 200

class TestDegradationEndpoint:
    def test_invalid_race_returns_error(self):
        """Should return 404 or 500 for unknown race."""
        response = client.get("/api/degradation/2023/FakeRace")
        assert response.status_code in [404, 500]
    
    # Note: Testing with real data requires FastF1 cache
    # Consider mocking the FastF1 client for CI/CD
```

---

## Pre-Commit Hooks

### Setup (Optional but Recommended)
```bash
pip install pre-commit
pre-commit install
```

### .pre-commit-config.yaml
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
      
      - id: black
        name: black
        entry: black --check
        language: system
        types: [python]
      
      - id: eslint
        name: eslint
        entry: npm run lint --prefix frontend
        language: system
        types: [typescript, javascript]
        pass_filenames: false
```

---

## Verification Loop

After implementing each feature:

1. **Run unit tests:**
   ```bash
   cd backend && pytest -v
   ```

2. **Start dev servers:**
   ```bash
   # Terminal 1
   cd backend && uvicorn app.main:app --reload
   
   # Terminal 2
   cd frontend && npm run dev
   ```

3. **Manual check:**
   - Open http://localhost:3000
   - Select Monza 2023
   - Verify feature works as expected

4. **Fix any issues before continuing**

---

## What to Test vs. Skip

### MUST Test
- DegradationModel calculations
- StrategyEngine simulation logic
- API response schemas
- Error handling paths

### CAN Skip (for MVP)
- FastF1 data fetching (it's a third-party library)
- UI visual appearance (manual check instead)
- Performance benchmarks

---

## CI/CD (Future)

For GitHub Actions (not required for MVP):

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest
```

---

## Manual Testing Checklist

### Before Each Milestone
- [ ] App starts without errors
- [ ] Can select Monza 2023 from dropdown
- [ ] Deg curves render (if implemented)
- [ ] Strategy ranking shows (if implemented)
- [ ] Overtake map displays (if implemented)
- [ ] No console errors in browser
- [ ] API returns valid JSON

### Before Deployment
- [ ] All features work with hero race
- [ ] Dark theme applied
- [ ] Model caveats visible
- [ ] Error states handled
- [ ] Loading states shown
- [ ] Mobile doesn't completely break
