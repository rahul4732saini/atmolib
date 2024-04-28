r"""
Weather Module
--------------

This module defines the Weather class facilitating the extraction of weather data from the
Open-Meteo Weather API based on the latitudinal and longitudinal coordinates of the location.

The Weather class allows users to extract various types of weather data including current
weather data and up to upcoming 16-days hourly and daily weather forecast data.
"""

import atexit
from typing import Any

import requests
import numpy as np
import pandas as pd

from ..common import constants, tools
from ..objects import BaseForecast, BaseWeather


class Weather(BaseForecast, BaseWeather):
    r"""
    Weather class to extract weather data based on the latitudinal and longitudinal
    coordinates of the location. It interacts with the Open-Meteo Weather API to fetch
    the current or upcoming 16-days hourly and daily weather forecast data.
    """

    __slots__ = "_lat", "_long", "_params", "_forecast_days"

    _api = constants.WEATHER_API
    _session = requests.Session()

    # The maximum number of days in the future for forecast data extraction.
    _max_forecast_days = 16

    # Closes the request session upon exit.
    atexit.register(_session.close)

    def __init__(
        self, lat: int | float, long: int | float, forecast_days: int = 7
    ) -> None:
        r"""
        Creates an instance of the Weather class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - forecast_days (int): Number of days for which the forecast has to
        be extracted; must be in the range of 1 and 16.
        """
        super().__init__(lat, long, forecast_days)

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

    def get_current_summary(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS = "celsius",
        precipitation_unit: constants.PRECIPITATION_UNITS = "mm",
        wind_speed_unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.Series:
        r"""
        Returns a pandas Series of current weather summary data
        at the specified coordinates in the specified units.

        #### The weather summary data includes the following data types:
        - temperature (2m above the ground level)
        - relative humidity (2m above the ground level)
        - precipitation (sum of rain/showers/snowfall)
        - weather code
        - cloud cover percentage
        - surface pressure in HPa (Hecto-pascal)
        - wind speed (10m above the ground level)
        - wind direction in degrees (10m above the ground level)
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # A string representation of the weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = ",".join(constants.CURRENT_WEATHER_SUMMARY_DATA_TYPES)

        params: dict[str, Any] = {
            "current": data_types,
            "temperature_unit": temperature_unit,
            "precipitation_unit": precipitation_unit,
            "wind_speed_unit": wind_speed_unit,
        }

        return tools.get_current_summary(
            self._session,
            self._api,
            self._params | params,
            constants.CURRENT_WEATHER_SUMMARY_INDEX_LABELS,
        )

    def get_hourly_summary(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS = "celsius",
        precipitation_unit: constants.PRECIPITATION_UNITS = "mm",
        wind_speed_unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly weather summary data
        at the specified coordinates in the specified units.

        #### The weather summary data includes the following data types:
        - temperature (2m above the ground level)
        - relative humidity (2m above the ground level)
        - dew point (2m above the ground level)
        - precipitation (sum of rain/showers/snowfall)
        - weather code
        - visibility in meters(m)
        - cloud cover percentage(%)
        - surface pressure in HPa (Hecto-pascal)
        - wind speed (10m above the ground level)
        - surface soil temperature
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # A string representation of the weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = ",".join(constants.HOURLY_WEATHER_SUMMARY_DATA_TYPES)

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
            constants.HOURLY_WEATHER_SUMMARY_COLUMN_LABELS,
        )

    def get_daily_summary(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS = "celsius",
        precipitation_unit: constants.PRECIPITATION_UNITS = "mm",
        wind_speed_unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of daily weather summary data
        at the specified coordinates in the specified units.

        #### The weather summary data includes the following data types:
        - mean temperature (2m above the ground level)
        - total precipitation (sum of rain/showers/snowfall)
        - weather code
        - Daylight duration
        - max Ultra-Violet (UV) index
        - mean wind speed (10m above the ground level)
        - dominant wind direction
        """
        self._verify_units(temperature_unit, precipitation_unit, wind_speed_unit)

        # A string representation of the weather summary data types
        # separated by commas as supported for requesting the Web API.
        data_types: str = ",".join(constants.DAILY_WEATHER_SUMMARY_DATA_TYPES)

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
            constants.DAILY_WEATHER_SUMMARY_COLUMN_LABELS,
        )

    def get_current_temperature(
        self,
        altitude: constants.TEMPERATURE_ALTITUDE = 2,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> int | float:
        r"""
        Returns the current temperature in the specified temperature unit
        at the specified altitude in meters(m) from the ground level.

        #### Params:
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

    def get_current_weather_code(self) -> tuple[int, str]:
        r"""
        Returns a tuple comprising the current weather code followed
        by a string description of the weather code.
        """

        weather_code: int = int(self._get_current_data({"current": "weather_code"}))

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

        #### Params:
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

        #### Params:
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

        #### Params:
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

        #### Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        """
        self._verify_wind_altitude(altitude)
        return self._get_current_data({"current": f"wind_direction_{altitude}m"})

    def get_current_wind_gusts(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> int | float:
        r"""
        Returns the current wind gusts above 10 meters(m) from ground level in the specified unit.

        #### Params:
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
            {"current": "wind_gusts_10m", "wind_speed_unit": unit}
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

        #### Params:
        - unit: Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)
        return self._get_current_data(
            {"current": "precipitation", "precipitation_unit": unit}
        )

    def get_current_pressure(
        self, level: constants.PRESSURE_LEVELS = "surface"
    ) -> int | float:
        r"""
        Returns the current atmospheric pressure in Hectopascal (hPa)
        at the specified level and coordinates.

        #### Params:
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

        #### Params:
        - unit: Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)
        return self._get_current_data({"current": "rain", "precipitation_unit": unit})

    def get_current_snowfall(self) -> int | float:
        r"""
        Returns the current snowfall in centimeters(cm) at the specified coordinates.
        """
        return self._get_current_data({"current": "snowfall"})

    def get_current_visibility(self) -> int | float:
        r"""
        Returns the current visibility in meters(m) at the specified coordinates.
        """
        return self._get_current_data({"current": "visibility"})

    def is_day_or_night(self) -> int:
        r"""
        Returns whether it's day or night at the specified coordinates.
        Returns integer `1` for daytime and `0` for nighttime.
        """
        return int(self._get_current_data({"current": "is_day"}))

    def get_hourly_visibility(self) -> pd.Series:
        r"""
        Returns a pandas Series of hourly visibility data
        in meters(m) at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "visibility"}, dtype=np.int32)

    def get_hourly_precipitation_probability(self) -> pd.Series:
        r"""
        Returns a pandas Series of precipitation (rain/showers/snowfall)
        probability in percentage(%) at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "precipitation_probability"})

    def get_hourly_wind_speed(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.Series:
        r"""
        Returns a pandas Series of hourly wind speed data at the
        specified coordinates and altitude in the specified unit.

        #### Params:
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
    ) -> pd.Series:
        r"""
        Returns a pandas Series of hourly wind direction data in degrees at
        the specified coordinates and altitude in the specified unit.

        #### Params:
        - altitude (int): Altitude from the ground level; must be 10, 80, 120 or 180.
        """
        self._verify_wind_altitude(altitude)
        return self._get_periodical_data({"hourly": f"wind_direction_{altitude}m"})

    def get_hourly_soil_temperature(
        self,
        depth: constants.SOIL_TEMP_DEPTH = 0,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.Series:
        r"""
        Returns a pandas Series of hourly soil temperature data at
        the specified depth and coordinates in the specified unit.

        #### Params:
        - depth: Depth below the ground level at which soil temperature data is
        desired to be extracted in centimeters(cm); must be 0, 6, 18 or 54.
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
        """

        if depth not in (0, 6, 18, 54):
            raise ValueError(f"Expected `depth` to be 0, 6, 18 or 54; got {depth}.")

        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"soil_temperature_{depth}cm", "temperature_unit": unit}
        )

    def get_hourly_soil_moisture(self, depth: int = 7) -> pd.Series:
        r"""
        Returns a pandas Series of soil moisture (m^3/m^3)
        data at the specified depth and coordinates.

        #### Params:
        - depth (int): Desired depth of the soil moisture data within the ground level in
        centimeters(m). Moisture data is extracted as a part of a range of depth. Available
        depth ranges are 0-1cm, 1-3cmd, 3-9cm, 9-27cm, 27-81cm. The supplied depth must fall
        in the range of 0 and 81.
        """

        for key, value in constants.SOIL_MOISTURE_DEPTH.items():
            if depth in key:

                # The range is represented in a string format as being
                # a supported type for requesting the API.
                depth_range: str = value
                break

        else:
            raise ValueError(
                f"Expected `depth` to be in the range of 0 and 81; got {depth}."
            )

        return self._get_periodical_data({"hourly": f"soil_moisture_{depth_range}cm"})

    def get_daily_max_uv_index(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily maximum Ultra-Violet (UV)
        index data at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "uv_index_max"})

    def get_daily_max_precipitation_probability(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily maximum precipitation probability
        (rain/showers/snowfall) in percentage (%) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "precipitation_probability_max"})
