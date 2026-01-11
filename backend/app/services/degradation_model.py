"""
Tyre degradation modeling service.

Uses polynomial regression to model lap time degradation as a function
of tyre age, accounting for fuel load reduction.
"""
from typing import Dict, List, Optional

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures


class DegradationModel:
    """
    Models tyre degradation using polynomial regression.

    Approach: lap_time = a*(tyre_life)² + b*(tyre_life) + c

    The model:
    1. Filters stints by compound
    2. Corrects lap times for fuel load (lighter car = faster laps)
    3. Fits 2nd-degree polynomial to (tyre_life, corrected_lap_time)
    4. Returns coefficients and goodness-of-fit metrics
    """

    FUEL_EFFECT_PER_LAP = 0.055  # seconds per lap (fuel burn makes car faster)
    MIN_LAPS_FOR_FITTING = 5  # Minimum laps needed to fit a curve

    def analyze_race(
        self, all_driver_stints: Dict[str, List[Dict]]
    ) -> List[Dict[str, any]]:
        """
        Analyze degradation for all compounds across all drivers.

        Args:
            all_driver_stints: Dict mapping driver code to list of stint objects
                               e.g., {"VER": [{stint1}, {stint2}], "HAM": [...]}

        Returns:
            List of degradation curves, one per compound with enough data
        """
        # Aggregate all stints by compound
        compound_data = {"SOFT": [], "MEDIUM": [], "HARD": []}

        for driver_stints in all_driver_stints.values():
            for stint in driver_stints:
                compound = stint.get("compound")
                if compound in compound_data:
                    compound_data[compound].extend(stint.get("laps", []))

        # Fit curves for each compound with sufficient data
        curves = []
        for compound, laps in compound_data.items():
            if len(laps) >= self.MIN_LAPS_FOR_FITTING:
                curve = self.fit_compound(laps, compound)
                if curve:
                    curves.append(curve)

        return curves

    def fit_compound(self, laps: List[Dict], compound: str) -> Optional[Dict[str, any]]:
        """
        Fit degradation curve for a single compound.

        Args:
            laps: List of lap objects with lap_time and tyre_life
            compound: Compound name (SOFT, MEDIUM, HARD)

        Returns:
            Dictionary with coefficients and metrics, or None if fitting fails
        """
        # Extract and filter valid data points
        tyre_lives = []
        lap_times = []

        for i, lap in enumerate(laps):
            if lap.get("lap_time") and lap.get("tyre_life"):
                tyre_life = lap["tyre_life"]
                lap_time = lap["lap_time"]

                # Apply fuel correction: earlier laps had more fuel
                fuel_correction = i * self.FUEL_EFFECT_PER_LAP
                corrected_time = lap_time + fuel_correction

                tyre_lives.append(tyre_life)
                lap_times.append(corrected_time)

        if len(tyre_lives) < self.MIN_LAPS_FOR_FITTING:
            return None

        # Fit 2nd-degree polynomial
        X = np.array(tyre_lives).reshape(-1, 1)
        y = np.array(lap_times)

        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)

        model = LinearRegression()
        model.fit(X_poly, y)

        # Get predictions and calculate R²
        y_pred = model.predict(X_poly)
        r2 = r2_score(y, y_pred)

        # Extract coefficients: [intercept, linear, quadratic]
        # Note: sklearn PolynomialFeatures creates [1, x, x²]
        coefficients = [
            model.coef_[2],  # quadratic (a)
            model.coef_[1],  # linear (b)
            model.intercept_,  # intercept (c)
        ]

        # Calculate average degradation per lap
        # Use derivative at midpoint of tyre life range
        mid_life = (max(tyre_lives) + min(tyre_lives)) / 2
        deg_per_lap = 2 * coefficients[0] * mid_life + coefficients[1]

        return {
            "compound": compound,
            "coefficients": coefficients,
            "deg_per_lap": float(deg_per_lap),
            "r_squared": float(r2),
            "sample_size": len(tyre_lives),
        }

    def predict_lap_time(
        self, tyre_life: int, coefficients: List[float], lap_number: int = 0
    ) -> float:
        """
        Predict lap time given tyre age and degradation coefficients.

        Args:
            tyre_life: Age of tyres in laps
            coefficients: [a, b, c] from polynomial fit
            lap_number: Current lap (for fuel correction)

        Returns:
            Predicted lap time in seconds
        """
        a, b, c = coefficients

        # Apply degradation model
        predicted_time = a * (tyre_life**2) + b * tyre_life + c

        # Remove fuel correction (car gets lighter as race progresses)
        fuel_correction = lap_number * self.FUEL_EFFECT_PER_LAP
        predicted_time -= fuel_correction

        return predicted_time
