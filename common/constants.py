r"""
Constants Module for the pyweather package

This module comprises all the constants to be used throughout
the pyweather package. These constants are designed to assist
the other functionalities present within the package.
"""

import json
from pathlib import Path

# API endpoint URLs
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
WEATHER_HISTORY_API = "https://archive-api.open-meteo.com/v1/archive"
MARINE_API = "https://marine-api.open-meteo.com/v1/marine"
AIR_QUALITY_API = "https://air-quality-api.open-meteo.com/v1/air-quality"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
ELEVATION_API = "https://api.open-meteo.com/v1/elevation"

WEATHER_CODES_FILE = Path("weather_codes.json")
WEATHER_CODES = json.load(WEATHER_CODES_FILE.open())
