r"""
This module defines the Weather class facilitating the retrieval of weather data from
the Open-Meteo Weather API based on latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather information, including 
current weather data, up to upcoming 16-days hourly weather forecast data, and up to upcoming
16-days daily weather forecast data.
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
    - Up to upcoming 16-days hourly weather forecast data including the current day.
    - Up to upcoming 16-days daily weather forecast data including the current day.
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

    def _get_current_weather_data(self, params: dict[str, Any]) -> int | float:
        r"""
        [PRIVATE] Uses the supplied parameters to request the Open-Meteo
        Weather API and returns the result.

        Params:
        - params (dict[str, Any]): A dictionary all the necessary parameters except the
        coordinate parameters to request the Open-Meteo Weather API.
        """

        params |= self._params
        data: int | float = tools.get_current_data(self._session, self._api, params)

        return data

    def get_current_temperature(
        self,
        altitude: constants.TEMPERATURE_ALTITUDE = 2,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> float:
        r"""
        Returns the current temperature in the supplied temperature unit
        at the supplied altitude in meters(m) from the ground level.

        Params:
        - altitude (int): Altitude from the ground level. Must be in (2, 80, 120, 180).
        - unit (str): Temperature unit. Must be 'celsius' or 'fahrenheit'.
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be one of (2, 80, 120, 180). Got {altitude}"
            )

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be one of 'celsius' or 'fahrenheit'. Got {unit!r}."
            )

        return self._get_current_weather_data(
            {"current": f"temperature_{altitude}m", "temperature_unit": unit}
        )

    def get_current_weather_code(self) -> tuple[int, str]:
        r"""
        Returns a tuple comprising the current weather code followed
        by a string description of the weather code.
        """

        weather_code: int = self._get_current_weather_data({"current": "weather_code"})
        description: str = constants.WEATHER_CODES[str(weather_code)]

        return weather_code, description

    def get_current_total_cloud_cover(self) -> int | float:
        r"""
        Returns the current total cloud cover in percentage(%) at the supplied coordinates.
        """
        return self._get_current_weather_data({"current": "cloud_cover"})

    def get_current_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> int | float:
        r"""
        Returns the current cloud cover in percentage(%) at the supplied level and coordinates.

        Params:
        - level (str): Altitude level of the desired cloud coverage. Level supplied must be
        one of the following:
            - 'low' (clouds and fog up to an altitude of 3 km.)
            - 'mid' (clouds at an altitude between 3 km and 8 km.)
            - 'high' (clouds at an altitude higher than 8 km.)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(
                f"Expected `level` to be one of ('low', 'mid', 'high'). Got {level!r}."
            )

        return self._get_current_weather_data({"current": f"cloud_cover_{level}"})

    def get_current_apparent_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> int | float:
        r"""
        Returns the current apparent temperature at the supplied coordinates.

        Apparent temperature is the perceived feels-like temperature
        combining wind chill factor, relative humidity and solar radiation.

        Params:
        - unit (str): Temperature unit. Must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit'. Got {unit!r}."
            )

        return self._get_current_weather_data(
            {"current": "apparent_temperature", "temperature_unit": unit}
        )

    def get_current_wind_speed(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> int | float:
        r"""
        Returns the current wind speed at the supplied altitude and in the supplied unit.

        Params:
        - altitude (int): Altitude from the ground level. Must be in (10, 80, 120, 180).
        - unit (str): Wind speed unit. The unit must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitute` to be one of (10, 80, 120, 180). Got {altitude}"
            )

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be one of ('kmh', 'mph', 'ms', 'kn'). Got {unit!r}."
            )

        return self._get_current_weather_data(
            {"current": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_current_wind_direction(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
    ) -> int | float:
        r"""
        Returns the current wind direction at the supplied altitude and in the supplied unit.

        Params:
        - altitude (int): Altitude from the ground level. Must be in (10, 80, 120, 180).
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be one of (10, 80, 120, 180). Got {altitude}."
            )

        return self._get_current_weather_data(
            {"current": f"wind_direction_{altitude}m"}
        )

    def get_current_wind_gusts(
        self, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> int | float:
        r"""
        Returns the current wind gusts above 10 meters(m) from ground level in the supplied unit.

        Params:
        - unit (str): Wind speed unit. The unit must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be one of ('kmh', 'mph', 'ms', 'kn'). Got {unit!r}."
            )

        return self._get_current_weather_data(
            {"current": "wind_gusts_10", "wind_speed_unit": unit}
        )

    def get_current_relative_humidity(self) -> int | float:
        r"""
        Returns the current relative humidity 2 meters(m) above the
        ground level in percentage(%) at the supplied coordinates.
        """
        return self._get_current_weather_data({"current": "relative_humidity_2m"})

    def get_current_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> int | float:
        r"""
        Returns the current precipitation (sum of rain, showers, and snowfall) at
        the supplied coordinates.

        Params:
        - unit: Precipitation unit. It must be in ('mm', 'inch').
        """

        if unit not in ("mm", "inch"):
            raise ValueError(
                f"Expected `unit` to be one of 'mm' or 'inch'. Got {unit!r}."
            )

        return self._get_current_weather_data(
            {"current": "precipitation", "precipitation_unit": unit}
        )
