r"""
Tools module
------------

This module comprises utility functions and tools supporting other
functionalities throughout the pyweather package.
"""

from typing import Any
from types import ModuleType

import requests
import pandas as pd

from . import constants
from ..errors import RequestError


def _request_json(
    api: str, params: dict[str, Any], session: requests.Session | None = None
) -> dict[str, Any]:
    r"""
    Sends a GET request to the supplied API, retrieves the JSON data, and returns it.

    #### Parameters:
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): Necessary parameters for the API request including the
    coordinates of the location, requested data type, etc.
    - session: (optional): A requests.Session object for making the API requests. If not provided,
    the default requests session is used.

    #### Returns:
    - dict[str, Any]: A dictionary containing the JSON response from the API.

    #### Raises:
    - RequestError: If there is an error while requesting the API.
    """

    # The session is used as the handler if supplied else the module
    # itself is used to execute the `get` method for data extraction.
    request_handler: requests.Session | ModuleType = session if session else requests

    with request_handler.get(api, params=params) as response:
        results: dict[str, Any] = response.json()

        # Raises a custom RequestError if the response status code is not 200 (OK).
        # The error message is extracted from the API response itself.
        if response.status_code != 200:
            message = results["reason"]

            raise RequestError(response.status_code, message)

    return results


def get_current_data(
    session: requests.Session, api: str, params: dict[str, Any]
) -> int | float:
    r"""
    Base function for current meteorology data extraction from supplied API.

    This function is intended for internal use within the package and may not be called
    directly by its users. It is exposed publicly for use by other modules within the package.

    #### Params:
    - session (requests.Session): A requests.Session object for making the API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, str | int]): Necessary parameters for the API request including the
    coordinates of the location, requested data type, etc.

    #### Returns:
    - int | float: Returns the requested current weather data in integer or float format.
    """

    if params.get("latitude") is None or params.get("longitude") is None:
        raise KeyError(
            "'latitude' and 'longitude' keys not found in the `params` dictionary "
            "to indicate the coordinates of the location."
        )

    if params.get("current") is None:
        raise KeyError(
            "`current` key not found in the `params` dictionary with the requested weather data type."
        )

    results: dict[str, Any] = _request_json(api, params, session)

    # The 'current' key in the `results` dictionary holds all the current weather data key-value pairs.
    data: dict[str, Any] = results["current"]

    # Extracts the requested current weather data. The name of the key for the
    # requested data is obtained from the 'current' key in the `params` dictionary.
    # The value associated with this key is returned as the result.
    return data[params["current"]]


def get_periodical_data(
    session: requests.Session, api: str, params: dict[str, Any]
) -> pd.DataFrame:
    r"""
    Base function for the periodical (daily/hourly) weather data extraction from supplied API.

    This function is intended for internal use within the package and may not be called
    directly by its users. It is exposed publicly for use by other modules within the package.

    #### Params:
    - session (requests.Session): A requests.Session object for making the API requests.
    - api (str): Absolute URL of the API endpoint.
    - frequency (str): Frequency of the weather forecast data; 'hourly' or 'daily'.
    - params (dict[str, Any]): Necessary parameters for the API request including the
    coordinates of the location, requested data type, etc.

    #### Returns:
    - pd.DataFrame: Returns a pandas DataFrame of periodical weather data comprising two
    columns namely 'time' and 'data' where 'time' column indicates the time of the
    weather data in ISO 8601 format (YYYY-MM-DDTHH:MM) or the date of the weather data as
    (YYYY-MM-DD) depending upon the frequency supplied and 'data' column contains the
    weather data.

    #### Raises:
    - ValueError: If `frequency` is assigned to a value other than 'hourly' or 'daily'.
    - KeyError: If 'hourly' key is not found in the `params` dictionary.
    """

    if params.get("latitude") is None or params.get("longitude") is None:
        raise KeyError(
            "'latitude' and 'longitude' keys not found in the `params` dictionary "
            "to indicate the coordinates of the location."
        )

    # Iterates through the `params` dictionary searching for the key named after
    # the frequency ('hourly' or 'daily') of the requested data and assigns the key
    # to the `frequency` variable to be used ahead. Raises a KeyError if none is found.
    for key in params:
        if key in ("hourly", "daily"):
            frequency: str = key
            break
    else:
        raise KeyError(
            "Expected 'daily' or 'hourly' parameter in the `params` dictionary, got none."
        )

    results: dict[str, Any] = _request_json(api, params, session)

    # The key corresponding to the supplied `frequency` in the `results` dictionary
    # holds all the periodical weather data key-value pairs.
    data: dict[str, Any] = results[frequency]

    # pandas DataFrame containing time and periodical weather data.
    # The object comprises two columns namely 'time' and 'data'.
    # 'data' column data is retrieved from the key-value pair named after the
    # requested data type (e.g. temperature_2m, weather_code, etc.) in the `data` dictionary.
    dataframe = pd.DataFrame(
        {
            "time": data["time"],
            "data": data[params[frequency]],
        }
    )

    return dataframe


