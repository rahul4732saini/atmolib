"""
Weather Archive Module
----------------------

This module defines the WeatherArchive class facilitating extraction
of historical weather data from Open-Meteo's Weather History API.
"""

from typing import Any
from datetime import date, datetime

import pandas as pd

from ..common import constants, tools
from ..base import BaseWeather


class WeatherArchive(BaseWeather):
    """
    WeatherArchive class defines methods for the extraction of historical
    weather data ranging from 1940 till the present, based on the latitudinal
    and longitudinal coordinates of the location.
    """

    __slots__ = (
        "_lat",
        "_long",
        "_params",
        "_start_date",
        "_end_date",
        "_timefmt",
        "_timeout",
    )

    _api = constants.WEATHER_ARCHIVE_API

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        start_date: str | date | datetime,
        end_date: str | date | datetime,
        timefmt: str = constants.DEFAULT_TIME_FORMAT,
        timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
    ) -> None:
        """
        Creates an instance of the WeatherArchive class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - start_date (str | date | datetime): Initial date for the weather data.
        - end_date (str | date | datetime): Final date for the weather data.
        - timefmt (str): Format of the date & time labels in periodic data
        tables; must be one of the following:
            - `iso8601` (ISO 8601 date & time format)
            - `unixtime` (Unix timestamp)

            Defaults to `iso8601`.
        - timeout (int | float | None): Maximum duration to wait for a response
        from the API endpoint. Must be a number greater than 0 or `None`.

        Date parameters must be date/datetime objects or strings
        formatted in the ISO-8601 date format (YYYY-MM-DD).
        """

        super().__init__(lat, long, timefmt, timeout)

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
            f"start_date={self._start_date}, end_date={self._end_date}, "
            f"timefmt={self._timefmt!r})"
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
            raise ValueError("'start_date' must be lower or equal to 'end_date'.")

        self._start_date: date = start_date
        self._params["start_date"] = start_date.strftime(r"%Y-%m-%d")

    def set_end_date(self, /, __value: str | date | datetime) -> None:
        """Sets the end date for historical weather extraction."""

        end_date: date = self._resolve_date(__value)

        if hasattr(self, "_start_date") and end_date < self._start_date:
            raise ValueError("'end_date' must be greater or equal to 'start_date'.")

        self._end_date: date = end_date
        self._params["end_date"] = end_date.strftime(r"%Y-%m-%d")

    @staticmethod
    def _get_soil_depth(depth: int) -> str:
        """
        Extracts a string representation of the depth range associated
        with the specified soil depth for requesting the API.

        #### Params:
        - depth (int): Desired depth for data extraction;
        must be an integer between 0 and 255.
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
        temperature_unit: str = "celsius",
        precipitation_unit: str = "mm",
        wind_speed_unit: str = "kmh",
    ) -> pd.DataFrame:
        """
        Extracts historical hourly weather summary in the specified
        temperature, precipitation and wind speed units.

        #### Params:
        - temperature_unit (str): Temperature unit; must be `celsius`
        or `fahrenheit`. Defaults to `celsius`.
        - precipitation_unit (str): Precipitation unit; must be `mm`
        or `inch`. Defaults to `mm`.
        - wind_speed_unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `kn` (knots)
            - `ms` (meter per second)

            Defaults to `kmh`.

        #### The weather summary data includes the following data types:
        - temperature (2m above ground level)
        - relative humidity (2m above ground level)
        - dew point (2m above ground level)
        - precipitation (sum of rain/showers/snowfall)
        - surface pressure in Hectopascal(HPa)
        - wind speed (10m above ground level)
        - surface soil temperature
        - weather code
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = ",".join(constants.HOURLY_ARCHIVE_SUMMARY_PARAMS)

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
            constants.HOURLY_ARCHIVE_SUMMARY_LABELS,
            self._timeout,
        )

    def get_daily_summary(
        self,
        temperature_unit: str = "celsius",
        precipitation_unit: str = "mm",
        wind_speed_unit: str = "kmh",
    ) -> pd.DataFrame:
        """
        Extracts daily historical weather summary in the specified
        temperature, precipitation and wind speed unit.

        #### Params:
        - temperature_unit (str): Temperature unit; must be `celsius`
        or `fahrenheit`. Defaults to `celsius`.
        - precipitation_unit (str): Precipitation unit; must be `mm`
        or `inch`. Defaults to `mm`.
        - wind_speed_unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `kn` (knots)
            - `ms` (meter per second)

            Defaults to `kmh`.

        #### The weather summary data includes the following data types:
        - Mean temperature (2m above ground level)
        - precipitation (sum of rain/showers/snowfall)
        - Daylight duration in seconds
        - surface pressure in Hectopascal(HPa)
        - Mean wind speed (10m above ground level)
        - weather code
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = ",".join(constants.DAILY_ARCHIVE_SUMMARY_PARAMS)

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
            constants.DAILY_ARCHIVE_SUMMARY_LABELS,
            self._timeout,
        )

    def get_hourly_wind_speed(self, altitude: int = 10, unit: str = "kmh") -> pd.Series:
        """
        Extracts historical hourly wind speed data at the
        specified altitude and in the specified wind speed unit.

        #### Params:
        - altitude (int): Altitude above the ground level in meters(m);
        must be 10 or 100. Defaults to 10.
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `ms` (meter per second)
            - `kn` (knots)

            Defaults to `kmh`
        """

        if altitude not in constants.ARCHIVE_WIND_ALTITUDES:
            raise ValueError(f"Invalid altitude level specified: {altitude}")

        self._verify_wind_speed_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_hourly_wind_direction(self, altitude: int = 10) -> pd.Series:
        """
        Extracts historical hourly wind direction
        data in degrees at the specified altitude.

        #### Params:
        - altitude (int): Altitude from the ground level in meters(m);
        must be 10 or 100. Defaults to 10.
        """

        if altitude not in constants.ARCHIVE_WIND_ALTITUDES:
            raise ValueError(f"Invalid altitude level specified: {altitude}")

        return self._get_periodical_data({"hourly": f"wind_direction_{altitude}m"})

    def get_hourly_soil_temperature(
        self, depth: int = 0, unit: str = "celsius"
    ) -> pd.Series:
        """
        Extracts historical hourly soil temperature data at the
        specified depth and in the specified temperature unit.

        #### Params:
        - depth (int): Desired depth of the temperature data beneath the ground level in
        centimeters(m). Temperature is extracted as a part of a range of depth. Available
        depth ranges are 0-7cm, 7-28cm, 28-100cm, 100-255cm. The specified depth must fall
        in the range of 0 and 255. Defaults to 0.
        - unit (str): Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """
        self._verify_temperature_unit(unit)

        # Extracts the string representation of the depth range.
        depth_range: str = self._get_soil_depth(depth)

        return self._get_periodical_data(
            {"hourly": f"soil_temperature_{depth_range}cm", "temperature_unit": unit},
        )

    def get_hourly_soil_moisture(self, depth: int = 0) -> pd.Series:
        """
        Extracts historical hourly soil moisture at the specified depth.

        #### Params:
        - depth (int): Desired depth of the moisture data beneath the ground level in
        centimeters(m). Moisture is extracted as a part of a range of depth. Available
        depth ranges are 0-7cm, 7-28cm, 28-100cm, 100-255cm. The specified depth must fall
        in the range of 0 and 255. Defaults to 0.
        """

        # Extracts the string representation of the depth range.
        depth_range: str = self._get_soil_depth(depth)

        return self._get_periodical_data({"hourly": f"soil_moisture_{depth_range}cm"})
