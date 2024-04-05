r"""
Tools Module for the pyweather Package

This module contains utility functions and tools used throughout
the pyweather package.
"""

from typing import Any

import requests
import pandas as pd

from . import constants
from errors import RequestError


def get_elevation(lat: int | float, long: int | float) -> float:
    r"""
    Retrieves elevation data from Open-meteo elevation
    API based on the latitude and longitude coordinates.

    Params:
        - lat (int | float): latitudinal coordinates of the location.
        - long (int | float): longitudinal coordinates of the location.

    Raises:
        - ValueError: If `lat` or `long` are not integers or floating point numbers.
        - RequestError: If there's an error while making the HTTP request to retrieve
        forecast data from the API.

    Returns:
        - float: Returns the elevation at the supplied coordinates in meters(m).

    Example:
        >>> altitude = get_elevation(26.91, 32.89)
        >>> print(altitude)
        300.0  # Example elevation value in meters
    """

    if not isinstance(lat, int | float) or not isinstance(long, int | float):
        raise ValueError("`lat` and `long` must be integers or floating point numbers.")

    params: dict[str, int] = {"latitude": lat, "longitude": long}

    with requests.get(constants.ELEVATION_API, params=params) as response:
        results: dict[str, Any] = response.json()

        if response.status_code != 200:
            message = results["reason"]

            raise RequestError(response.status_code, message)

    # Extracts the elevation data from the 'elevation' key-value pair in the results dictionary.
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
        - RequestError: If there's an error while making the HTTP request to retrieve
        forecast data from the API.
    """

    if not isinstance(count, int) or count <= 0:
        raise ValueError("`count` must be a positive integer.")

    params: dict[str, str | int] = {"name": name, "count": count}

    with requests.get(constants.GEOCODING_API, params=params) as response:
        results: dict[str, Any] = response.json()

        if response.status_code != 200:
            message: str = results.get("reason", "Unknown Error")

            raise RequestError(response.status_code, message)

    # Extracts city details from the 'results' key-value pair in the results dictionary.
    # The key-value pair is only present if cities with matching names are found in the
    # Open-Meteo database. None is assigned and returned if matching cities are not found.
    details: list[dict[str, Any]] | None = results.get("results")

    return details


def get_current_forecast(
    session: requests.Session, api: str, params: dict[str, str | int]
) -> int | float:
    r"""
    Base function for retrieving the current forecast data from supplied API.

    This function is intended for internal use within the package and may not be called
    directly by its users. It is exposed publicly for use by other modules within the package.

    Params:
        - session (requests.Session): A requests session object for making the API requests.
        - api (str): Absolute URL of the API.
        - params (dict[str, str | int]): Necessary parameters for the API request including the
        coordinates of the location, requested data type, etc.

    Returns:
        - int | float: Returns the requested current forecast data in string or integer format.

    Raises:
        - RequestError: If there's an error while making the HTTP request to retrieve
        forecast data from the API.
    """

    if not params.get("latitude") or not params.get("longitude"):
        raise KeyError(
            "`latitude` and `longitude` keys not found in the params dictionary "
            "indicating the coordinates of the location."
        )

    if not params.get("current"):
        raise KeyError(
            "`current` key not found in the params dictionary with the requested weather data type."
        )

    with session.get(api, params=params) as response:
        results: dict[str, Any] = response.json()

        # Raises a custom RequestError if the response status code is not 200 (OK).
        # The error message is extracted from the API response.
        if response.status_code != 200:
            message: str = results.get("reason", "Unknown Error")

            raise RequestError(response.status_code, message)

    # The "current" key in the results dictionary holds all the current weather data key-value pairs.
    data: dict[str, Any] = results["current"]

    # Extracts the specific current weather data requested by the user.
    # The name of the key for the requested data is obtained from
    # the 'current' key in the 'params' dictionary.
    # The value associated with this key is returned as the result.
    return data[params["current"]]


def get_hourly_forecast(
    session: requests.Session, api: str, params: dict[str, str | int]
) -> pd.DataFrame:
    r"""
    Base function for retrieving the hourly forecast data from supplied API.

    This function is intended for internal use within the package and may not be called
    directly by its users. It is exposed publicly for use by other modules within the package.

    Params:
        - session (requests.Session): A requests session object for making the API requests.
        - api (str): Absolute URL of the API.
        - params (dict[str, str | int]): Necessary parameters for the API request including the
        coordinates of the location, requested data type, etc.

    Returns:
        - pd.DataFrame: Returns a pandas DataFrame of hourly weather forecast data comprising of
        two columns namely 'time' and 'forecast' where 'time' column indicates the time of the
        forecast data in ISO 8601 format (YYYY-MM-DDTHH:MM) and 'forecast' columns contains the
        hourly weather forecast data.

    Raises:
        - KeyError: If 'hourly' key is not found in the `params` dictionary.
        - RequestError: If there's an error while making the HTTP request to retrieve
        forecast data from the API.
    """

    if not params.get("latitude") or not params.get("longitude"):
        raise KeyError(
            "`latitude` and `longitude` keys not found in the params dictionary "
            "indicating the coordinates of the location."
        )

    if not params.get("hourly"):
        raise KeyError(
            "`hourly` key not found in the params dictionary with the requested weather data type."
        )

    with session.get(api, params=params) as response:
        results: dict[str, Any] = response.json()

        if response.status_code != 200:
            message: str = results.get("reason", "Unknown Error")

            # Raises a custom RequestError if the response status code is not 200 (OK).
            # The error message is extracted from the API response.
            raise RequestError(response.status_code, message)

    # The "hourly" key in the results dictionary holds all the hourly
    # weather forecast data key-value pairs.
    hourly_data: dict[str, Any] = results["hourly"]

    # pandas DataFrame containing time and hourly weather forecast data.
    # The object comprises of two columns namely 'time' and 'forecast'.
    # 'forecast' column data is retrived from the key-value pair named after the
    # requested data type (eg. temperature_2m, weather_code, etc.) in the hourly_data mapping.
    dataframe = pd.DataFrame(
        {
            "time": hourly_data["time"],
            "forecast": hourly_data[params["hourly"]],
        }
    )

    return dataframe
