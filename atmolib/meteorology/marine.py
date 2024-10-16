"""
Marine Module
-------------

This module defines the MarineWeather class facilitating extraction
of marine weather data from Open-Meteo's Marine Weather API.
"""

import atexit

import requests
import pandas as pd

from ..base import BaseForecast
from ..common import constants, tools


class MarineWeather(BaseForecast):
    """
    MarineWeather class defines mechanism for extraction of marine weather
    data based on the latitudinal and longitudinal coordinates of the location.
    It interactrs with Open-Meteo's Marine Weather API to fetech the current or
    upto upcoming 8-days hourly and daily marine weather forecast data with a
    resolution of 5 kilometers(km).
    """

    __slots__ = "_lat", "_long", "_wave_type", "_type", "_params", "_forecast_days"

    _session = requests.Session()
    _api = constants.MARINE_API

    # Maximum number of days for which forecast data can be extracted.
    _max_forecast_days = 8

    # Closes the request session upon exit.
    atexit.register(_session.close)

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        wave_type: str = "composite",
        forecast_days: int = 7,
    ) -> None:
        """
        Creates an instance of the MarineWeather class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - wave_type (str): Ocean wave type; must be one of the following:
            - `composite` (All wave types)
            - `wind` (Waves generated by winds)
            - `swell` (Waves travelling across long distances)

            Defaults to `composite`.
        - forecast_days (int): Number of days for which the forecast has to
        be extracted; must be in the range of 1 and 8. Defaults to 7.
        """
        super().__init__(lat, long, forecast_days)
        self.wave_type = wave_type

    @property
    def wave_type(self) -> str:
        return self._wave_type

    @wave_type.setter
    def wave_type(self, __value: str) -> None:

        # Extracts the request parameter for the
        # corresponding user specified wave type.
        wave_type: str | None = constants.WAVE_TYPES_MAP.get(__value)

        if wave_type is None:
            raise ValueError(f"Invalid wave type specified: {__value!r}")

        # Sets the same value as specified for user reference.
        self._wave_type = __value

        # Stores the wave type paramter for internal usage by
        # extraction methods for requesting the API endpoint.
        self._type = wave_type

    def __repr__(self) -> str:
        return (
            f"MarineWeather(lat={self._lat}, long={self._long}, "
            f"wave_type={self._wave_type!r}, forecast_days={self._forecast_days})"
        )

    def get_current_summary(self) -> pd.Series:
        """
        Extracts current marine weather summary data.

        #### The summary data distribution includes the following:
        - Wave height
        - Wave direction
        - Wave period
        """

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = self._type + f",{self._type}".join(
            constants.MARINE_WEATHER_SUMMARY_PARAMS
        )

        return tools.get_current_summary(
            self._session,
            self._api,
            self._params | {"current": data_types},
            constants.MARINE_WEATHER_SUMMARY_PARAMS,
        )

    def get_hourly_summary(self) -> pd.DataFrame:
        """
        Extracts hourly marine weather forecase summary data.

        #### The summary data distribution includes the following:
        - Wave height
        - Wave direction
        - Wave period
        """

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = self._type + f",{self._type}".join(
            constants.MARINE_WEATHER_SUMMARY_PARAMS
        )

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | {"hourly": data_types},
            constants.MARINE_WEATHER_SUMMARY_PARAMS,
        )

    def get_daily_summary(self) -> pd.DataFrame:
        """
        Extracts daily marine weather forecast summary data.

        #### The summary data distribution includes the following:
        - Max wave height
        - Dominant wave direction
        - Max wave period
        """

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = self._type + f",{self._type}".join(
            constants.DAILY_MARINE_WEATHER_SUMMARY_PARAMS
        )

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | {"daily": data_types},
            constants.MARINE_WEATHER_SUMMARY_PARAMS,
        )

    def get_current_wave_height(self) -> int | float | None:
        """Extracts current wave height in meters(m)."""
        return self._get_current_data({"current": f"{self._type}wave_height"})

    def get_current_wave_direction(self) -> int | float | None:
        """Extracts current wave direction in degrees."""
        return self._get_current_data({"current": f"{self._type}wave_direction"})

    def get_current_wave_period(self) -> int | float | None:
        """
        Extracts current wave period in seconds(s).

        #### Brief:

        Wave period refers to the time taken by two consecutive
        wave crests (or troughs) to pass through a fixed point.
        """
        return self._get_current_data({"current": f"{self._type}wave_period"})

    def get_hourly_wave_height(self) -> pd.Series:
        """Extracts hourly wave height forecast in meters(m)."""
        return self._get_periodical_data({"hourly": f"{self._type}wave_height"})

    def get_hourly_wave_direction(self) -> pd.Series:
        """Extracts hourly wave direction forecast in degrees."""
        return self._get_periodical_data({"hourly": f"{self._type}wave_direction"})

    def get_hourly_wave_period(self) -> pd.Series:
        """
        Extracts hourly wave period forecast in seconds(s).

        #### Brief:

        Wave period refers to the time taken by two consecutive
        wave crests (or troughs) to pass through a fixed point.
        """
        return self._get_periodical_data({"hourly": f"{self._type}wave_period"})

    def get_daily_max_wave_height(self) -> pd.Series:
        """Extracts daily maximum wave height forecast in meters(m)."""
        return self._get_periodical_data({"daily": f"{self._type}wave_height_max"})

    def get_daily_dominant_wave_direction(self) -> pd.Series:
        """Extracts daily dominant wave direction forecast in degrees."""
        return self._get_periodical_data(
            {"daily": f"{self._type}wave_direction_dominant"}
        )

    def get_daily_max_wave_period(self) -> pd.Series:
        """
        Extracts daily maximum wave period forecast in seconds(s).

        #### Brief:

        Wave period refers to the time taken by two consecutive
        wave crests (or troughs) to pass through a fixed point.
        """
        return self._get_periodical_data({"daily": f"{self._type}wave_period_max"})
