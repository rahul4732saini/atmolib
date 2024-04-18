r"""
This module comprises classes that serve as foundational components
for various functionalities within the package.
"""

from typing import Any

import requests
import pandas as pd

from common import tools


class BaseMeteor:
    r"""
    Base class for all meteorology classes.
    """

    _session: requests.Session
    _api: str

    __slots__ = "_lat", "_long", "_params"

    def __init__(self, lat: int | float, long: int | float) -> None:

        # params dictionary to be used to store request parameters for API requests.
        self._params: dict[str, Any] = {}

        self.lat = lat
        self.long = long

    @property
    def lat(self) -> int | float:
        return self._lat

    @lat.setter
    def lat(self, __value: int | float) -> None:
        assert -90 <= __value <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90, got {__value}."
        )
        self._lat = self._params["latitude"] = __value

    @property
    def long(self) -> int | float:
        return self._long

    @long.setter
    def long(self, __value: int | float) -> None:
        assert -90 <= __value <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90, got {__value}."
        )
        self._long = self._params["longitude"] = __value

    def _get_current_data(self, params: dict[str, Any]) -> int | float:
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

    def _get_periodical_data(self, params: dict[str, Any]) -> pd.DataFrame:
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


class BaseForecast(BaseMeteor):
    r"""
    Base class for all weather forecast classes.
    """

    # This attribute must be explicitly defined in
    # the child classes as per their customs.
    _max_forecast_days: int

    __slots__ = "_lat", "_long", "_params", "_forecast_days"

    def __init__(
        self, lat: int | float, long: int | float, forecast_days: int = 7
    ) -> None:
        rf"""
        Creates an instance of the {self.__class__.__name__} class.

        Params:
        -------
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - forecast_days (int): Number of days for which the forecast has to
        be extracted, must be in the range of 1 and {self._max_forecast_days}.
        """

        super().__init__(lat, long)

        self.forecast_days = forecast_days

    @property
    def forecast_days(self) -> int:
        return self._forecast_days

    @forecast_days.setter
    def forecast_days(self, __value: int) -> None:

        # Asserts if the forecast days value is within the range
        # of the maximum forecast days assigned by the child class
        # with the `_max_forecast_days` class attribute.
        assert __value in range(1, self._max_forecast_days + 1), ValueError(
            f"`forecast_days` must be in the range of 1 and {self._max_forecast_days}, got {__value!r}."
        )
        self._forecast_days = __value

        # Updating the `_params` dictionary with the 'forecast_days' key-value
        # pair to be used as a parameter in requesting the API.
        self._params["forecast_days"] = __value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(lat={self._lat}, long={self._long}, "
            f"forecast_days={self._forecast_days})"
        )
