r"""
Tools Module for the pyweather Package

This module contains utility functions and tools used throughout
the pyweather package.
"""

import requests

from . import constants
from errors import RequestError


def get_elevation(lat: int | float, long: int | float) -> float:
    r"""
    Retrieves elevation data from Open-meteo elevation
    API based on the latitude and longitude coordinates.

    Raises:
        RequestError: If there's a server related error while requesting elevation data from the API.

    Example:
        >>> altitude = get_elevation(26.91, 32.89)
        >>> print(altitude)
        300.0  # Example elevation value in meters
    """

    url: str = f"{constants.ELEVATION_API}?latitude={lat}&longitude={long}"

    with requests.get(url) as response:
        if response.status_code != 200:
            message = response.json()["reason"]

            raise RequestError(response.status_code, message)

        (elevation,) = response.json()["elevation"]

    return elevation
