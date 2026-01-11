"""
Races listing API endpoint.
"""
import fastf1
from app.config import FASTF1_CACHE_DIR
from app.models.schemas import RaceInfo, RacesResponse
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/races", tags=["races"])


@router.get("/{year}", response_model=RacesResponse)
async def list_races(year: int):
    """
    List all races for a given season.

    Returns race calendar with names, dates, and locations.
    """
    try:
        # Enable cache
        fastf1.Cache.enable_cache(FASTF1_CACHE_DIR)

        # Get schedule
        schedule = fastf1.get_event_schedule(year)

        races = []
        for _, event in schedule.iterrows():
            # Only include actual race events (skip testing)
            if event.get("EventFormat") != "testing":
                races.append(
                    RaceInfo(
                        year=year,
                        round_number=int(event["RoundNumber"]),
                        race_name=event["EventName"],
                        circuit_name=event.get("Location", "Unknown"),
                        country=event.get("Country", "Unknown"),
                        date=str(event["EventDate"]),
                    )
                )

        return RacesResponse(season=year, races=races)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Could not fetch race schedule: {str(e)}"
        )
