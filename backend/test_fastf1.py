"""Quick test script to verify FastF1 works with Monza 2023."""
import sys

sys.path.insert(0, ".")

from app.services.fastf1_client import FastF1Client  # noqa: E402

print("Testing FastF1 with Monza 2023...")
print("This may take 30-60 seconds on first load...\n")

client = FastF1Client()
session = client.load_session(2023, "Monza", "R")

if session:
    print("SUCCESS: Session loaded successfully!")
    print(f"   Event: {session.event['EventName']}")
    print(f"   Date: {session.event['EventDate']}")
    print(f"   Total laps: {len(session.laps)}")

    laps_data = client.get_race_laps(session)
    print(f"\nSUCCESS: Quick laps extracted: {laps_data['total_laps']}")

    # Test stint data for Verstappen
    stint_data = client.get_stint_data(session, "VER")
    print("\nSUCCESS: Verstappen stint data:")
    for stint in stint_data:
        print(
            f"   Stint {stint['stint_number']}: {stint['compound']} ({len(stint['laps'])} laps)"
        )

    print("\nFastF1 is working correctly!")
else:
    print("FAILED: Failed to load session")
