r"""
Tools Module for the pyweather Package

This module contains utility functions and tools used throughout
the pyweather package.
"""

from typing import Any

import requests

from . import constants
from errors import RequestError


def get_elevation(lat: int | float, long: int | float) -> float:
    r"""
    Retrieves elevation data from Open-meteo elevation
    API based on the latitude and longitude coordinates.

    Params:
        lat (int | float): latitudinal coordinates of the location.
        long (int | float): longitudinal coordinates of the location.

    Raises:
        ValueError: If `lat` or `long` are not integers or floating point numbers.
        RequestError: If there's a server related error while requesting elevation data from the API.

    Example:
        >>> altitude = get_elevation(26.91, 32.89)
        >>> print(altitude)
        300.0  # Example elevation value in meters
    """

    if not isinstance(lat, int | float) or not isinstance(long, int | float):
        raise ValueError("lat and long must be integers or floating point numbers.")

    params: dict[str, int] = {"latitude": lat, "longitude": long}

    with requests.get(constants.ELEVATION_API, params=params) as response:
        if response.status_code != 200:
            message = response.json()["reason"]

            raise RequestError(response.status_code, message)

        (elevation,) = response.json()["elevation"]

    return elevation


def get_city_details(name: str, count: int = 5) -> list[dict[str, Any]] | None:
    r"""
    Retrieves the city details from Open-meteo
    geocoding API based on the name of the city.

    Params:
        name (str): The name of the city to retrieve details for.
        count (int): The number of results to be shown.

    Returns:
        List[Dict[str, Any]] | None: Returns a list of dictionaries containing details of the city.
        Each dictionary represents a result, containing various information about the city. None is
        returned if no cities corresponding to the supplied name are found in the database.

    Raises:
        ValueError: If `count` is not a positive integer.
        RequestError: If there's a server related error while requesting elevation data from the API.
    """

    if not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be a positive integer.")

    params: dict[str, str | int] = {"name": name, "count": count}

    with requests.get(constants.GEOCODING_API, params=params) as response:
        if response.status_code != 200:
            message = response.json()["reason"]

            raise RequestError(response.status_code, message)

        result: dict[str, Any] = response.json()

    # Returns None if no matching results are found.
    if result.get("results") is None:
        return None

    details: list[dict[str, Any]] = result["results"]
    return details
