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

BASE_DIR = Path(__file__).resolve().parent.parent

# Weather codes JSON file comprising weather codes mapped with the corresponding
# description of the same. `WEATHER_CODES` loads the JSON file into a dictionary.
WEATHER_CODES_FILE = BASE_DIR / "weather_codes.json"
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
# as request parameter for extracting data from the API Endpoints.
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
    range(27, 82): "27_to_81",
}

# Air Quality Index sources.
AQI_SOURCES = Literal["european", "us"]

# Mapping of AQI descriptions falling within different ranges of AQI.
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

CURRENT_WEATHER_SUMMARY_DATA_TYPES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
]

CURRENT_WEATHER_SUMMARY_INDEX_LABELS = [
    "temperature",
    "relative_humidity",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "surface_pressure",
    "wind_speed",
    "wind_direction",
]

# List of marine weather data types extracted in the marine weather
# summary data extraction. The same are also used as the index
# labels for the marine weather summary pandas Series object.
MARINE_WEATHER_SUMMARY_DATA_TYPES = [
    "wave_height",
    "wave_direction",
    "wave_period",
]

# List of air quality data types extracted in the current
# air quality summary data extraction. The same are also used
# as the index labels for the air quality summary pandas Series object.
CURRENT_AIR_QUALITY_SUMMARY_DATA_TYPES = [
    "dust",
    "pm10",
    "ozone",
    "pm2_5",
    "us_aqi",
    "uv_index",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "european_aqi",
    "ammonia",
]

HOURLY_WEATHER_SUMMARY_DATA_TYPES = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "cloud_cover",
    "visibility",
    "wind_speed_10m",
    "soil_temperature_0cm",
]

HOURLY_WEATHER_SUMMARY_COLUMN_LABELS = [
    "temperature",
    "relative_humidity",
    "dew_point",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "cloud_cover",
    "visibility",
    "wind_speed",
    "soil_temperature",
]

DAILY_WEATHER_SUMMARY_DATA_TYPES = [
    "weather_code",
    "temperature_2m_mean",
    "daylight_duration",
    "uv_index_max",
    "precipitation_sum",
    "wind_speed_10m_mean",
    "wind_direction_10m_dominant",
]

DAILY_WEATHER_SUMMARY_COLUMN_LABELS = [
    "weather_code",
    "temperature",
    "daylight_duration",
    "uv_index",
    "precipitation",
    "wind_speed",
    "wind_direction",
]

HOURLY_AIR_QUALITY_SUMMARY_DATA_TYPES = [
    "pm10",
    "pm2_5",
    "carbon_monoxide",
    "nitrogen_dioxide",
    "sulphur_dioxide",
    "ozone",
    "dust",
    "uv_index",
    "ammonia",
]

HOURLY_ARCHIVE_SUMMARY_DATA_TYPES = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "wind_speed_10m",
    "soil_temperature_0_to_7cm",
]

HOURLY_ARCHIVE_SUMMARY_COLUMN_LABELS = [
    "temperature",
    "relative_humidity",
    "dew_point",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "wind_speed",
    "soil_temperature",
]

DAILY_ARCHIVE_SUMMARY_DATA_TYPES = [
    "weather_code",
    "temperature_2m_mean",
    "daylight_duration",
    "precipitation_sum",
    "wind_speed_10m_mean",
    "wind_direction_10m_dominant",
]

DAILY_ARCHIVE_SUMMARY_COLUMN_LABELS = [
    "weather_code",
    "temperature",
    "daylight_duration",
    "precipitation",
    "wind_speed",
    "wind_direction",
]
