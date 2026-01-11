"""Test script for DegradationModel service."""
import sys

sys.path.insert(0, ".")

from app.services.degradation_model import DegradationModel  # noqa: E402
from app.services.fastf1_client import FastF1Client  # noqa: E402

print("Testing DegradationModel with Monza 2023...")
print("Loading session data (may take 30s if not cached)...\n")

# Load Monza 2023
client = FastF1Client()
session = client.load_session(2023, "Monza", "R")

if not session:
    print("FAILED: Could not load session")
    sys.exit(1)

print(f"SUCCESS: Loaded {session.event['EventName']}")

# Get stint data for all drivers
print("\nExtracting stint data for all drivers...")
all_drivers = session.laps["Driver"].unique()
print(f"Found {len(all_drivers)} drivers")

all_stints = {}
for driver in all_drivers:
    stints = client.get_stint_data(session, driver)
    if stints:
        all_stints[driver] = stints

print(f"Collected stints from {len(all_stints)} drivers")

# Fit degradation model
print("\nFitting degradation curves...")
model = DegradationModel()
curves = model.analyze_race(all_stints)

if not curves:
    print("FAILED: No degradation curves generated")
    sys.exit(1)

print(f"\nSUCCESS: Generated {len(curves)} degradation curves")
print("\n" + "=" * 70)

for curve in curves:
    print(f"\n{curve['compound']} Compound:")
    print(f"  Coefficients (a, b, c): {[f'{c:.6f}' for c in curve['coefficients']]}")
    print(f"  Degradation per lap: {curve['deg_per_lap']:.4f} seconds/lap")
    print(f"  R² score: {curve['r_squared']:.4f}")
    print(f"  Sample size: {curve['sample_size']} laps")

    # Test prediction
    predicted_lap1 = model.predict_lap_time(1, curve["coefficients"], lap_number=10)
    predicted_lap20 = model.predict_lap_time(20, curve["coefficients"], lap_number=30)

    print(f"\n  Sample predictions:")
    print(f"    Lap 1 on tyres: {predicted_lap1:.3f}s")
    print(f"    Lap 20 on tyres: {predicted_lap20:.3f}s")
    print(f"    Delta: +{predicted_lap20 - predicted_lap1:.3f}s")

print("\n" + "=" * 70)
print("\nDegradation model working correctly!")
