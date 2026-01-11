"""Test script for StrategyEngine service."""
import sys

sys.path.insert(0, ".")

from app.config import PIT_LOSS  # noqa: E402
from app.services.degradation_model import DegradationModel  # noqa: E402
from app.services.fastf1_client import FastF1Client  # noqa: E402
from app.services.strategy_engine import StrategyEngine  # noqa: E402

print("Testing StrategyEngine with Monza 2023...")
print("Loading and analyzing data...\n")

# Load Monza 2023
client = FastF1Client()
session = client.load_session(2023, "Monza", "R")

if not session:
    print("FAILED: Could not load session")
    sys.exit(1)

# Get total laps
total_laps = int(session.laps["LapNumber"].max())
print(f"Total laps: {total_laps}")

# Get stint data
all_drivers = session.laps["Driver"].unique()
all_stints = {}
for driver in all_drivers:
    stints = client.get_stint_data(session, driver)
    if stints:
        all_stints[driver] = stints

# Fit degradation model
model = DegradationModel()
curves = model.analyze_race(all_stints)

print(f"Degradation curves: {[c['compound'] for c in curves]}\n")

# Simulate strategies
pit_loss = PIT_LOSS.get("Monza", PIT_LOSS["default"])
print(f"Pit loss: {pit_loss}s")
print("\nSimulating strategies (max 2 stops)...\n")

engine = StrategyEngine(model)
strategies = engine.simulate_strategies(curves, total_laps, pit_loss, max_stops=2)

if not strategies:
    print("FAILED: No strategies generated")
    sys.exit(1)

print(f"SUCCESS: Generated {len(strategies)} strategies")
print("\n" + "=" * 80)
print("TOP 5 STRATEGIES:")
print("=" * 80)

for i, strategy in enumerate(strategies[:5], 1):
    total_mins = strategy["predicted_time"] / 60
    delta_secs = strategy["time_delta"]

    print(f"\n{i}. {strategy['strategy_name']}")
    print(f"   Total time: {total_mins:.2f} min ({total_mins*60:.1f}s)")
    print(f"   Delta to fastest: +{delta_secs:.2f}s")
    print(f"   Stints:")

    for stint in strategy["stints"]:
        print(
            f"     Lap {stint['start_lap']}-{stint['end_lap']}: "
            f"{stint['compound']} ({stint['laps']} laps)"
        )

print("\n" + "=" * 80)
print("\nStrategy engine working correctly!")
print(f"Fastest strategy: {strategies[0]['strategy_name']}")
