r"""
Meteorology Package
-------------------

This package facilitates the extraction of meteorological data, encompassing
weather, historical weather, marine conditions, and air quality data. If offers
a robust suite of classes and function designed for the same.

### Classes Exported:

- `Weather`: Extracts current or upto upcoming 16-days hourly and daily
weather forecast data.
- `MarineWeather`: Extracts current or upto upcoming 8-days hourly and
daily marine weather forecast data.
- `AirQuality`: Extracts current or upto upcoming 7-days hourly air
quality forecast data.
- `WeatherArchive`: Extracts historical weather data ranging from the
year 1940 till present.
"""

__all__ = "Weather", "WeatherArchive", "MarineWeather", "AirQuality"

from .weather import Weather
from .archive import WeatherArchive
from .air import AirQuality
from .marine import MarineWeather
