"""
Atmolib Package
-----------------

Atmolib is a Python library that provides easy and fast access to meteorology data through
Open-Meteo APIs. It enables developers to extract weather, historical weather, air quality,
and marine weather data effortlessly, empowering them to integrate accurate meteorological
information seamlessly into their applications.

#### Features:
- Weather data extraction: Retrieve current and forecast weather data for any location.
- Historical weather data: Access past weather data for analysis and reporting.
- Air quality information: Obtain real-time air quality data to monitor environmental conditions.
- Marine weather data: Retrieve marine weather forecasts for maritime activities.

Author: rahul4732saini
License: MIT, see LICENSE for more details. (https://opensource.org/licenses/MIT)
"""

__all__ = (
    "Weather",
    "WeatherArchive",
    "MarineWeather",
    "AirQuality",
    "get_elevation",
    "get_city_details",
    "constants",
    "tools",
    "version",
)

from .meteorology import Weather, WeatherArchive, AirQuality, MarineWeather
from .common import tools, constants
from .common.tools import get_city_details, get_elevation
from .version import version

__version__ = version
