"""
Weather Archive Module
----------------------

This module defines the WeatherArchive class facilitating extraction
of historical weather data from Open-Meteo's Weather History API.
"""

import atexit
from typing import Any
from datetime import date, datetime

import requests
import pandas as pd

from ..common import constants, tools
from ..base import BaseWeather


class WeatherArchive(BaseWeather):
    """
    WeatherArchive class defines mechanism for extraction of historical weather data
    based on the latitudinal and longitudinal coordinates of the location. It interacts
    with Open-Meteo's Weather History API to featch weather data ranging from 1940 till
    the present.
    """

    __slots__ = (
        "_lat",
        "_long",
        "_params",
        "_start_date",
        "_end_date",
    )

    _session = requests.Session()
    _api = constants.WEATHER_ARCHIVE_API

    # Closes the request session upon exit.
    atexit.register(_session.close)

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        start_date: str | date | datetime,
        end_date: str | date | datetime,
    ) -> None:
        """
        Creates an instance of the WeatherArchive class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - start_date (str | date | datetime): Initial date for the weather data.
        - end_date (str | date | datetime): Final date for the weather data.

        Date parameters must be date/datetime objects or strings
        formatted in the ISO-8601 date format (YYYY-MM-DD).
        """

        super().__init__(lat, long)

        self.set_start_date(start_date)
        self.set_end_date(end_date)

    @property
    def start_date(self) -> date:
        return self._start_date

    @property
    def end_date(self) -> date:
        return self._end_date

    def __repr__(self) -> str:
        return (
            f"Archive(lat={self._lat}, long={self._long},"
            f"start_date={self._start_date}, end_date={self._end_date})"
        )

    @staticmethod
    def _resolve_date(target: str | date | datetime) -> date:
        """Resolves the specified date into a `datetime.date` object."""

        if not isinstance(target, date | datetime):
            try:
                target = datetime.strptime(target, r"%Y-%m-%d").date()

            except ValueError:
                raise ValueError(f"{target!r} is not a valid date format.")

        elif isinstance(target, datetime):
            target = target.date()

        if target > date.today():
            raise ValueError(f"'{target:%Y-%m-%d}' is a date in the future.")

        return target

    def set_start_date(self, /, __value: str | date | datetime) -> None:
        """Sets the start date for historical weather extraction."""

        start_date: date = self._resolve_date(__value)

        if hasattr(self, "_end_date") and self._end_date < start_date:
            raise ValueError("'start_date' must be lower or equal to 'end_date'")

        self._start_date: date = start_date

        # Updates the parameters mapping with the start date for
        # requesting weather history from the Weather History API.
        self._params["start_date"] = start_date.strftime(r"%Y-%m-%d")

    def set_end_date(self, /, __value: str | date | datetime) -> None:
        """Sets the end date for historical weather extraction."""

        end_date: date = self._resolve_date(__value)

        if hasattr(self, "_start_date") and end_date < self._start_date:
            raise ValueError("'end_date' must be greater or equal to 'start_date'")

        self._end_date: date = end_date

        # Updates the parameters mapping with the end date for
        # requesting weather history from the Weather History API.
        self._params["end_date"] = end_date.strftime(r"%Y-%m-%d")

    @staticmethod
    def _get_soil_depth(depth: int) -> str:
        """
        Extracts the string representation of the depth range associated
        with the specified soil depth for requesting the Weather History API.

        #### Params:
        - depth (int): Desired depth for data extraction;
        must be an integer between 0 and 256.
        """

        if depth not in range(256):
            raise ValueError("'depth' must be an integer between 0 and 256.")

        for key, value in constants.ARCHIVE_SOIL_DEPTH.items():
            if depth in key:

                # The range is represented in a string
                # format as supported for API requests.
                return value

    def get_hourly_summary(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS = "celsius",
        precipitation_unit: constants.PRECIPITATION_UNITS = "mm",
        wind_speed_unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.DataFrame:
        """
        Returns a pandas DataFrame of hourly historical weather summary data at the
        specified coordinates in the specified units within the specified date range.

        #### The weather summary data includes the following data types:
        - temperature (2m above the ground level)
        - relative humidity (2m above the ground level)
        - dew point (2m above the ground level)
        - precipitation (sum of rain/showers/snowfall)
        - surface pressure in HPa (Hecto-pascal)
        - wind speed (10m above the ground level)
        - surface soil temperature
        - weather code
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # A string representation of the weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = ",".join(constants.HOURLY_ARCHIVE_SUMMARY_DATA_TYPES)

        params: dict[str, Any] = {
            "hourly": data_types,
            "temperature_unit": temperature_unit,
            "precipitation_unit": precipitation_unit,
            "wind_speed_unit": wind_speed_unit,
        }

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | params,
            constants.HOURLY_ARCHIVE_SUMMARY_COLUMN_LABELS,
        )

    def get_daily_summary(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS = "celsius",
        precipitation_unit: constants.PRECIPITATION_UNITS = "mm",
        wind_speed_unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.DataFrame:
        """
        Returns a pandas DataFrame of daily historical weather summary data at the
        specified coordinates in the specified units within the specified date range.

        #### The weather summary data includes the following data types:
        - Mean temperature (2m above the ground level)
        - precipitation (sum of rain/showers/snowfall)
        - Daylight duration in seconds
        - surface pressure in HPa (Hecto-pascal)
        - Mean wind speed (10m above the ground level)
        - weather code
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # A string representation of the weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = ",".join(constants.DAILY_ARCHIVE_SUMMARY_DATA_TYPES)

        params: dict[str, Any] = {
            "daily": data_types,
            "temperature_unit": temperature_unit,
            "precipitation_unit": precipitation_unit,
            "wind_speed_unit": wind_speed_unit,
        }

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | params,
            constants.DAILY_ARCHIVE_SUMMARY_COLUMN_LABELS,
        )

    def get_hourly_wind_speed(
        self,
        altitude: constants.ARCHIVE_WIND_ALTITUDES = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly wind speed data at the specified
        altitude and coordinates within the supplied date range.

        #### Params:
        - altitude (int): Altitude from the ground level in meters(m); must be 10 or 100.
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if altitude not in (10, 100):
            raise ValueError(f"Expected `altitude` to be 10 or 100; got {altitude}.")

        self._verify_wind_speed_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_hourly_wind_direction(
        self,
        altitude: constants.ARCHIVE_WIND_ALTITUDES = 10,
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly wind direction data at the
        specified altitude and coordinates within the supplied date range.

        #### Params:
        - altitude (int): Altitude from the ground level in meters(m); must be 10 or 100.
        """

        if altitude not in (10, 100):
            raise ValueError(f"Expected `altitude` to be 10 or 100; got {altitude}.")

        return self._get_periodical_data({"hourly": f"wind_direction_{altitude}m"})

    def get_hourly_soil_temperature(
        self, depth: int = 0, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly soil temperature data at the specified
        depth and coordinates in the specified unit within the supplied date range.

        #### Params:
        - depth (int): Desired depth of the temperature data within the ground level in
        centimeters(m). Temperature is extracted as a part of a range of depth. Available
        depth ranges are 0-7cm, 7-28cm, 28-100cm, 100-255cm. The supplied depth must fall
        in the range of 0 and 255.
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
        """
        self._verify_temperature_unit(unit)

        # Extracts the string representation of the depth range.
        depth_range: str = self._get_soil_depth(depth)

        return self._get_periodical_data(
            {"hourly": f"soil_temperature_{depth_range}cm", "temperature_unit": unit},
        )

    def get_hourly_soil_moisture(self, depth: int = 0) -> pd.Series:
        """
        Returns a pandas Series of hourly soil moisture data at the specified
        depth and coordinates in the specified unit within the supplied date range.

        #### Params:
        - depth (int): Desired depth of the moisture data within the ground level in
        centimeters(m). Moisture is extracted as a part of a range of depth. Available
        depth ranges are 0-7cm, 7-28cm, 28-100cm, 100-255cm. The supplied depth must fall
        in the range of 0 and 255.
        """

        # Extracts the string representation of the depth range.
        depth_range: str = self._get_soil_depth(depth)

        return self._get_periodical_data({"hourly": f"soil_moisture_{depth_range}cm"})
