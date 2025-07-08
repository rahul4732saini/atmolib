"""
Constants Module
----------------

This module comprises constants designed to assist the
various classes and functions defined within the package.
"""

import json
from pathlib import Path

# Default timeout for requesting data from API endpoints in seconds(s).
DEFAULT_REQUEST_TIMEOUT = 30

MAX_PAST_DAYS = 92
DEFAULT_PAST_DAYS = 0

DEFAULT_TIME_FORMAT = "iso8601"
TIME_FORMATS = "iso8601", "unixtime"

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
    WEATHER_CODES: dict[str, str] = json.load(file)

AQI_SOURCES = "european", "us"

# Maps different AQI ranges with their corresponding descriptions.
AQI_LEVELS = {
    range(50): "Good",
    range(51, 101): "Moderate",
    range(101, 151): "Slight Unhealthy",
    range(151, 201): "Unhealthy",
    range(201, 301): "Very Unhealthy",
    range(301, 501): "Hazardous",
}

# Available frequencies for periodical weather data extraction.
FREQUENCIES = "hourly", "daily"

TEMPERATURE_UNITS = "celsius", "fahrenheit"
WIND_SPEED_UNITS = "kmh", "mph", "ms", "kn"
PRECIPITATION_UNITS = "mm", "inch"

CLOUD_COVER_LEVELS = "low", "mid", "high"
PRESSURE_LEVELS = "sealevel", "surface"

TEMPERATURE_ALTITUDES = 2, 80, 120, 180
WIND_ALTITUDES = 10, 80, 120, 180
ARCHIVE_WIND_ALTITUDES = 10, 100

# Available atmospheric gases and plant species for
# corresponding aerial concentration data extraction.
GASES = "ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide"
PLANTS = "alder", "birch", "grass", "mugwort", "olive", "ragweed"

# Available soil depths in centimeters(cm) for temperature data extraction.
SOIL_TEMP_DEPTH = 0, 6, 18, 54

# Available soil depth ranges in centimeters(m) for
# historical soil temperature/moisture data extraction.
ARCHIVE_SOIL_DEPTH = {
    range(7): "0_to_7",
    range(7, 28): "7_to_28",
    range(28, 100): "28_to_100",
    range(100, 256): "100_to_255",
}

# Available soil depth ranges in centimeters(cm) for soil moisture data extraction.
SOIL_MOISTURE_DEPTH = {
    range(1): "0_to_1",
    range(1, 3): "1_to_3",
    range(3, 9): "3_to_9",
    range(9, 27): "9_to_27",
    range(27, 82): "27_to_81",
}

DAILY_WEATHER_STATISTICAL_METRICS = "max", "min", "mean"
WAVE_TYPES = "composite", "wind", "swell"

# Maps user specified arguments with their corresponding request
# parameters for extracting meteorology data from API endpoints.
WAVE_TYPES_MAP = {"composite": "", "wind": "wind_", "swell": "swell_"}
PRESSURE_LEVEL_MAPPING = {"sealevel": "pressure_msl", "surface": "surface_pressure"}

# The constants defined below comprise requests metric names and their
# corresponding labels for extracting summary of various meteorological
# factors in different time intervals.

CURRENT_WEATHER_SUMMARY_PARAMS = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "surface_pressure",
    "wind_speed_10m",
    "wind_direction_10m",
]

CURRENT_WEATHER_SUMMARY_LABELS = [
    "temperature",
    "relative_humidity",
    "precipitation",
    "weather_code",
    "cloud_cover",
    "surface_pressure",
    "wind_speed",
    "wind_direction",
]

HOURLY_WEATHER_SUMMARY_PARAMS = [
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

HOURLY_WEATHER_SUMMARY_LABELS = [
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

DAILY_WEATHER_SUMMARY_PARAMS = [
    "weather_code",
    "temperature_2m_mean",
    "daylight_duration",
    "uv_index_max",
    "precipitation_sum",
    "wind_speed_10m_mean",
    "wind_direction_10m_dominant",
]

DAILY_WEATHER_SUMMARY_LABELS = [
    "weather_code",
    "temperature",
    "daylight_duration",
    "uv_index",
    "precipitation",
    "wind_speed",
    "wind_direction",
]

MARINE_WEATHER_SUMMARY_PARAMS = [
    "wave_height",
    "wave_direction",
    "wave_period",
]

DAILY_MARINE_WEATHER_SUMMARY_PARAMS = [
    "wave_height_max",
    "wave_direction_dominant",
    "wave_period_max",
]

CURRENT_AIR_QUALITY_SUMMARY_PARAMS = [
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

HOURLY_AIR_QUALITY_SUMMARY_PARAMS = [
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

HOURLY_ARCHIVE_SUMMARY_PARAMS = [
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "wind_speed_10m",
    "soil_temperature_0_to_7cm",
]

HOURLY_ARCHIVE_SUMMARY_LABELS = [
    "temperature",
    "relative_humidity",
    "dew_point",
    "precipitation",
    "weather_code",
    "surface_pressure",
    "wind_speed",
    "soil_temperature",
]

DAILY_ARCHIVE_SUMMARY_PARAMS = [
    "weather_code",
    "temperature_2m_mean",
    "daylight_duration",
    "precipitation_sum",
    "wind_speed_10m_mean",
    "wind_direction_10m_dominant",
]

DAILY_ARCHIVE_SUMMARY_LABELS = [
    "weather_code",
    "temperature",
    "daylight_duration",
    "precipitation",
    "wind_speed",
    "wind_direction",
]
