"""
Constants Module
----------------

This module comprises constants designed to assist the
various classes and functions defined within the package.
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

# Loads the `weather_codes.json` file comprising weather
# codes mapped with their corresponding descriptions.
with open(BASE_DIR / "weather_codes.json") as file:
    WEATHER_CODES = json.load(file)

# Available frequencies for periodical weather data extraction.
FREQUENCIES = "hourly", "daily"

TEMPERATURE_UNITS = "celsius", "fahrenheit"
WIND_SPEED_UNITS = "kmh", "mph", "ms", "kn"
PRECIPITATION_UNITS = "mm", "inch"

CLOUD_COVER_LEVEL = Literal["low", "mid", "high"]
PRESSURE_LEVELS = Literal["sealevel", "surface"]

TEMPERATURE_ALTITUDES = Literal[2, 80, 120, 180]
WIND_ALTITUDES = Literal[10, 80, 120, 180]
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

AQI_SOURCES = Literal["european", "us"]

# Maps different AQI ranges with their corresponding descriptions.
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

# Available plants for pollen grains concentration data extraction.
PLANTS = Literal["alder", "birch", "grass", "mugwort", "olive", "ragweed"]

DAILY_WEATHER_REQUEST_TYPES = Literal["max", "min", "mean"]

WAVE_TYPES = Literal["composite", "wind", "swell"]

# Maps user specified arguments with request parameters
# for extracting meteorology data from API endpoints.
WAVE_TYPES_MAP = {"composite": "", "wind": "wind_", "swell": "swell_"}
PRESSURE_LEVEL_MAPPING = {"sealevel": "pressure_msl", "surface": "surface_pressure"}

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
# summary data extraction. The same are also used as the index labels
# for the marine weather summary pandas Series/DataFrame object.
MARINE_WEATHER_SUMMARY_DATA_TYPES = [
    "wave_height",
    "wave_direction",
    "wave_period",
]

DAILY_MARINE_WEATHER_SUMMARY_DATA_TYPES = [
    "wave_height_max",
    "wave_direction_dominant",
    "wave_period_max",
]

# List of air quality data types extracted in the current air quality
# summary data extraction. The same are also used as the index labels
# for the current air quality summary data pandas Series object.
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
