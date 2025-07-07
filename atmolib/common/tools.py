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
    - session (requests.Session | None): A `requests.Session` object for making
    API requests. If not specified, the `requests` module is used as the fallback.
    - timeout (int | float | None): Maximum duration to wait for a response
    from the API endpoint. Must be a number greater than 0 or `None`.

    #### Returns:
    - dict[str, Any]: A dictionary comprising the API response data.
    """

    handler: requests.Session | ModuleType = session if session else requests

    with handler.get(api, params=params, timeout=timeout) as response:
        results: dict[str, Any] = response.json()

        # Extracts the reason from the API response and raises a request
        # error if the status code does not indicate a success.
        if response.status_code // 100 != 2:
            message = results["reason"]

            raise RequestError(response.status_code, message)

    return results


def _verify_keys(params: dict[str, Any], keys: tuple[str, ...]) -> None:
    """
    Looks up for the specified keys in the specified parameters
    dictionary and raises a `KeyError` if any are found missing.

    #### Params:
    - params (dict[str, Any]): API request parameters.
    - keys (tuple[str]): Keys to look up for in the parameters dictionary.
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

    #### Returns:
    - int | float: An integer or floating-point number signifying the
    current meteorology data associated with the specified metric.
    """

    _verify_keys(params, ("latitude", "longitude", "current"))
    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts the current meteorology data from the 'results' dictionary.
    # The data value is mapped to the name of the specified metric within
    # the dictionary mapped to the 'current' key. The name of the metric is
    # mapped to the 'current' key within the request parameters dictionary.
    return results["current"][params["current"]]


def get_periodical_data(
    session: requests.Session,
    api: str,
    params: dict[str, Any],
    dtype=np.float32,
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> pd.Series:
    """
    Extracts periodical (hourly or daily) meteorology
    data from the specified API endpoint.

    #### Params:
    - session (requests.Session): A `requests.Session` object for making API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): API request parameters.
    - dtype: numpy datatype for meteorology data storage.
    Defaults to float32 (32-bit floating point number).
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.

    #### Returns:
    - pd.Series: Returns a pandas Series object comprising the periodical
    meteorology data. The index comprises the date or datetime depending
    upon the frequency in ISO-8601 format (YYYY-MM-DDTHH:MM) or (YYYY-MM-DD).
    """

    _verify_keys(params, ("latitude", "longitude"))

    # Sets the frequency to 'daily' if the 'hourly' key is not found
    # in the parameters dictionary. This is later verified under the
    # following conditional statement.
    frequency: str = "hourly" if "hourly" in params else "daily"

    if frequency not in params:
        raise KeyError("frequency parameter not found in the request parameters.")

    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts the meteorology data mapped to the name
    # of the frequency within the 'results' dictionary.
    data: dict[str, Any] = results[frequency]

    # Extracts the meteorology data mapped to the name of the requested
    # metric from the 'data' dictionary and initializes a pandas Series
    # object for storing the data along with their associated timestamps.
    # The metric name is mapped to the name of the frequency within the
    # request parameters dictionary.
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
    data from the specified API endpoint.

    #### Params:
    - session (requests.Session): A `requests.Session` object for making API requests.
    - api (str): Absolute URL of the API endpoint.
    - params (dict[str, Any]): API request parameters.
    - labels (list[str]): List of strings representing the index labels for
    the resultant pandas Series object.
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.

    #### Returns:
    - pd.Series: A pandas Series object comprising the current
    meteorology summary data, indexed by the specified data labels.
    """

    _verify_keys(params, ("latitude", "longitude", "current"))
    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts the current meteorology data mapped to the
    # 'current' key within from the 'results' dictionary.
    data: dict[str, Any] = results["current"]

    # Removes redundant key-values pairs from the dictionary as the same
    # object is used for initializing the resultant pandas Series object.
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
    - labels (list[str]): List of strings representing the column labels
    for the resultant pandas DataFrame object.
    - timeout (int | float | None): Maximum duration to wait for a response from
    the API endpoint. Must be a number greater than 0 or `None`.

    #### Returns:
    - pd.DataFrame: A pandas DataFrame object comprising the periodical
    meteorology summary data, with each individual column representing the
    data associated with a specific metric.
    """

    _verify_keys(params, ("latitude", "longitude"))

    # Sets the frequency to 'daily' if the 'hourly' key is not found
    # in the parameters dictionary. This is later verified under the
    # following conditional statement.
    frequency: str = "hourly" if "hourly" in params else "daily"

    if frequency not in params:
        raise KeyError("frequency parameter not found in the request parameters.")

    results: dict[str, Any] = _request_json(api, params, session, timeout)

    # Extracts the summary data mapped to the name of
    # the frequency within the 'results' dictioanary.
    data: dict[str, Any] = results[frequency]

    # Pops the data timeline array mapped to the 'time' key within the
    # 'data' dictionary to use the datetime labels as the index of the
    # resultant pandas DataFrame object.
    timeline: list[str] = data.pop("time")

    return pd.DataFrame(data, index=timeline, columns=labels)


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

    # Extracts the elevation data from the 'results' dictionary.
    (elevation,) = results["elevation"]

    return elevation


def get_city_details(
    name: str,
    count: int = 5,
    timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
) -> list[dict[str, Any]] | None:
    """
    Extracts the details of the city from Open-meteo's
    geocoding API based on the specified city name.

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

    # Extracts the city details from the 'results' key in the 'results'
    # dictionary. 'None' is returned if no cities with the specified name
    # are found in the API's database.
    return results.get("results")
