"""
Pydantic models for API request/response validation.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# ============================================================================
# Common Models
# ============================================================================


class LapData(BaseModel):
    """Single lap telemetry data."""

    driver: str
    lap_number: int
    lap_time: Optional[float] = None
    compound: str
    tyre_life: Optional[int] = None
    is_personal_best: bool


class StintLap(BaseModel):
    """Single lap within a stint."""

    lap_time: Optional[float]
    tyre_life: Optional[int]


class Stint(BaseModel):
    """Continuous set of laps on same tyres."""

    stint_number: int
    compound: str
    start_lap: int
    end_lap: int
    laps: List[StintLap]


# ============================================================================
# Degradation Endpoint
# ============================================================================


class DegradationRequest(BaseModel):
    """Request for degradation analysis."""

    year: int = Field(..., ge=2018, le=2030, description="Race year")
    race: str = Field(..., description="Race name or circuit (e.g., 'Monza')")
    session: str = Field(
        default="R", description="Session type: R, Q, FP1, FP2, FP3, S"
    )


class DegradationCurve(BaseModel):
    """Degradation curve for a single compound."""

    compound: str
    coefficients: List[float] = Field(
        ..., description="Polynomial coefficients [a, b, c] for ax²+bx+c"
    )
    deg_per_lap: float = Field(
        ..., description="Average degradation in seconds per lap"
    )
    r_squared: float = Field(..., description="R² goodness of fit (0-1)")
    sample_size: int = Field(..., description="Number of laps used for fitting")


class DegradationResponse(BaseModel):
    """Response with degradation curves for all compounds."""

    race_name: str
    year: int
    curves: List[DegradationCurve]
    fuel_effect_per_lap: float = Field(
        ..., description="Fuel effect correction applied (seconds)"
    )


# ============================================================================
# Strategy Endpoint
# ============================================================================


class StrategyRequest(BaseModel):
    """Request for strategy simulation."""

    year: int = Field(..., ge=2018, le=2030)
    race: str
    session: str = Field(default="R")
    total_laps: Optional[int] = Field(
        default=None, description="Total race laps (auto-detected if None)"
    )
    pit_loss_seconds: Optional[float] = Field(
        default=None, description="Pit stop time loss (uses circuit default if None)"
    )


class PitStop(BaseModel):
    """Single pit stop in a strategy."""

    lap: int
    compound_before: str
    compound_after: str


class Strategy(BaseModel):
    """Complete race strategy."""

    strategy_name: str = Field(..., description="e.g., 'MEDIUM-HARD (1-stop)'")
    stops: int = Field(..., description="Number of pit stops")
    pit_stops: List[PitStop]
    stints: List[Dict[str, Any]] = Field(
        ..., description="Stint details with compound and lap range"
    )
    predicted_time: float = Field(..., description="Total race time in seconds")
    time_delta: float = Field(..., description="Delta to fastest strategy in seconds")


class StrategyResponse(BaseModel):
    """Response with ranked strategies."""

    race_name: str
    year: int
    total_laps: int
    pit_loss_seconds: float
    strategies: List[Strategy] = Field(
        ..., description="Strategies ranked by predicted time"
    )
    fastest_strategy: str


# ============================================================================
# Overtake Endpoint
# ============================================================================


class OvertakeRequest(BaseModel):
    """Request for overtake zone analysis."""

    year: int = Field(..., ge=2018, le=2030)
    race: str
    session: str = Field(default="R")


class OvertakeZone(BaseModel):
    """Single overtaking opportunity zone."""

    zone_id: int
    distance_start: float = Field(..., description="Track distance in meters")
    distance_end: float = Field(..., description="Track distance in meters")
    avg_speed_delta: float = Field(
        ..., description="Average speed differential in km/h"
    )
    overtake_count: int = Field(
        ..., description="Number of overtakes observed in this zone"
    )
    difficulty: str = Field(..., description="Easy, Medium, Hard based on speed delta")
    has_drs: bool = Field(..., description="DRS zone detected")


class OvertakeResponse(BaseModel):
    """Response with overtake zones."""

    race_name: str
    year: int
    zones: List[OvertakeZone]
    total_overtakes: int


# ============================================================================
# Races Endpoint
# ============================================================================


class RaceInfo(BaseModel):
    """Information about a single race."""

    year: int
    round_number: int
    race_name: str
    circuit_name: str
    country: str
    date: str


class RacesResponse(BaseModel):
    """Response with available races."""

    season: int
    races: List[RaceInfo]
