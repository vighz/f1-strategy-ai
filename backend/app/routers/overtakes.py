"""
Overtake zone analysis API endpoint.
"""
from app.models.schemas import OvertakeRequest, OvertakeResponse
from app.services.fastf1_client import FastF1Client
from app.services.overtake_analyzer import OvertakeAnalyzer
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/overtakes", tags=["overtakes"])


@router.post("", response_model=OvertakeResponse)
async def analyze_overtakes(request: OvertakeRequest):
    """
    Analyze overtaking zones for a race.

    Returns identified overtaking zones with speed deltas,
    overtake counts, and difficulty ratings.
    """
    # Load session
    client = FastF1Client()
    session = client.load_session(request.year, request.race, request.session)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session not found: {request.year} {request.race} {request.session}",
        )

    # Analyze overtaking zones
    analyzer = OvertakeAnalyzer()
    result = analyzer.analyze_session(session)

    return OvertakeResponse(
        race_name=session.event["EventName"],
        year=request.year,
        zones=result["zones"],
        total_overtakes=result["total_overtakes"],
    )
