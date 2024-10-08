"""
Weather Module
--------------

This module defines the Weather class facilitating extraction
of weather data from Open-Meteo's Weather API.
"""

import atexit
from typing import Any

import requests
import numpy as np
import pandas as pd

from ..common import constants, tools
from ..base import BaseForecast, BaseWeather


class Weather(BaseForecast, BaseWeather):
    """
    Weather class defines mechanism for extraction of weather data based on the
    latitudinal and longitudinal coordinates of the location. It interacts with
    Open-Meteo's Weather API to fetch the current or upto upcoming 16-days hourly
    and daily weather forecast data.
    """

    __slots__ = "_lat", "_long", "_params", "_forecast_days"

    _api = constants.WEATHER_API
    _session = requests.Session()

    # Maximum number of days for which forecast data can be extracted.
    _max_forecast_days = 16

    # Closes the request session upon exit.
    atexit.register(_session.close)

    def __init__(
        self, lat: int | float, long: int | float, forecast_days: int = 7
    ) -> None:
        """
        Creates an instance of the Weather class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - forecast_days (int): Number of days for which the forecast has to
        be extracted; must be in the range of 1 and 16. Defaults to 7.
        """
        super().__init__(lat, long, forecast_days)

    @staticmethod
    def _verify_wind_altitude(altitude: int) -> None:
        """
        Verifies the specified altitude for wind data extraction
        and raises a ValueError if found invalid.
        """

        if altitude not in (10, 80, 120, 180):
            raise ValueError(f"Invalid altitude value specified: {altitude!r}")

    def get_current_summary(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS = "celsius",
        precipitation_unit: constants.PRECIPITATION_UNITS = "mm",
        wind_speed_unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.Series:
        """
        Extracts current weather summary data in the specified
        temperature, precipitation, and wind speed unit.

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

        #### The summary data distribution includes the following:
        - temperature (2m above ground level)
        - relative humidity (2m above ground level)
        - precipitation (sum of rain/showers/snowfall)
        - weather code
        - cloud cover percentage
        - surface pressure in HPa (Hectopascal)
        - wind speed (10m above ground level)
        - wind direction in degrees (10m above ground level)
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
        """
        Extracts hourly weather summary forecast data in the
        specified temperature, precipitation, and wind speed unit.

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

        #### The summary data distribution includes the following:
        - temperature (2m above ground level)
        - relative humidity (2m above the ground level)
        - dew point (2m above ground level)
        - precipitation (sum of rain/showers/snowfall)
        - weather code
        - visibility in meters(m)
        - cloud cover percentage(%)
        - surface pressure in HPa (Hectopascal)
        - wind speed (10m above ground level)
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
        """
        Extracts daily weather summary forecast data in the
        specified temperature, precipitation, and wind speed unit.

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

        #### The summary data distribution includes the following:
        - mean temperature (2m above ground level)
        - total precipitation (sum of rain/showers/snowfall)
        - weather code
        - Daylight duration
        - max Ultra-Violet (UV) index
        - mean wind speed (10m above ground level)
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
        """
        Extracts current temperature at the specified altitude
        above the ground level in the specified temperature unit.

        #### Params:
        - altitude (int): Altitude in meters(m) above the ground level;
        must be one of 2, 80, 120, or 180. Defaults to 2.
        - unit (str): Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """

        if altitude not in (2, 80, 120, 180):
            raise ValueError(f"Invalid altitude level specified: {altitude}")

        self._verify_temperature_unit(unit)

        return self._get_current_data(
            {"current": f"temperature_{altitude}m", "temperature_unit": unit}
        )

    def get_current_weather_code(self) -> tuple[int, str]:
        """
        Extracts current weather code and returns a tuple
        comprising it along with its string description.
        """

        weather_code: int = int(self._get_current_data({"current": "weather_code"}))
        description: str = constants.WEATHER_CODES[str(weather_code)]

        return weather_code, description

    def get_current_total_cloud_cover(self) -> int | float:
        """
        Extracts current total cloud cover percentage(%).
        """
        return self._get_current_data({"current": "cloud_cover"})

    def get_current_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> int | float:
        """
        Extracts current cloud cover percentage(%)
        at the specified altitude level.

        #### Params:
        - level (str): Altitude level of the desired cloud coverage;
        must be one of the following:
            - 'low' (clouds and fog up to an altitude of 3 km)
            - 'mid' (clouds at an altitude between 3 km and 8 km)
            - 'high' (clouds at an altitude higher than 8 km)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(f"Invalid altitude level specified: {level!r}")

        return self._get_current_data({"current": f"cloud_cover_{level}"})

    def get_current_apparent_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> int | float:
        """
        Extracts current apparent temperature in the specified temperature unit.

        #### Params:
        - unit (str): Temperature unit; must be `celsius`
        or `fahrenhiet`. Defaults to `celsius`.

        #### Brief:
        Apparent temperature is the perceived feels-like temperature
        combining wind chill factor, relative humidity and solar radiation.
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
        """
        Extracts the current wind speed at the specified
        altitude and in the specified wind speed unit.

        #### Params:
        - altitude (int): Altitude from the ground level;
        must be 10, 80, 120 or 180. Defaults to 10.
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `ms` (meter per second)
            - `kn` (knots)

            Defaults to `kmh`.
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
        """
        Extracts current wind direction in degress at
        the specified altitude above the ground level.

        #### Params:
        - altitude (int): Altitude in meters(m) above the ground
        level; must be 10, 80, 120 or 180. Defaults to 10.
        """
        self._verify_wind_altitude(altitude)
        return self._get_current_data({"current": f"wind_direction_{altitude}m"})

    def get_current_wind_gusts(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> int | float:
        """
        Extracts current wind gusts at the specified
        altitude and in the specified wind speed unit.

        #### Params:
        - altitude (int): Altitude from the ground level;
        must be 10, 80, 120 or 180. Defaults to 10.
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `ms` (meter per second)
            - `kn` (knots)

            Defaults to `kmh`.
        """
        self._verify_wind_altitude(altitude)
        self._verify_wind_speed_unit(unit)

        return self._get_current_data(
            {"current": "wind_gusts_10m", "wind_speed_unit": unit}
        )

    def get_current_relative_humidity(self) -> int | float:
        """
        Extracts current relative humidity percentage(%)
        at 2 meters(m) above the ground level.
        """
        return self._get_current_data({"current": "relative_humidity_2m"})

    def get_current_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> int | float:
        """
        Extracts the current precipitation sum (rain + showers
        + snowfall) in the specified precipitation unit.

        #### Params:
        - unit: Precipitation unit; must be `mm` or `inch`. Defaults to `mm`.
        """
        self._verify_precipitation_unit(unit)
        return self._get_current_data(
            {"current": "precipitation", "precipitation_unit": unit}
        )

    def get_current_pressure(
        self, level: constants.PRESSURE_LEVELS = "surface"
    ) -> int | float:
        """
        Extracts current atmospheric pressure in Hectopascal(hPa)
        at the specified measurement level.

        #### Params:
        - level (str): Desired level of the atmospheric pressure
        data; must be `surface` or `sealevel`. Defaults to `surface`.
        """

        # Mapped value of the specified pressure level.
        pressure: str | None = constants.PRESSURE_LEVEL_MAPPING.get(level)

        if pressure is None:
            raise ValueError(f"Invalid measurement level specified: {level!r}")

        return self._get_current_data({"current": pressure})

    def get_current_rainfall(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> int | float:
        """
        Extracts the current rainfall in
        the specified precipitation unit.

        #### Params:
        - unit: Precipitation unit; must be `mm` or `inch`. Defaults to `mm`.
        """
        self._verify_precipitation_unit(unit)
        return self._get_current_data({"current": "rain", "precipitation_unit": unit})

    def get_current_snowfall(self) -> int | float:
        """
        Extracts current snowfall in centimeters(m).
        """
        return self._get_current_data({"current": "snowfall"})

    def get_current_visibility(self) -> int | float:
        """
        Extracts current visibility in meters(m).
        """
        return self._get_current_data({"current": "visibility"})

    def is_day_or_night(self) -> int:
        """
        Returns whether it's day or night. Returns the
        integer `1` for daytime and `0` for nighttime.
        """
        return int(self._get_current_data({"current": "is_day"}))

    def get_hourly_visibility(self) -> pd.Series:
        """
        Extracts hourly visibility data in meters(m).
        """
        return self._get_periodical_data({"hourly": "visibility"}, dtype=np.int32)

    def get_hourly_precipitation_probability(self) -> pd.Series:
        """
        Extracts hourly precipitation (rain
        + showers + snowfall) percentage(%).
        """
        return self._get_periodical_data({"hourly": "precipitation_probability"})

    def get_hourly_wind_speed(
        self,
        altitude: constants.WIND_ALTITUDE = 10,
        unit: constants.WIND_SPEED_UNITS = "kmh",
    ) -> pd.Series:
        """
        Extracts hourly wind speed data at the specified
        altitude and in the specified wind speed unit.

        #### Params:
        - altitude (int): Altitude from the ground level;
        must be 10, 80, 120 or 180. Defaults to 10.
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `ms` (meter per second)
            - `kn` (knots)

            Defaults to `kmh`.
        """
        self._verify_wind_altitude(altitude)
        self._verify_wind_speed_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"wind_speed_{altitude}m", "wind_speed_unit": unit}
        )

    def get_hourly_wind_direction(
        self, altitude: constants.WIND_ALTITUDE = 10
    ) -> pd.Series:
        """
        Extracts hourly wind direction data in degrees at
        the specified altitude above the ground level.

        #### Params:
        - altitude (int): Altitude from the ground level;
        must be 10, 80, 120 or 180. Defaults to 10.
        """
        self._verify_wind_altitude(altitude)
        return self._get_periodical_data({"hourly": f"wind_direction_{altitude}m"})

    def get_hourly_soil_temperature(
        self,
        depth: constants.SOIL_TEMP_DEPTH = 0,
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.Series:
        """
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
        """
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
        """Extracts daily maximum Ultra-Violet (UV) index data."""
        return self._get_periodical_data({"daily": "uv_index_max"})

    def get_daily_max_precipitation_probability(self) -> pd.Series:
        """
        Extracts daily maximum precipitation (rain +
        showers + snowfall) probability percentage(%).
        """
        return self._get_periodical_data({"daily": "precipitation_probability_max"})
