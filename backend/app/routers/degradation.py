"""
Degradation analysis API endpoint.
"""
from app.models.schemas import DegradationRequest, DegradationResponse
from app.services.degradation_model import DegradationModel
from app.services.fastf1_client import FastF1Client
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/degradation", tags=["degradation"])


@router.post("", response_model=DegradationResponse)
async def analyze_degradation(request: DegradationRequest):
    """
    Analyze tyre degradation for a race.

    Returns degradation curves for each compound with coefficients,
    degradation rate, and goodness-of-fit metrics.
    """
    # Load session
    client = FastF1Client()
    session = client.load_session(request.year, request.race, request.session)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {request.year} {request.race} {request.session}",
        )

    # Get stint data for all drivers
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

    # Fit degradation model
    model = DegradationModel()
    curves = model.analyze_race(all_stints)

    if not curves:
        raise HTTPException(
            status_code=500, detail="Could not generate degradation curves"
        )

    return DegradationResponse(
        race_name=session.event["EventName"],
        year=request.year,
        curves=curves,
        fuel_effect_per_lap=DegradationModel.FUEL_EFFECT_PER_LAP,
    )
