"""
Strategy simulation API endpoint.
"""
from app.config import PIT_LOSS
from app.models.schemas import StrategyRequest, StrategyResponse
from app.services.degradation_model import DegradationModel
from app.services.fastf1_client import FastF1Client
from app.services.strategy_engine import StrategyEngine
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/strategy", tags=["strategy"])


@router.post("", response_model=StrategyResponse)
async def simulate_strategies(request: StrategyRequest):
    """
    Simulate and rank pit stop strategies.

    Returns all viable strategies ranked by predicted finish time,
    using degradation model to estimate lap times.
    """
    # Load session
    client = FastF1Client()
    session = client.load_session(request.year, request.race, request.session)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {request.year} {request.race} {request.session}",
        )

    # Get total laps
    total_laps = request.total_laps or int(session.laps["LapNumber"].max())

    # Get pit loss time
    circuit_name = session.event.get("Location", "default")
    pit_loss = request.pit_loss_seconds or PIT_LOSS.get(
        circuit_name, PIT_LOSS["default"]
    )

    # Get stint data and fit degradation model
    all_drivers = session.laps["Driver"].unique()
    all_stints = {}

    for driver in all_drivers:
        stints = client.get_stint_data(session, driver)
        if stints:
            all_stints[driver] = stints

    if not all_stints:
        raise HTTPException(
            status_code=500, detail="No stint data available for analysis"
        )

    model = DegradationModel()
    curves = model.analyze_race(all_stints)

    if not curves:
        raise HTTPException(
            status_code=500, detail="Could not generate degradation curves"
        )

    # Simulate strategies
    engine = StrategyEngine(model)
    strategies = engine.simulate_strategies(curves, total_laps, pit_loss, max_stops=2)

    if not strategies:
        raise HTTPException(status_code=500, detail="Could not simulate strategies")

    return StrategyResponse(
        race_name=session.event["EventName"],
        year=request.year,
        total_laps=total_laps,
        pit_loss_seconds=pit_loss,
        strategies=strategies,
        fastest_strategy=strategies[0]["strategy_name"],
    )
