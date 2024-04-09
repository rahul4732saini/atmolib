r"""
This module comprises classes that serve as foundational components
for various functionalities within the package.
"""

import pandas as pd

from typing import Any
import requests

from common import tools


class BaseWeather:
    r"""
    BaseClass for all weather classes.
    """

    _session: requests.Session
    _api: str

    __slots__ = "_lat", "_long", "_params"

    def __init__(self, lat: int | float, long: int | float) -> None:

        # Verifying the supplied `lat` and `long` arguments.
        assert -90 <= lat <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90. Got {lat}"
        )
        assert -180 <= long <= 180, ValueError(
            f"`long` must be in the range of -180 and 180. Got {long}"
        )

        # Template of the params dictionary to be used for API requests.
        self._params = {"latitude": lat, "longitude": long}

    @property
    def lat(self) -> int | float:
        return self._params["latitude"]

    @property
    def long(self) -> int | float:
        return self._params["longitude"]

    def __repr__(self) -> str:
        return f"Weather(lat={self.lat}, long={self.long})"

    def get_current_weather_data(self, params: dict[str, Any]) -> int | float:
        r"""
        Uses the supplied parameters to request the supplied
        Open-Meteo API and returns the current weather data.

        This function is intended for internal use within the package and may not be called
        directly by its users. It is exposed publicly for use by other modules within the package.

        Params:
        - params (dict[str, Any]): A dictionary all the necessary parameters except the
        coordinate parameters to request the Open-Meteo Weather API.
        """

        params |= self._params

        # _session and _api class attributes must be defined by the child class.
        data: int | float = tools.get_current_data(self._session, self._api, params)

        return data

    def get_periodical_data(self, params: dict[str, Any]) -> pd.DataFrame:
        r"""
        Uses the supplied parameters to request the supplied
        Open-Meteo API and returns the periodical weather data.

        This function is intended for internal use within the package and may not be called
        directly by its users. It is exposed publicly for use by other modules within the package.

        Params:
        - params (dict[str, Any]): A dictionary all the necessary parameters except the
        coordinate parameters to request the Open-Meteo Weather API.
        """

        params |= self._params

        # _session and _api class attributes must be defined by the child class.
        data: pd.DataFrame = tools.get_periodical_data(self._session, self._api, params)

        return data
