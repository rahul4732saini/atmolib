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

        # Template of the params dictionary to be used for API requests.
        self._params = {"latitude": None, "longitude": None}

        self._lat = lat
        self._long = long

    @property
    def lat(self) -> int | float:
        return self._lat

    @lat.setter
    def lat(self, __value: int | float) -> None:
        assert -90 <= __value <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90. Got {__value}"
        )
        self._lat = self._params["latitude"] = __value

    @property
    def long(self) -> int | float:
        return self._long

    @long.setter
    def long(self, __value: int | float) -> None:
        assert -90 <= __value <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90. Got {__value}"
        )
        self._long = self._params["longitude"] = __value

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