def get_current_summary(
    session: requests.Session, api: str, params: dict[str, Any], labels: list[str]
) -> pd.Series:
    r"""
    Base function for current meteorology summary data extraction from supplied API.

    This function is intended for internal use within the package and may not be called
    directly by its users. It is exposed publicly for use by other modules within the package.

    #### Params:
    - session (requests.Session): A requests.Session object for making the API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, str | int]): Necessary parameters for the API request including the
    coordinates of the location, requested data type, etc.
    - labels (list[str]): A list of strings used as index labels for
    the summary data pandas Series object.

    #### Returns:
    - pd.Series: Returns a pandas Series of the current meteorology summary data, comprising
    the index labels being the string representations of the data types.
    """

    if params.get("latitude") is None or params.get("longitude") is None:
        raise KeyError(
            "'latitude' and 'longitude' keys not found in the `params` dictionary "
            "to indicate the coordinates of the location."
        )

    if params.get("current") is None:
        raise KeyError(
            "`current` key not found in the `params` dictionary "
            "with the requested weather data types."
        )

    results: dict[str, Any] = _request_json(api, params, session)

    # The 'current' key in the `results` dictionary holds
    # all the current summary data key-value pairs.
    data: dict[str, Any] = results["current"]

    # Removing unnecessary key-values pairs.
    del data["time"], data["interval"]

    return pd.Series(data.values(), index=labels)


def get_periodical_summary(
    session: requests.Session, api: str, params: dict[str, Any], labels: list[str]
) -> pd.DataFrame:
    r"""
    Base function for periodical meteorology summary data extraction from supplied API.

    This function is intended for internal use within the package and may not be called
    directly by its users. It is exposed publicly for use by other modules within the package.

    #### Params:
    - session (requests.Session): A requests.Session object for making the API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, str | int]): Necessary parameters for the API request including the
    coordinates of the location, requested data type, etc.
    - labels (list[str]): A list of strings used as index labels for
    the summary data pandas Series object.

    #### Returns:
    - pd.Series: Returns a pandas Series of the periodical meteorology summary data, comprising
    the index labels being the string representations of the data types.
    """

    if params.get("latitude") is None or params.get("longitude") is None:
        raise KeyError(
            "'latitude' and 'longitude' keys not found in the `params` dictionary "
            "to indicate the coordinates of the location."
        )

    # Iterates through the `params` dictionary searching for the key named after
    # the frequency ('hourly' or 'daily') of the requested data and assigns the key
    # to the `frequency` variable to be used ahead. Raises a KeyError if none is found.
    for key in params:
        if key in ("hourly", "daily"):
            frequency: str = key
            break
    else:
        raise KeyError(
            "Expected 'daily' or 'hourly' parameter in the `params` dictionary, got none."
        )

    results: dict[str, Any] = _request_json(api, params, session)

    # The key corresponding to the supplied `frequency` in the `results`
    # dictionary holds all the current summary data key-value pairs.
    data: dict[str, Any] = results[frequency]

    # Removed the 'time' key-value pair containing the timeline of the summary
    # data to be used as index labels in the summary pandas DataFrame.
    timeline: list[str] = data.pop("time")

    # Creates a dataframe of the request summary data and modifies the
    # column labels with the supplied column labels in the `labels` list.
    dataframe: pd.DataFrame = pd.DataFrame(data, index=timeline)
    dataframe.columns = labels

    return dataframe


def get_elevation(lat: int | float, long: int | float) -> float:
    r"""
    Retrieves elevation data from Open-meteo elevation
    API based on the latitude and longitude coordinates.

    #### Params:
        - lat (int | float): latitudinal coordinates of the location.
        - long (int | float): longitudinal coordinates of the location.

    #### Raises:
        - ValueError: If `lat` or `long` are not integers or floating point numbers.

    #### Returns:
        - float: Returns the elevation at the supplied coordinates in meters(m).

    #### Example:
        >>> altitude = get_elevation(26.91, 32.89)
        >>> print(altitude)
        300.0  # Example elevation value in meters
    """

    if not isinstance(lat, int | float) or not isinstance(long, int | float):
        raise ValueError("`lat` and `long` must be integers or floating point numbers.")

    params: dict[str, int | float] = {"latitude": lat, "longitude": long}
    results: dict[str, Any] = _request_json(constants.ELEVATION_API, params)

    # Extracts the elevation data from the 'elevation' key-value pair in the `results` dictionary.
    (elevation,) = results["elevation"]

    return elevation


def get_city_details(name: str, count: int = 5) -> list[dict[str, Any]] | None:
    r"""
    Retrieves the city details from Open-meteo
    geocoding API based on the name of the city.

    #### Params:
        - name (str): The name of the city to retrieve details for.
        - count (int): The number of results to be shown.

    #### Returns:
        - List[Dict[str, Any]] | None: Returns a list of dictionaries containing details of the city.
        Each dictionary represents a result, containing various information about the city. None is
        returned if no cities corresponding to the supplied name are found in the database.

    #### Raises:
        - ValueError: If `count` is not a positive integer.
    """

    if not isinstance(count, int) or count <= 0:
        raise ValueError("`count` must be a positive integer.")

    params: dict[str, str | int] = {"name": name, "count": count}
    results: dict[str, Any] = _request_json(constants.GEOCODING_API, params)

    # Extracts city details from the 'results' key-value pair in the `results` dictionary.
    # The key-value pair is only present if cities with matching names are found in the
    # Open-Meteo database. None is assigned and returned if matching cities are not found.
    details: list[dict[str, Any]] | None = results.get("results")

    return details
