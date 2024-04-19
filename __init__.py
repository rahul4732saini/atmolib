r"""
Pyweather Package
-----------------

PyWeather is a Python library that provides easy and fast access to meteorology data through
the Open-Meteo APIs. It enables developers to extract weather, historical weather, air quality,
and marine weather data effortlessly, empowering them to integrate accurate meteorological
information seamlessly into their applications.

Features:
- Weather data extraction: Retrieve current and forecast weather data for any location.
- Historical weather data: Access past weather data for analysis and reporting.
- Air quality information: Obtain real-time air quality data to monitor environmental conditions.
- Marine weather data: Retrieve marine weather forecasts for maritime activities.

Author: rahul4732saini
Version: ---
License: MIT License, see LICENSE for more details. (https://opensource.org/licenses/MIT)
"""

__all__ = (
    "Weather",
    "WeatherArchive",
    "AirQuality",
    "MarineWeather",
    "get_elevation",
    "get_city_details",
)

from typing import Any

from common import tools, constants
from meteorology import Weather, WeatherArchive, AirQuality, MarineWeather


def get_elevation(lat: int | float, long: int | float) -> float:
    r"""
    Retrieves elevation data from Open-meteo elevation
    API based on the latitude and longitude coordinates.

    Params:
        - lat (int | float): latitudinal coordinates of the location.
        - long (int | float): longitudinal coordinates of the location.

    Raises:
        - ValueError: If `lat` or `long` are not integers or floating point numbers.

    Returns:
        - float: Returns the elevation at the supplied coordinates in meters(m).

    Example:
        >>> altitude = get_elevation(26.91, 32.89)
        >>> print(altitude)
        300.0  # Example elevation value in meters
    """

    if not isinstance(lat, int | float) or not isinstance(long, int | float):
        raise ValueError("`lat` and `long` must be integers or floating point numbers.")

    params: dict[str, int | float] = {"latitude": lat, "longitude": long}
    results: dict[str, Any] = tools._request_json(constants.ELEVATION_API, params)

    # Extracts the elevation data from the 'elevation' key-value pair in the `results` dictionary.
    (elevation,) = results["elevation"]

    return elevation


def get_city_details(name: str, count: int = 5) -> list[dict[str, Any]] | None:
    r"""
    Retrieves the city details from Open-meteo
    geocoding API based on the name of the city.

    Params:
        - name (str): The name of the city to retrieve details for.
        - count (int): The number of results to be shown.

    Returns:
        - List[Dict[str, Any]] | None: Returns a list of dictionaries containing details of the city.
        Each dictionary represents a result, containing various information about the city. None is
        returned if no cities corresponding to the supplied name are found in the database.

    Raises:
        - ValueError: If `count` is not a positive integer.
    """

    if not isinstance(count, int) or count <= 0:
        raise ValueError("`count` must be a positive integer.")

    params: dict[str, str | int] = {"name": name, "count": count}
    results: dict[str, Any] = tools._request_json(constants.GEOCODING_API, params)

    # Extracts city details from the 'results' key-value pair in the `results` dictionary.
    # The key-value pair is only present if cities with matching names are found in the
    # Open-Meteo database. None is assigned and returned if matching cities are not found.
    details: list[dict[str, Any]] | None = results.get("results")

    return details
