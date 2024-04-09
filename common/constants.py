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

# Available freuqencies of periodical weather data.
FREQUENCY = Literal["hourly", "daily"]

TEMPERATURE_UNITS = Literal["celcius", "fahrenheit"]
WIND_SPEED_UNITS = Literal["kmh", "mph", "ms", "kn"]
PRECIPITATION_UNITS = Literal["mm", "inch"]

CLOUD_COVER_LEVEL = Literal["low", "mid", "high"]
PRESSURE_LEVELS = {"sealevel": "pressure_msl", "surface": "surface_pressure"}

# Holds the altitude in meters(m) above the surface level.
TEMPERATURE_ALTITUDE = Literal[2, 80, 120, 180]
WIND_ALTITUDE = Literal[10, 80, 120, 180]

# Available altitude in meters(m) options for historial wind data.
ARCHIVE_WIND_ALTITUDES = Literal[10, 100]

# Air Quality Index sources.
AQI_SOURCES = Literal["european", "us"]

# Description of Air Quality Index falling in different ranges.
AQI_LEVELS = {
    range(50): "Good",
    range(51, 101): "Moderate",
    range(101, 151): "Slight Unhealthy",
    range(151, 201): "Unhealthy",
    range(201, 301): "Very Unhealthy",
    range(301, 501): "Harazdous",
}

GASES = Literal["ozone", "carbon_monoxide", "nitrogen_dioxide", "suphur_dioxide"]
PLANTS = Literal["alder", "birch", "grass", "mugwort", "olive", "ragweed"]
