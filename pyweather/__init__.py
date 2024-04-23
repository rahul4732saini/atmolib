r"""
Pyweather Package
-----------------

PyWeather is a Python library that provides easy and fast access to meteorology data through
the Open-Meteo APIs. It enables developers to extract weather, historical weather, air quality,
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
    "tools",
    "Weather",
    "get_elevation",
    "WeatherArchive",
    "get_city_details",
    "MarineWeather",
    "AirQuality",
    "constants",
    "errors",
    "objects",
)

from .version import version
from . import errors, objects
from .common import tools, constants
from .common.tools import get_city_details, get_elevation
from .meteorology import Weather, WeatherArchive, AirQuality, MarineWeather

__version__ = version
