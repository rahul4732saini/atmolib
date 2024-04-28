r"""
Meteorology Package
-------------------

This package facilitates the extraction of meteorology data including
weather, historical weather, marine, and air quality data. It provides
a comprehensive set of objects and functions for the same.

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
