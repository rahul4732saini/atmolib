r"""
This module defines the Archive class facilitating the retrieval of historical weather data from
the Open-Meteo Weather History API based on latitudinal and longitudinal coordinates of the location.

The Archive class allows users to extract vaious types of historical weather data information
ranging from 1940 till the present.
"""

from datetime import date, datetime

import requests

from common import constants
from objects import BaseWeather


class Archive(BaseWeather):
    r"""
    Archive class to extract historical weather data based on latitude and longitude coordinates of
    the location within the specified date range. It interacts with the Open-Meteo Weather History
    API to fetch the weather data ranging from 1940 till the present.
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
