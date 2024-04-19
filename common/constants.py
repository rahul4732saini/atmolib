r"""
Constants Module
----------------

This module comprises all the constants used throughout the pyweather package.
These constants are designed to assist other functionalities present within the package.
"""

import json
from pathlib import Path
from typing import Literal

# API endpoint URLs.
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
WEATHER_ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"
MARINE_API = "https://marine-api.open-meteo.com/v1/marine"
AIR_QUALITY_API = "https://air-quality-api.open-meteo.com/v1/air-quality"
GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
ELEVATION_API = "https://api.open-meteo.com/v1/elevation"

# Weather codes JSON file comprising weather codes mapped with the corresponding
# description of the same. `WEATHER_CODES` loads the JSON file into a dictionary.
WEATHER_CODES_FILE = Path("weather_codes.json")
WEATHER_CODES = json.load(WEATHER_CODES_FILE.open())

# Available frequencies of periodical weather data.
FREQUENCY = Literal["hourly", "daily"]

# Units used as request parameters in different weather data extraction requests.
TEMPERATURE_UNITS = Literal["celsius", "fahrenheit"]
WIND_SPEED_UNITS = Literal["kmh", "mph", "ms", "kn"]
PRECIPITATION_UNITS = Literal["mm", "inch"]

CLOUD_COVER_LEVEL = Literal["low", "mid", "high"]
PRESSURE_LEVELS = Literal["sealevel", "surface"]

# Dictionary of keys as accepted arguments by users mapped to values used
# as request parameter for extracting data from the Open-Meteo Weather API.
PRESSURE_LEVEL_MAPPING = {"sealevel": "pressure_msl", "surface": "surface_pressure"}

# Holds the altitude in meters(m) above the surface level for different request types.
TEMPERATURE_ALTITUDE = Literal[2, 80, 120, 180]
WIND_ALTITUDE = Literal[10, 80, 120, 180]
ARCHIVE_WIND_ALTITUDES = Literal[10, 100]

# Available depth-range options in centimeters(cm) for
# historical soil temperature/moisture data extraction.
ARCHIVE_SOIL_DEPTH = {
    range(7): "0_to_7",
    range(7, 28): "7_to_28",
    range(28, 100): "28_to_100",
    range(100, 256): "100_to_255",
}

# Available depth options in centimeters(cm) for soil temperature data extraction.
SOIL_TEMP_DEPTH = Literal[0, 6, 18, 54]

# Available depth-range options in centimeters(cm) for soil moisture data extraction.
SOIL_MOISTURE_DEPTH = {
    range(1): "0_to_1",
    range(1, 3): "1_to_3",
    range(3, 9): "3_to_9",
    range(9, 27): "9_to_27",
    range(27, 81): "27_to_81",
}

# Air Quality Index sources.
AQI_SOURCES = Literal["european", "us"]

# Description of Air Quality Index falling within different ranges.
AQI_LEVELS = {
    range(50): "Good",
    range(51, 101): "Moderate",
    range(101, 151): "Slight Unhealthy",
    range(151, 201): "Unhealthy",
    range(201, 301): "Very Unhealthy",
    range(301, 501): "Hazardous",
}

# Available atmospheric gases for gaseous concentration data extraction.
GASES = Literal["ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide"]

# Available plant options for pollen grains concentration data extraction.
PLANTS = Literal["alder", "birch", "grass", "mugwort", "olive", "ragweed"]

DAILY_WEATHER_REQUEST_TYPES = Literal["max", "min", "mean"]

# Available wave types for marine weather data extraction.
WAVE_TYPES = Literal["composite", "wind", "swell"]

# Dictionary of keys as accepted arguments by users mapped to values used
# as request parameter for extracting data from the Open-Meteo Marine API.
WAVE_TYPES_MAP = {"composite": "", "wind": "wind_", "swell": "swell_"}

# Available types of temperatures which can be extracted from the API.
TEMPERATURE_TYPES = Literal["temperature_2m", "apparent_temperature"]
