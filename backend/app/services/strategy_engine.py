"""
Strategy simulation engine.

Generates viable pit strategies and predicts race time for each using
the degradation model.
"""
from itertools import combinations_with_replacement
from typing import Dict, List, Optional

from app.services.degradation_model import DegradationModel


class StrategyEngine:
    """
    Simulates and ranks pit stop strategies.

    Approach:
    1. Generate all viable strategies (0-stop, 1-stop, 2-stop, 3-stop)
    2. For each strategy, simulate lap-by-lap tire degradation
    3. Sum total race time including pit losses
    4. Rank by predicted finish time
    """

    def __init__(self, degradation_model: DegradationModel):
        """
        Initialize strategy engine with a degradation model.

        Args:
            degradation_model: Fitted DegradationModel instance
        """
        self.deg_model = degradation_model

    def simulate_strategies(
        self,
        degradation_curves: List[Dict],
        total_laps: int,
        pit_loss_seconds: float,
        max_stops: int = 3,
    ) -> List[Dict]:
        """
        Generate and simulate all viable strategies.

        Args:
            degradation_curves: List of fitted degradation curves by compound
            total_laps: Total race distance in laps
            pit_loss_seconds: Time lost per pit stop
            max_stops: Maximum pit stops to consider

        Returns:
            List of strategies ranked by predicted time (fastest first)
        """
        # Convert curves to dict for easier lookup
        curves_dict = {curve["compound"]: curve for curve in degradation_curves}

        available_compounds = list(curves_dict.keys())

        if not available_compounds:
            return []

        strategies = []

        # Generate strategies for 0 to max_stops
        for num_stops in range(0, max_stops + 1):
            # Generate compound combinations
            # For n stops, we have n+1 stints
            num_stints = num_stops + 1

            for compounds in combinations_with_replacement(
                available_compounds, num_stints
            ):
                # Skip invalid strategies (must use at least 2 compounds in dry race)
                if num_stops > 0 and len(set(compounds)) < 2:
                    continue

                strategy = self._simulate_strategy(
                    list(compounds),
                    curves_dict,
                    total_laps,
                    pit_loss_seconds,
                    num_stops,
                )

                if strategy:
                    strategies.append(strategy)

        # Sort by predicted time
        strategies.sort(key=lambda s: s["predicted_time"])

        # Calculate deltas from fastest
        if strategies:
            fastest_time = strategies[0]["predicted_time"]
            for strategy in strategies:
                strategy["time_delta"] = strategy["predicted_time"] - fastest_time

        return strategies

    def _simulate_strategy(
        self,
        compounds: List[str],
        curves_dict: Dict[str, Dict],
        total_laps: int,
        pit_loss_seconds: float,
        num_stops: int,
    ) -> Optional[Dict]:
        """
        Simulate a single strategy lap-by-lap.

        Args:
            compounds: List of compounds for each stint (length = num_stops + 1)
            curves_dict: Degradation curves indexed by compound
            total_laps: Total race laps
            pit_loss_seconds: Pit stop time loss
            num_stops: Number of pit stops

        Returns:
            Strategy dict with predicted time, or None if invalid
        """
        # Distribute laps across stints (simple equal distribution for now)
        laps_per_stint = [total_laps // len(compounds)] * len(compounds)

        # Add remaining laps to last stint
        remaining = total_laps - sum(laps_per_stint)
        laps_per_stint[-1] += remaining

        # Simulate lap-by-lap
        total_time = 0.0
        current_lap = 1
        pit_stops = []
        stints = []

        for stint_idx, (compound, stint_length) in enumerate(
            zip(compounds, laps_per_stint)
        ):
            if compound not in curves_dict:
                return None

            curve = curves_dict[compound]
            coefficients = curve["coefficients"]

            stint_start = current_lap
            stint_end = current_lap + stint_length - 1

            # Add pit stop if not first stint
            if stint_idx > 0:
                total_time += pit_loss_seconds
                pit_stops.append(
                    {
                        "lap": current_lap,
                        "compound_before": compounds[stint_idx - 1],
                        "compound_after": compound,
                    }
                )

            # Simulate each lap in this stint
            for tyre_life in range(1, stint_length + 1):
                lap_time = self.deg_model.predict_lap_time(
                    tyre_life, coefficients, current_lap
                )
                total_time += lap_time
                current_lap += 1

            stints.append(
                {
                    "compound": compound,
                    "start_lap": stint_start,
                    "end_lap": stint_end,
                    "laps": stint_length,
                }
            )

        # Create strategy name
        compound_str = "-".join(compounds)
        strategy_name = f"{compound_str} ({num_stops}-stop)"

        return {
            "strategy_name": strategy_name,
            "stops": num_stops,
            "pit_stops": pit_stops,
            "stints": stints,
            "predicted_time": total_time,
            "time_delta": 0.0,  # Will be calculated later
        }
