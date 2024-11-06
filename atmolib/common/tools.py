"""
Tools module
------------

This module comprises utility functions designed to support
other classes and functions defined within the package.
"""

from typing import Any
from types import ModuleType

import requests
import numpy as np
import pandas as pd

from . import constants
from ..errors import RequestError


def verify_timeout(timeout: int | float | None) -> None:
    """Verifies the specified timeout value."""

    if timeout is not None and timeout <= 0:
        raise ValueError("'timeout' must be greater than 0 or None.")


def _request_json(
    api: str,
    params: dict[str, Any],
    session: requests.Session | None = None,
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> dict[str, Any]:
    """
    Sends a GET request to the specified API endpoint,
    and returns the retrieved the JSON response.

    #### Params:
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): API request parameters.
    - session (requests.Session | None): A `requests.Session` object for making API
    requests. If not specified, the `requests` module as the fallback.
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.
    """

    # Verifies the specified timeout value.
    verify_timeout(timeout)

    request_handler: requests.Session | ModuleType = session if session else requests

    with request_handler.get(api, params=params, timeout=timeout) as response:
        results: dict[str, Any] = response.json()

        # Raises a request error if the response
        # status code does not indicate a success.
        if response.status_code // 100 != 2:
            message = results["reason"]

            raise RequestError(response.status_code, message)

    return results


def _verify_keys(params: dict[str, Any], keys: tuple[str, ...]) -> None:
    """
    Looks up for the specified keys in the parameters
    mapping and raises a `KeyError` if any are missing.

    #### Params:
    - params (dict[str, Any]): API request parameters.
    - keys (tuple[str]): Keys to look up for in the parameters mapping.
    """

    for key in keys:
        if key in params:
            continue

        raise KeyError(
            f"Required parameter {key!r} not found in the request parameters."
        )


def get_current_data(
    session: requests.Session,
    api: str,
    params: dict[str, Any],
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> int | float:
    """
    Extracts current meteorology data from the specified API endpoint.

    #### Params:
    - session (requests.Session): A `requests.Session` object for making API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): API request parameters.
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.
    """

    _verify_keys(params, ("latitude", "longitude", "current"))
    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts the request current meteorology data metrics from
    # the 'results' mapping. It is mapped with the name of the requested
    # metric within the dictionary mapped with the 'current' key.
    return results["current"][params["current"]]


def get_periodical_data(
    session: requests.Session,
    api: str,
    params: dict[str, Any],
    dtype=np.float32,
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> pd.Series:
    """
    Extracts periodical (hourly/daily) meteorology
    data from the specified API endpoint.

    #### Params:
    - session (requests.Session): A `requests.Session` object for making API requests.
    - api (str): Absolute URL of the API endpoint.
    - frequency (str): Frequency of the meteorology data (hourly/daily).
    - params (dict[str, Any]): API request parameters.
    - dtype: numpy datatype for meteorology data storage.
    Defaults to float32 (32-bit floating point number).
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.

    #### Returns:
    - pd.Series: Returns a pandas Series comprising the datetime and periodical meteorology
    data. The index comprises the datetime/date of the corresponding data depending upon the
    frequency in ISO-8601 format (YYYY-MM-DDTHH:MM) or (YYYY-MM-DD).
    """

    _verify_keys(params, ("latitude", "longitude"))
    frequency: str

    # Looks up for the frequency of the requested periodical data
    # in the parameters mapping and raises an error if not found.
    if "hourly" in params:
        frequency = "hourly"

    elif "daily" in params:
        frequency = "daily"

    else:
        raise KeyError("frequency parameter not found in the reuqest parameters.")

    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts meteorology data mapped with the key corresponding to the
    # name of the specified 'frequency' within the 'results' mapping.
    data: dict[str, Any] = results[frequency]

    # Extracts meteorology data mapped with the name of the requested metric
    # from the 'data' mapping and initializes the pandas Series object.
    series = pd.Series(data[params[frequency]], index=data["time"], dtype=dtype)
    series.index.name = "Date" if frequency == "daily" else "Datetime"

    return series


def get_current_summary(
    session: requests.Session,
    api: str,
    params: dict[str, Any],
    labels: list[str],
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> pd.Series:
    """
    Extracts current meteorology summary
    data from the supplied API endpoint.

    #### Params:
    - session (requests.Session): A `requests.Session` object for making API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): API request parameters.
    - labels (list[str]): List of strings representing the index labels for
    the resultant pandas Series object.
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.
    """

    _verify_keys(params, ("latitude", "longitude", "current"))
    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts current meteorology data from the 'current' key in the 'results' mapping.
    data: dict[str, Any] = results["current"]

    # Removing redundant key-values pairs from summary data.
    del data["time"], data["interval"]

    return pd.Series(data.values(), index=labels)


def get_periodical_summary(
    session: requests.Session,
    api: str,
    params: dict[str, Any],
    labels: list[str],
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> pd.DataFrame:
    """
    Extracts periodical meteorology summary
    data from the specified API endpoint.

    #### Params:
    - session (requests.Session): A `requests.Session` object for making API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): API request parameters.
    - labels (list[str]): List of strings representing the index labels
    for the resultant pandas Series object.
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.
    """

    _verify_keys(params, ("latitude", "longitude"))
    frequency: str

    # Looks up for the frequency of the requested periodical data
    # in the parameters mapping and raises an error if not found.
    if "hourly" in params:
        frequency = "hourly"

    elif "daily" in params:
        frequency = "daily"

    else:
        raise KeyError("frequency parameter not found in the request parameters.")

    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts summary data mapped with the key corresponding to the
    # name of the specified 'frequency' within the 'results' mapping.
    data: dict[str, Any] = results[frequency]

    # Pops the data timeline array mapped with 'time' key within the 'data'
    # mapping to be used as index labels in the resultant pandas DataFrame.
    timeline: list[str] = data.pop("time")

    # Initializes a pandas DataFrame for the summary data and alters the
    # column labels with the specified labels within the `labels` array.
    dataframe: pd.DataFrame = pd.DataFrame(data, index=timeline)
    dataframe.columns = pd.Index(labels)

    return dataframe


def get_elevation(
    lat: int | float,
    long: int | float,
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> float:
    """
    Extracts elevation in meters(m) from the sea-level at the specified
    latitude and longitude from the Open-meteo's elevation API.

    #### Params:
        - lat (int | float): latitudinal coordinates of the location.
        - long (int | float): longitudinal coordinates of the location.
        - timeout (int | float | None): Maximum duration to wait for a response from
        the API endpoint. Must be a number greater than 0 or `None`.

    #### Example:
        >>> altitude = get_elevation(26.91, 32.89)
        >>> print(altitude)
        300.0  # Example elevation value in meters
    """

    if not -90 <= lat <= 90:
        raise ValueError("'lat' must be a number between -90 and 90.")

    if not -180 <= long <= 180:
        raise ValueError("'long' must be a number between -180 and 180.")

    params: dict[str, int | float] = {"latitude": lat, "longitude": long}
    results: dict[str, Any] = _request_json(
        constants.ELEVATION_API, params, timeout=timeout
    )

    # Extracts and returns the elevation data from the API response mapping.
    (elevation,) = results["elevation"]

    return elevation


def get_city_details(
    name: str,
    count: int = 5,
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> list[dict[str, Any]] | None:
    """
    Retrieves the city details from Open-meteo geocoding API based on the city name.

    #### Params:
        - name (str): The name of the city to retrieve details for.
        - count (int): Maximum number of matching city records to be extracted;
        must be an integer between 1 and 20.
        - timeout (int | float | None): Maximum duration to wait for a response from
        the API endpoint. Must be a number greater than 0 or `None`.
    """

    if not isinstance(count, int) or count not in range(1, 21):
        raise ValueError("'count' must be an integer between 1 and 20.")

    params: dict[str, str | int] = {"name": name, "count": count}
    results: dict[str, Any] = _request_json(
        constants.GEOCODING_API, params, timeout=timeout
    )

    # Extracts the city details from the 'results' key in the API response
    # mapping. `None` is returned if no cities with the specified name are
    # found in the Open-Meteo database.
    return results.get("results")
