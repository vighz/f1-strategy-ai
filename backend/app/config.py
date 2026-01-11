"""
Configuration and environment variables for F1 Strategy Room backend.
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"

# Ensure directories exist
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# FastF1 Configuration
FASTF1_CACHE_DIR = str(CACHE_DIR)

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002"
).split(",")

# F1 Constants
PIT_LOSS = {
    "Monza": 22.5,
    "Monaco": 24.0,
    "Spa": 21.0,
    "Bahrain": 22.0,
    "Silverstone": 21.5,
    "default": 22.0,
}

FUEL_EFFECT_PER_LAP = 0.055  # seconds per lap

# Compound colors (exact F1 colors)
COMPOUND_COLORS = {
    "SOFT": "#FF0000",
    "MEDIUM": "#FFFF00",
    "HARD": "#FFFFFF",
    "INTERMEDIATE": "#00FF00",
    "WET": "#00BFFF",
}
