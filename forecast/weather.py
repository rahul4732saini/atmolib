r"""
This module defines the Weather class facilitating the retrieval of weather data from
the Open-Meteo Weather API based on latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather information, including 
current weather data and up to upcoming 16-days hourly and daily weather forecast data.
"""

import requests
import pandas as pd

from common import constants
from objects import BaseForecast


class Weather(BaseForecast):
    r"""
    Weather class to extract weather data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Weather API to fetch the current or upcoming 16-days
    hourly and daily weather forecast data.

    Params:
    - lat (int | float): Latitudinal coordinates of the location.
    - long (int | float): Longitudinal coordinates of the location.
    - forecast_days (int): Number of days for which the forecast has to
    be extracted, must be in the range of 1 and 16.
    """

    __slots__ = "_lat", "_long", "_params", "_forecast_days"

    _api = constants.WEATHER_API
    _session = requests.Session()

    # The maximum number of days for which forecast data can be requested.
    _max_forecast_days = 16

    def get_current_temperature(
        self,
        altitude: constants.TEMPERATURE_ALTITUDE = 2,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> float:
        r"""
        Returns the current temperature in the supplied temperature unit
        at the supplied altitude in meters(m) from the ground level.

        Params:
        - altitude (int): Altitude from the ground level, must be in 2, 80, 120 or 180.
        - unit (str): Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 2, 80, 120 or 180, got {altitude}."
            )

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_current_weather_data(
            {"current": f"temperature_{altitude}m", "temperature_unit": unit}
        )

    def get_current_weather_code(self) -> tuple[int | float, str]:
        r"""
        Returns a tuple comprising the current weather code followed
        by a string description of the weather code.
        """

        weather_code: int | float = self.get_current_weather_data(
            {"current": "weather_code"}
        )
        description: str = constants.WEATHER_CODES[str(weather_code)]

        return weather_code, description

    def get_current_total_cloud_cover(self) -> int | float:
        r"""
        Returns the current total cloud cover in percentage(%) at the supplied coordinates.
        """
        return self.get_current_weather_data({"current": "cloud_cover"})

    def get_current_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> int | float:
        r"""
        Returns the current cloud cover in percentage(%) at the supplied level and coordinates.

        Params:
        - level (str): Altitude level of the desired cloud coverage, must be one of the following:
            - 'low' (clouds and fog up to an altitude of 3 km.)
            - 'mid' (clouds at an altitude between 3 km and 8 km.)
            - 'high' (clouds at an altitude higher than 8 km.)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(
                f"Expected `level` to be 'low', 'mid' or 'high', got {level!r}."
            )

        return self.get_current_weather_data({"current": f"cloud_cover_{level}"})

    def get_current_apparent_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> int | float:
        r"""
        Returns the current apparent temperature at the supplied coordinates.

        Apparent temperature is the perceived feels-like temperature
        combining wind chill factor, relative humidity and solar radiation.

        Params:
        - unit (str): Temperature unit must be 'celsius' or 'fahrenheit'.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_current_weather_data(
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
        - altitude (int): Altitude from the ground level, Must be 10, 80, 120 or 180.
        - unit (str): Wind speed unit, must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 10, 80, 120 or 180, got {altitude}."
            )

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be 'kmh', 'mph', 'ms' or 'kn', got {unit!r}."
            )

        return self.get_current_weather_data(
            {"current": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_current_wind_direction(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
    ) -> int | float:
        r"""
        Returns the current wind direction at the supplied altitude and in the supplied unit.

        Params:
        - altitude (int): Altitude from the ground level, must be 10, 80, 120 or 180.
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 10, 80, 120 or 180, got {altitude}."
            )

        return self.get_current_weather_data({"current": f"wind_direction_{altitude}m"})

    def get_current_wind_gusts(
        self, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> int | float:
        r"""
        Returns the current wind gusts above 10 meters(m) from ground level in the supplied unit.

        Params:
        - unit (str): Wind speed unit, must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be 'kmh', 'mph', 'ms' or 'kn', got {unit!r}."
            )

        return self.get_current_weather_data(
            {"current": "wind_gusts_10", "wind_speed_unit": unit}
        )

    def get_current_relative_humidity(self) -> int | float:
        r"""
        Returns the current relative humidity 2 meters(m) above the
        ground level in percentage(%) at the supplied coordinates.
        """
        return self.get_current_weather_data({"current": "relative_humidity_2m"})

    def get_current_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> int | float:
        r"""
        Returns the current precipitation (sum of rain, showers, and snowfall) at
        the supplied coordinates.

        Params:
        - unit: Precipitation unit, must be 'mm' or 'inch'.
        """

        if unit not in ("mm", "inch"):
            raise ValueError(f"Expected `unit` to be 'mm' or 'inch'. Got {unit!r}.")

        return self.get_current_weather_data(
            {"current": "precipitation", "precipitation_unit": unit}
        )

    def get_daily_temperature(
        self,
        type_: constants.DAILY_WEATHER_REQUEST_TYPES,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily maximum, minimum or mean temperature data
        2 meters(m) above the ground level at the specified coordinates.

        Params:
        - type: Specifies the type of daily temperature to be retrieved,
        must be 'min', 'max' or 'mean'.
            - 'min': Daily minimum temperature.
            - 'max': Daily maximum temperature.
            - 'mean': Daily mean temperature.
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if type_ not in ("max", "min", "mean"):
            raise ValueError(f"Expected `type` to be 'min' or 'max', got {type_!r}.")

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"daily": f"temperature_2m_{type}", "temperature_unit": unit}
        )

    def get_daily_apparent_temperature(
        self,
        type_: constants.DAILY_WEATHER_REQUEST_TYPES,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily maximum, minimum or mean apparent temperature
        data 2 meters(m) above the ground level at the specified coordinates.

        Params:
        - type: Specifies the type of daily apparent temperature to be retrieved,
        must be 'min', 'max' or 'mean'.
            - 'min': Daily minimum apparent temperature.
            - 'max': Daily maximum apparent temperature.
            - 'mean': Daily mean apparent temperature.
        - unit: Temperature unit, must be 'celsius' or 'fahrenheit'.
        """

        if type_ not in ("max", "min", "mean"):
            raise ValueError(f"Expected `type` to be 'min' or 'max', got {type_!r}.")

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit', got {unit!r}."
            )

        return self.get_periodical_data(
            {"daily": f"apparent_temperature_{type_}", "temperature_unit": unit}
        )

    def get_daily_dominant_wind_direction(self) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily dominant wind direction in degrees data 10 meters(m)
        above the ground level at the specified coordinates.
        """
        return self.get_periodical_data({"daily": "wind_direction_10m_dominant"})

    def get_daily_total_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly precipitation (sum of rain, showers, and snowfall)
        data at the specified coordinates.

        Params:
        - unit: Precipitation unit, must be 'mm' or 'inch'.
        """

        if unit not in ("mm", "inch"):
            raise ValueError(f"Expected `unit` to be 'mm' or 'inch', got {unit!r}.")

        return self.get_periodical_data(
            {"daily": "precipitation_sum", "precipitation_unit": unit}
        )
