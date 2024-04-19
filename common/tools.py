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

from errors import RequestError


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

    if params.get(frequency) is None:
        raise KeyError(
            f"'{frequency}' key not found in the `params` dictionary with the requested weather data type."
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
