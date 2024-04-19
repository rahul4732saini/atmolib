r"""
This module defines the Weather class facilitating the extraction of weather data from the
Open-Meteo Weather API based on the latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather data including current
weather data and up to upcoming 16-days hourly and daily weather forecast data.
"""

import atexit

import requests
import pandas as pd

from common import constants
from objects import BaseForecast, BaseWeather


class Weather(BaseForecast, BaseWeather):
    r"""
    Weather class to extract weather data based on the latitude and longitude coordinates.
    It interacts with the Open-Meteo Weather API to fetch the current or upcoming 16-days
    hourly and daily weather forecast data.
    """

    __slots__ = "_lat", "_long", "_params", "_forecast_days"

    _api = constants.WEATHER_API
    _session = requests.Session()

    # The maximum number of days in the future for forecast data extraction.
    _max_forecast_days = 16

    # Closes the request session upon exit.
    atexit.register(_session.close)

    @staticmethod
    def _verify_wind_altitude(altitude: int) -> None:
        r"""
        Verifies the specified altitude for wind data extraction. Raises a ValueError if
        the argument provided is not a valid altitude for requesting data from the API.
        """

        if altitude not in (10, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 10, 80, 120 or 180; got {altitude}."
            )

    def get_current_temperature(
        self,
        altitude: constants.TEMPERATURE_ALTITUDE = 2,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> float:
        r"""
        Returns the current temperature in the specified temperature unit
        at the specified altitude in meters(m) from the ground level.

        Params:
        - altitude (int): Altitude from the ground level; must be 2, 80, 120 or 180.
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 2, 80, 120 or 180; got {altitude}."
            )

        self._verify_temperature_unit(unit)

        return self._get_current_data(
            {"current": f"temperature_{altitude}m", "temperature_unit": unit}
        )

    def get_current_weather_code(self) -> tuple[int | float, str]:
        r"""
        Returns a tuple comprising the current weather code followed
        by a string description of the weather code.
        """

        weather_code: int | float = self._get_current_data({"current": "weather_code"})

        # Weather code description is looked up in the `WEATHER_CODES` dictionary.
        description: str = constants.WEATHER_CODES[str(weather_code)]

        return weather_code, description

    def get_current_total_cloud_cover(self) -> int | float:
        r"""
        Returns the current total cloud cover in percentage(%) at the specified coordinates.
        """
        return self._get_current_data({"current": "cloud_cover"})

    def get_current_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> int | float:
        r"""
        Returns the current cloud cover in percentage(%) at the specified level and coordinates.

        Params:
        - level (str): Altitude level of the desired cloud coverage; must be one of the following:
            - 'low' (clouds and fog up to an altitude of 3 km.)
            - 'mid' (clouds at an altitude between 3 km and 8 km.)
            - 'high' (clouds at an altitude higher than 8 km.)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(
                f"Expected `level` to be 'low', 'mid' or 'high'; got {level!r}."
            )

        return self._get_current_data({"current": f"cloud_cover_{level}"})

    def get_current_apparent_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> int | float:
        r"""
        Returns the current apparent temperature at the specified coordinates.

        Apparent temperature is the perceived feels-like temperature
        combining wind chill factor, relative humidity and solar radiation.

        Params:
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
        """
        self._verify_temperature_unit(unit)

        return self._get_current_data(
            {"current": "apparent_temperature", "temperature_unit": unit}
        )

    def get_current_wind_speed(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> int | float:
        r"""
        Returns the current wind speed at the specified
        altitude and in the specified wind speed unit.

        Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """
        self._verify_wind_altitude(altitude)
        self._verify_wind_speed_unit(unit)

        return self._get_current_data(
            {"current": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_current_wind_direction(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
    ) -> int | float:
        r"""
        Returns the current wind direction in degrees at the
        specified altitude and in the specified unit.

        Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        """

        if altitude not in (10, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 10, 80, 120 or 180; got {altitude}."
            )

        return self._get_current_data({"current": f"wind_direction_{altitude}m"})

    def get_current_wind_gusts(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> int | float:
        r"""
        Returns the current wind gusts above 10 meters(m) from ground level in the specified unit.

        Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """
        self._verify_wind_altitude(altitude)
        self._verify_wind_speed_unit(unit)

        return self._get_current_data(
            {"current": "wind_gusts_10", "wind_speed_unit": unit}
        )

    def get_current_relative_humidity(self) -> int | float:
        r"""
        Returns the current relative humidity 2 meters(m) above the
        ground level in percentage(%) at the specified coordinates.
        """
        return self._get_current_data({"current": "relative_humidity_2m"})

    def get_current_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> int | float:
        r"""
        Returns the current precipitation (sum of rain, showers, and snowfall)
        at the specified coordinates.

        Params:
        - unit: Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)

        return self._get_current_data(
            {"current": "precipitation", "precipitation_unit": unit}
        )

    def get_current_pressure(self, level: constants.PRESSURE_LEVELS) -> int | float:
        r"""
        Returns the current atmospheric pressure in
        Hectopascal (hPa) at the specified coordinates.

        Params:
        - level (str): Desired level of the atmospheric
        pressure data; must be 'surface' or 'sealevel'.
        """

        # Mapped value of the specified pressure level.
        pressure: str | None = constants.PRESSURE_LEVEL_MAPPING.get(level)

        if not pressure:
            raise ValueError(
                f"Expected `level` to be 'sealevel' or 'surface'; got {level!r}."
            )

        return self._get_current_data({"current": pressure})

    def get_current_rainfall(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> int | float:
        r"""
        Returns the current rainfall in mm/inch at the specified coordinates.

        Params:
        - unit: Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)
        return self._get_current_data({"current": "rain", "precipitation_unit": unit})

    def get_current_snowfall(self) -> int | float:
        r"""
        Returns the current snowfall in centimeters(cm) at the specified coordinates.
        """
        return self._get_current_data({"current": "snowfall"})

    def is_day_or_night(self) -> int:
        r"""
        Returns whether it's day or night at the specified coordinates.
        Returns integer `1` for daytime and `0` for night time.
        """
        return self._get_current_data({"current": "is_day"})

    def get_hourly_visibility(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly visibility data
        in meters(m) at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "visibility"})

    def get_hourly_precipitation_probability(self) -> pd.DataFrame:
        r"""
        Returns the probability of precipitation (rain/showers/snowfall)
        in percentage(%) at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "precipitation_probability"})

    def get_hourly_wind_speed(
        self, altitude: int = 10, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly wind speed data at the
        specified coordinates and altitude in the specified unit.

        Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """
        self._verify_wind_altitude(altitude)
        self._verify_wind_speed_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_hourly_wind_direction(
        self, altitude: constants.WIND_ALTITUDE = 10
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly wind direction data in degrees at
        the specified coordinates and altitude in the specified unit.

        Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        """
        self._verify_wind_altitude(altitude)
        return self._get_periodical_data({"hourly": f"wind_direction_{altitude}m"})

    def get_daily_max_uv_index(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily maximum Ultra-Violet (UV)
        index data at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "uv_index_max"})

    def get_daily_max_precipitation_probability(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily maximum precipitation probability
        (rain/showers/snowfall) in percentage (%) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "precipitation_probability_max"})
