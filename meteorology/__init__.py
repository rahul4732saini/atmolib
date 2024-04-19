r"""
Weather Forecast Package
------------------------

This package facilitates the extraction of weather data including
atmospheric, marine, and air quality data. It provides a comprehensive
set of tools for weather data extraction.

Classes Exported:
- `Weather`: Extracts current or up to upcoming 16-days hourly and daily weather forecast data.
- `MarineWeather`: Extracts current or up to upcoming 8-days hourly and daily marine weather forecast data.
- `AirQuality`: Extracts current or up to upcoming 7-days hourly air quality forecast data.
- `WeatherArchive`: Extracts historical weather data ranging from the year 1940 till the present.
"""

__all__ = "Weather", "WeatherArchive", "MarineWeather", "AirQuality"

from .air import AirQuality
from .weather import Weather
from .marine import MarineWeather
from .archive import WeatherArchive
