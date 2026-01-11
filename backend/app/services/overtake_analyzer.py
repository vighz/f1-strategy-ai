"""
Overtake zone analyzer service.

Identifies potential overtaking zones based on speed differentials
across the track.
"""
from typing import Dict

import fastf1


class OvertakeAnalyzer:
    """
    Analyzes telemetry to identify overtaking zones.

    Approach:
    1. Extract position and speed data across track
    2. Identify zones with high speed variance (accel/braking zones)
    3. Detect DRS zones from telemetry
    4. Rank zones by overtaking potential
    """

    MIN_SPEED_DELTA = 50  # km/h minimum delta to consider a zone
    ZONE_DISTANCE_THRESHOLD = 100  # meters - group nearby points

    def analyze_session(self, session: fastf1.core.Session) -> Dict[str, any]:
        """
        Analyze a session to find overtaking zones.

        Args:
            session: Loaded FastF1 session with telemetry

        Returns:
            Dictionary with zones and statistics
        """
        if session is None or session.laps is None:
            return {"zones": [], "total_overtakes": 0}

        # For Phase 2, we'll create a simplified version
        # that returns demo data based on typical Monza characteristics

        # Monza has 3 main overtaking zones:
        # 1. Turn 1 (end of main straight)
        # 2. Turn 4 (Lesmo braking zone)
        # 3. Variante Ascari

        zones = [
            {
                "zone_id": 1,
                "distance_start": 0,
                "distance_end": 200,
                "avg_speed_delta": 180.5,
                "overtake_count": 12,
                "difficulty": "Easy",
                "has_drs": True,
            },
            {
                "zone_id": 2,
                "distance_start": 1500,
                "distance_end": 1650,
                "avg_speed_delta": 95.3,
                "overtake_count": 5,
                "difficulty": "Medium",
                "has_drs": False,
            },
            {
                "zone_id": 3,
                "distance_start": 3800,
                "distance_end": 3950,
                "avg_speed_delta": 110.7,
                "overtake_count": 8,
                "difficulty": "Medium",
                "has_drs": True,
            },
        ]

        total_overtakes = sum(zone["overtake_count"] for zone in zones)

        return {
            "zones": zones,
            "total_overtakes": total_overtakes,
        }

    def _classify_difficulty(self, speed_delta: float) -> str:
        """
        Classify overtaking difficulty based on speed differential.

        Args:
            speed_delta: Average speed difference in km/h

        Returns:
            Difficulty level: Easy, Medium, or Hard
        """
        if speed_delta > 150:
            return "Easy"
        elif speed_delta > 80:
            return "Medium"
        else:
            return "Hard"
