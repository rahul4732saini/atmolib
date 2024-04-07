r"""
This module defines the Weather class facilitating the retrieval of weather data from
the Open-Meteo Weather API based on latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather information, including 
current weather data, upcoming 7-days hourly weather forecast data, and upcoming 7-days 
daily weather forecast data.
"""

from typing import Any

import requests

from common import constants, tools


class Weather:
    r"""
    Weather class to extract weather data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Weather API to fetch the current or upcoming 7-days
    forecast weather data.

    Initialization(__init__) Params:
    - lat (int | float): latitudinal coordinates of the location.
    - long (int | float): longitudinal coordinates of the location.

    This class allows the user to extract the following:
    - Current weather data such as temperature, atmospheric pressure, weather code, etc.
    - Upcoming 7-days hourly weather forecast data including the current day.
    - Upcoming 7-days daily weather forecast data including the current day.
    """

    __slots__ = "_lat", "_long", "_params"

    _api = constants.WEATHER_API
    _session = requests.Session()

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

    def get_current_temperature(self, altitude: constants.ALTITUDE = 2) -> float:
        r"""
        Returns the current temperature at the supplied altitude from the ground level.

        Params:
        - altitude (int): Altitude from the ground level. Must be in (2, 80, 120, 180).
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(f"`altitude` must be in (2, 80, 120, 180). Got {altitude}")

        params: dict[str, Any] = self._params | {"current": f"temperature_{altitude}m"}
        temperature: float = tools.get_current_data(self._session, self._api, params)

        return temperature

    def get_current_weather_code(self) -> tuple[int, str]:
        r"""
        Returns a tuple comprising the weather code followed
        by a string description of the weather code.
        """

        params: dict[str, Any] = self._params | {"current": "weather_code"}

        weather_code: int = tools.get_current_data(self._session, self._api, params)
        description: str = constants.WEATHER_CODES[str(weather_code)]

        return weather_code, description

    def get_current_total_cloud_cover(self) -> int | float:
        r"""
        Returns the total cloud cover in percentage(%) at the supplied coordinates.
        """

        params: dict[str, Any] = self._params | {"current": "cloud_cover"}
        cloud_cover: int | float = tools.get_current_data(
            self._session, self._api, params
        )

        return cloud_cover
