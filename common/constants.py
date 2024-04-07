r"""
Constants Module for the pyweather package

This module comprises all the constants used throughout the
pyweather package. These constants are designed to assist
other functionalities present within the package.
"""

import json
from pathlib import Path
from typing import Literal

# API endpoint URLs
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
WEATHER_HISTORY_API = "https://archive-api.open-meteo.com/v1/archive"
MARINE_API = "https://marine-api.open-meteo.com/v1/marine"
AIR_QUALITY_API = "https://air-quality-api.open-meteo.com/v1/air-quality"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
ELEVATION_API = "https://api.open-meteo.com/v1/elevation"

WEATHER_CODES_FILE = Path("weather_codes.json")
WEATHER_CODES = json.load(WEATHER_CODES_FILE.open())

TEMPERATURE_UNITS = Literal["celcius", "fahrenheit"]
CLOUD_COVER_LEVEL = Literal["low", "mid", "high"]
PRESSURE_LEVELS = {"sealevel": "pressure_msl", "surface": "surface_pressure"}

# Holds the altitude in meters(m) above the surface level.
ALTITUDE = Literal[2, 80, 120, 180]
