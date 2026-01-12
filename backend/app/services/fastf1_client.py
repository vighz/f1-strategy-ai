"""
FastF1 client service for extracting F1 telemetry data.

This service handles all interactions with the FastF1 library,
including session loading, data extraction, and filtering.
"""
import gc
from typing import Dict, List, Optional

import fastf1
from app.config import FASTF1_CACHE_DIR


class FastF1Client:
    """Client for fetching and processing F1 telemetry data."""

    def __init__(self):
        """Initialize FastF1 client and enable caching."""
        # CRITICAL: Enable cache BEFORE any session loads
        fastf1.Cache.enable_cache(FASTF1_CACHE_DIR)

    def load_session(
        self, year: int, race_name: str, session_type: str = "R"
    ) -> Optional[fastf1.core.Session]:
        """
        Load a specific F1 session with memory-efficient settings.

        Args:
            year: Race year (e.g., 2023)
            race_name: Race name, can be:
                - Circuit name: "Monza"
                - GP name: "Italian Grand Prix"
                - Round number: 14
            session_type: Session identifier:
                - "R" = Race
                - "Q" = Qualifying
                - "FP1", "FP2", "FP3" = Practice sessions
                - "S" = Sprint

        Returns:
            Loaded session object, or None if loading fails

        Note:
            First load can take 30-60 seconds as data is downloaded.
            Subsequent loads are faster due to caching.
            Memory-optimized to load only laps data (not full telemetry).
        """
        try:
            session = fastf1.get_session(year, race_name, session_type)
            # MEMORY OPTIMIZATION: Only load laps, not full telemetry
            # This reduces memory usage from ~1200MB to ~200-300MB
            session.load(laps=True, telemetry=False, weather=False, messages=False)

            # Force garbage collection after loading to free memory
            gc.collect()

            return session
        except Exception as e:
            print(f"Error loading session {year} {race_name} {session_type}: {e}")
            return None

    def get_race_laps(self, session: fastf1.core.Session) -> dict:
        """
        Extract lap data from a race session.

        Args:
            session: Loaded FastF1 session

        Returns:
            Dictionary with lap data including:
            - driver
            - lap_number
            - lap_time
            - compound
            - tyre_life
            - is_personal_best
        """
        if session is None or session.laps is None:
            return {"laps": [], "total_laps": 0}

        # Use pick_quicklaps() to filter outliers (pit laps, traffic, etc.)
        quick_laps = session.laps.pick_quicklaps()

        laps_data = []
        for _, lap in quick_laps.iterrows():
            laps_data.append(
                {
                    "driver": lap["Driver"],
                    "lap_number": int(lap["LapNumber"]),
                    "lap_time": (
                        float(lap["LapTime"].total_seconds())
                        if lap["LapTime"] is not None
                        else None
                    ),
                    "compound": lap["Compound"],
                    "tyre_life": int(lap["TyreLife"]) if lap["TyreLife"] else None,
                    "is_personal_best": bool(lap["IsPersonalBest"]),
                }
            )

        # Free memory after processing
        del quick_laps
        gc.collect()

        return {"laps": laps_data, "total_laps": len(laps_data)}

    def get_stint_data(self, session: fastf1.core.Session, driver: str) -> List[Dict]:
        """
        Extract stint data for a specific driver.

        A stint is a continuous set of laps on the same set of tyres.

        Args:
            session: Loaded FastF1 session
            driver: Driver code (e.g., "VER", "HAM", "LEC")

        Returns:
            List of stints, each containing:
            - stint_number
            - compound
            - start_lap
            - end_lap
            - laps (list of lap times)
        """
        if session is None or session.laps is None:
            return []

        driver_laps = session.laps.pick_driver(driver).pick_quicklaps()

        stints = []
        current_stint = None
        stint_number = 0

        for _, lap in driver_laps.iterrows():
            compound = lap["Compound"]
            lap_time = (
                float(lap["LapTime"].total_seconds())
                if lap["LapTime"] is not None
                else None
            )
            tyre_life = int(lap["TyreLife"]) if lap["TyreLife"] else None

            # Start new stint if compound changed or first lap
            if current_stint is None or current_stint["compound"] != compound:
                if current_stint is not None:
                    stints.append(current_stint)

                stint_number += 1
                current_stint = {
                    "stint_number": stint_number,
                    "compound": compound,
                    "start_lap": int(lap["LapNumber"]),
                    "end_lap": int(lap["LapNumber"]),
                    "laps": [{"lap_time": lap_time, "tyre_life": tyre_life}],
                }
            else:
                # Continue current stint
                current_stint["end_lap"] = int(lap["LapNumber"])
                current_stint["laps"].append(
                    {"lap_time": lap_time, "tyre_life": tyre_life}
                )

        # Add final stint
        if current_stint is not None:
            stints.append(current_stint)

        # Free memory after processing
        del driver_laps
        gc.collect()

        return stints
