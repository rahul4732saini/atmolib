r"""
This module defines the MarineWeather class facilitating the retrieval of marine weather data from
the Open-Meteo Marine Weather API based on latitudinal and longitudinal coordinates of the location.

The MarineWeather class allows users to extract various types of marine weather information, including 
current marine weather data and up to upcoming 8-days hourly and daily marine weather forecast data.
"""

from typing import Any

import requests
import pandas as pd

from common import constants
from errors import RequestError
from objects import BaseForecast


class MarineWeather(BaseForecast):
    r"""
    MarineWeather class to extract marine weather data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Marine Weather API to fetch the current or up to upcoming 8-days
    hourly and daily marine weather forecast data with a resolution of 5 kilometers(km).

    Params:
    - lat (int | float): Latitudinal coordinates of the location.
    - long (int | float): Longitudinal coordinates of the location.
    - wave_type (str): Type of ocean wave, must be one of the following:
        - 'composite' (Extracts data related to all wave types.)
        - 'wind' (Extracts data related to waves generated by winds.)
        - 'swell' (Extracts data related to waves travelling across long distances.)
    - forecast_days (int): Number of days for which the forecast has to
    be extracted, must be in the range of 1 and 16.
    """

    __slots__ = "_lat", "_long", "_wave_type", "_type", "_params", "_forecast_days"

    _session = requests.Session()
    _api = constants.MARINE_API

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        wave_type: constants.WAVE_TYPES,
        forecast_days: int = 7,
    ) -> None:
        super().__init__(lat, long, forecast_days)

        # Verifies the availability of marine weather data at the
        # supplied coorindates at object initilization.
        self._check_data_availability()

        self.wave_type = wave_type

    @property
    def wave_type(self) -> str:
        return self._wave_type

    @wave_type.setter
    def wave_type(self, __value: str) -> None:

        # Retrieves the corresponding wave type value used as a request parameter for
        # extracting marine weather data from the Open-Meteo Marine Weather API.
        wave_type: str | None = constants.WAVE_TYPES_MAP.get(__value)

        if wave_type is None:
            raise ValueError(
                f"Expected `wave_type` to be 'composite', 'wind' or 'swell', got {__value!r}."
            )

        # self._wave_type is assigned the wave type
        # value same as provided for user reference.
        self._wave_type = __value

        # self._type is used by the internally by the methods
        # for requesting marine weather data from the API.
        self._type = wave_type

    def __repr__(self) -> str:
        return (
            f"MarineWeather(lat={self._lat}, long={self._long}, "
            f"wave_type={self._wave_type!r}, forecast_days={self._forecast_days})"
        )

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

        if __name in ("_lat", "_long"):

            # Only executes the verification method if coordinate attributes
            # (`_lat`, `_long`) are altered post initialization by verifying
            # it with the `_params` dictionary.
            if (
                self._params["latitude"] is not None
                and self._params["longitude"] is not None
            ):
                self._check_data_availability()

    def _check_data_availability(self) -> None:
        r"""
        Verifies the availability of marine weather data for the supplied coordinates.
        """

        with self._session.get(constants.MARINE_API, params=self._params) as response:
            data: dict[str, Any] = response.json()

            if response.status_code != 200:
                raise RequestError(response.status_code, data["reason"])

    def get_current_wave_height(self) -> int | float:
        r"""
        Returns the wave height in meters(m) of the
        specified wave type at the supplied coorinates.
        """
        return self.get_current_weather_data({"current": f"{self._type}wave_height"})

    def get_current_wave_direction(self) -> int | float:
        r"""
        Returns the wave direction in degress of the specified
        wave type at the supplied coorinates.
        """
        return self.get_current_weather_data({"current": f"{self._type}wave_direction"})

    def get_current_wave_period(self) -> int | float:
        r"""
        Returns the wave period (It refers to the time taken by two consecutive
        wave crests (or troughs) to pass a fixed point) in seconds of the
        specified wave type at the supplied coorinates.
        """
        return self.get_current_weather_data({"current": f"{self._type}wave_period"})

    def get_daily_max_wave_height(self) -> pd.DataFrame:
        r"""
        Returns the daily maximum wave height in meters of the
        specified wave type at the specified coorindates.
        """
        return self.get_periodical_data({"daily": f"{self._type}wave_height_max"})
