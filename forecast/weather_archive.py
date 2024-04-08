r"""
This module defines the Archive class facilitating the retrieval of historical weather data from
the Open-Meteo Weather History API based on latitudinal and longitudinal coordinates of the location.

The Archive class allows users to extract vaious types of historical weather data information
ranging from 1940 till the present.
"""

from datetime import date, datetime

import requests
import pandas as pd

from common import constants
from objects import BaseWeather


class Archive(BaseWeather):
    r"""
    Archive class to extract historical weather data based on latitude and longitude coordinates of
    the location within the specified date range. It interacts with the Open-Meteo Weather History
    API to fetch the weather data ranging from 1940 till the present.

    Date parameters must be date or datetime objects or strings formatted
    in the ISO-8601 date format (YYYY-MM-DD).

    Params:
    - lat (int | float): Latitudinal coordinates of the location.
    - long (int | float): Longitudinal coordinates of the location.
    - start_date (str | date | datetime): Initial date for the weather data.
    - end_date(str | date | datetime): Final date for the weather data.
    """

    _session = requests.Session()
    _api = constants.WEATHER_HISTORY_API

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        start_date: str | date | datetime,
        end_date: str | date | datetime,
    ) -> None:
        super().__init__(lat, long)

        self.start_date = start_date
        self.end_date = end_date

        self._params |= {"start_date": start_date, "end_date": end_date}

    @staticmethod
    def _resolve_date(target: str | date | datetime, var: str) -> date:
        r"""
        [PRIVATE] Verifies the supplied date argument, resolves it into the
        string formatted date with the ISO-8601 format (YYYY-MM-DD).

        The `var` parameter has to be the name of the actual date parameter
        (`start_date` or `end_date`) for reference in custom error messages.
        """

        if isinstance(target, date | datetime):
            target = date.strftime(r"%Y-%m-%d")

        try:
            datetime.strptime(target, r"%Y-%m-%d")

        except (ValueError, TypeError):
            raise ValueError(f"Invalid value for `{var}` parameter.")

        return target

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, __value: str | date | datetime) -> None:
        self._start_date = self._resolve_date(__value, "start_date")

    @property
    def end_date(self) -> str:
        return self._end_date

    @end_date.setter
    def end_date(self, __value: str | date | datetime) -> None:
        self._end_date = self._resolve_date(__value, "end_date")

    def get_hourly_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of temperature data 2 meters(m) above the ground
        level at the specified coordinates within the supplied date range.

        Params:
        - unit: Temperature unit. Must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be one of 'celsius' or 'fahrenheit'. Got {unit!r}."
            )

        params: dict[str, str] = {
            "hourly": "temperature_2m",
            "temperature_unit": unit,
        }

        return self.get_periodical_weather_data("hourly", self._params | params)

    def get_hourly_relative_humidity(self) -> int | float:
        r"""
        Returns a pandas DataFrame of hourly relative humidity percentage(%)
        data at the specified coordinates within the date range.
        """
        return self.get_periodical_weather_data(
            "hourly", self._params | {"hourly": "relative_humidity_2m"}
        )

    def get_hourly_weather_code(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly weather code data with its corresponding
        description at the specified coordinates withing the date range.

        Columns:
        - time: time of the forecast data in ISO 8601 format (YYYY-MM-DDTHH-MM).
        - data: weather code at the corresponding hour.
        - description: description of the corresponding weather code.
        """

        data: pd.DataFrame = self.get_periodical_weather_data(
            "hourly", {"hourly": "weather_code"}
        )

        # Creating a new column 'description' mapped to the the
        # description of the corresponding weather code.
        data["description"] = data["data"].map(
            lambda x: constants.WEATHER_CODES[str(x)]
        )

        return data

    def get_hourly_total_cloud_cover(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly total cloud cover data percentage(%) at
        the specified coordinates within the supplied date range.
        """
        return self.get_periodical_weather_data("hourly", {"hourly": "cloud_cover"})
