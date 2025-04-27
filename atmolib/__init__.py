"""
Atmolib Package
---------------

Atmolib is a Python library that provides easy and fast access to meteorology data through
Open-Meteo APIs. It enables developers to extract weather, historical weather, air quality,
and marine weather data effortlessly, empowering them to integrate accurate meteorological
information seamlessly into their python code.

A short overview of all meteorology data extraction classes
has been defined below for quick user reference:

### Weather Class
The Weather class defines mechanism for extracting current and
forecast weather data for any location based on the coordinates.

#### Basic Usage:

>>> import atmolib as atmo
>>> weather = atmo.Weather(53.957, -1.082)
>>> weather.get_current_temperature()
13.9
>>> weather.get_current_wind_speed()
10.7

### WeatherArchive Class:
The WeatherArchive class defines mechansim for extracting
past weather data since 1940 for analysis and reporting.

#### Basic Usage:

>>> import atmolib as atmo
>>> archive = atmo.WeatherArchive(25.077, 55.309, '2022-02-02', '2022-02-04')
>>> archive.get_daily_temperature()
Date
Date1   Val1
Date2   Val2
Date3   Val3
dtype: float32

### MarineWeather Class
The MarineWeather class defines mechanism for extracting current and forecast
marine weather data for marinetime activities with a resolution of 5 kilometers(km).

#### Basic Usage:

>>> import atmolib as atmo
>>> marine = atmo.MarineWeather()
>>> marine.get_current_wave_direction()
174
>>> marine.get_daily_max_wave_height()
Date
Date1   Val1
Date2   Val2
        ...
Date6   Val6
Date7   Val7
Length: 7, dtype: float32

### AirQuality Class
The AirQuality class defines mechanism for extracting real-time
air quality data for monitoring environmental conditions.

>>> import atmolib as atmo
>>> air = atmo.AirQuality(28.91, 75.67)
>>> air.get_current_pm10_conc()
118.7
>>> air.get_hourly_uv_index()
Datetime
Time1   Val1
Time2   Val2
        ...
Time71  Val71
Time72  Val72
Length: 72, dtype: float32

The methods available for meteorological data extraction extend well beyong
those mentioned above. For a comprehensive overview, please refer to the package
documentation at https://www.github.com/rahul4732saini/atmolib.

Author: Rahul Saini (https://www.github.com/rahul4732saini)
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
