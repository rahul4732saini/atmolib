"""
Base Module
-----------

This module comprises classes serving as foundational components
for the various other classes and functions within the package.
"""

from typing import Any

import requests
import numpy as np
import pandas as pd

from .common import tools, constants


class BaseMeteor:
    """Base class for all meteorology classes."""

    # The following class attributes are essential for operation and
    # must be explicitly defined by child classes as per requirements.
    _session: requests.Session
    _api: str

    __slots__ = "_lat", "_long", "_timeout", "_params"

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
    ) -> None:

        # Stores parameters for API requests.
        self._params: dict[str, Any] = {}

        self.lat = lat
        self.long = long
        self.timeout = timeout

    @property
    def lat(self) -> int | float:
        return self._lat

    @lat.setter
    def lat(self, __value: int | float) -> None:
        if __value < -90 or __value > 90:
            raise ValueError(f"'lat' must be a number between -90 and 90.")

        self._lat = self._params["latitude"] = __value

    @property
    def long(self) -> int | float:
        return self._long

    @long.setter
    def long(self, __value: int | float) -> None:
        if __value < -180 or __value > 180:
            raise ValueError(f"'long' must be a number between -180 and 180.")

        self._long = self._params["longitude"] = __value

    @property
    def timeout(self) -> int | float | None:
        return self._timeout

    @timeout.setter
    def timeout(self, __value: int | float | None) -> None:

        if __value is not None and __value <= 0:
            raise ValueError("'timeout' must be a greater than 0 or None.")

        self._timeout = __value

    def _get_periodical_data(
        self, params: dict[str, Any], dtype=np.float32
    ) -> pd.Series:
        """
        Extracts periodical meteorology data from Open-Meteo's
        API endpoints based on the specified parameters.

        #### Params:
        - params (dict[str, Any]): API request parameters.
        - dtype: numpy datatype for meteorology data storage.
        Defaults to float32 (32-bit floating point number).
        """
        return tools.get_periodical_data(
            self._session, self._api, params | self._params, dtype, self._timeout
        )


class BaseForecast(BaseMeteor):
    """Base class for all meteorological forecast classes."""

    # This class attribute is essential for operation and must be
    # explicitly defined by child classes as per requirements.
    _max_forecast_days: int

    __slots__ = "_lat", "_long", "_params", "_forecast_days", "_past_days"

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        forecast_days: int = 7,
        past_days: int = constants.DEFAULT_PAST_DAYS,
        timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
    ) -> None:
        super().__init__(lat, long, timeout)

        self.forecast_days = forecast_days
        self.past_days = past_days

    @property
    def forecast_days(self) -> int:
        return self._forecast_days

    @forecast_days.setter
    def forecast_days(self, __value: int) -> None:

        if __value not in range(1, self._max_forecast_days + 1):
            raise ValueError(
                "'forecast_days' must be an integer between"
                f" 1 and {self._max_forecast_days}."
            )

        # Also updates the request parameters mapping with
        # the forecast days value for usage in API requests.
        self._forecast_days = self._params["forecast_days"] = __value

    @property
    def past_days(self) -> int:
        return self._past_days

    @past_days.setter
    def past_days(self, __value: int) -> None:

        if __value not in range(constants.MAX_PAST_DAYS + 1):
            raise ValueError(
                "'past_days' must be an integer between"
                f" 0 and {constants.MAX_PAST_DAYS}."
            )

        # Also updates the request parameters mapping with
        # the past days value for usage in API requests.
        self._past_days = self._params["past_days"] = __value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(lat={self._lat}, long={self._long},"
            f" forecast_days={self._forecast_days})"
        )

    def _get_current_data(self, params: dict[str, Any]) -> int | float:
        """
        Extracts current meteorology data from Open-Meteo's
        API endpoints based on the specified parameters.

        #### Params:
        - params (dict[str, Any]): API request parameters.
        """
        return tools.get_current_data(
            self._session, self._api, params | self._params, self._timeout
        )


class BaseWeather(BaseMeteor):
    """Baseclass for all weather classes."""

    @staticmethod
    def _verify_temperature_unit(unit: str) -> None:
        """
        Verifies the specified temperature unit
        and raises a ValueError if found invalid.
        """

        if unit not in constants.TEMPERATURE_UNITS:
            raise ValueError(f"Invalid temperature unit specified: {unit!r}")

    @staticmethod
    def _verify_precipitation_unit(unit: str) -> None:
        """
        Verifies the specified precipitation unit
        and raises a ValueError if found invalid.
        """

        if unit not in constants.PRECIPITATION_UNITS:
            raise ValueError(f"Invalid precipitation unit specified: {unit!r}")

    @staticmethod
    def _verify_wind_speed_unit(unit: str) -> None:
        """
        Verifies the specified wind speed unit
        and raises a ValueError if found invalid.
        """

        if unit not in constants.WIND_SPEED_UNITS:
            raise ValueError(f"Invalid wind speed unit specified: {unit!r}")

    def _verify_units(
        self, temperature_unit: str, precipitation_unit: str, wind_speed_unit: str
    ) -> None:
        """
        Verifies the specified temperature, precipitation and wind speed units.
        """

        self._verify_temperature_unit(temperature_unit)
        self._verify_precipitation_unit(precipitation_unit)
        self._verify_wind_speed_unit(wind_speed_unit)

    def get_hourly_temperature(
        self, altitude: int = 2, unit: str = "celsius"
    ) -> pd.Series:
        """
        Extracts hourly temperature data at the specified altitude
        above the ground level in the specified temperature unit.

        #### Params:
        - altitude (int): Altitude in meters(m) above the ground level;
        must be one of 2, 80, 120, or 180. Defaults to 2.
        - unit (str): Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """
        self._verify_temperature_unit(unit)

        if altitude not in constants.TEMPERATURE_ALTITUDES:
            raise ValueError(f"Invalid altitude level specified: {altitude}")

        return self._get_periodical_data(
            {"hourly": f"temperature_{altitude}m", "temperature_unit": unit}
        )

    def get_hourly_apparent_temperature(self, unit: str = "celsius") -> pd.Series:
        """
        Extracts hourly apparent temperature data at 2 meters(m)
        above the ground level in the specified temperature unit.

        #### Params:
        - unit (str): Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """
        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"hourly": "apparent_temperature", "temperature_unit": unit}
        )

    def get_hourly_dew_point(self, unit: str = "celsius") -> pd.Series:
        """
        Extracts hourly dew point data at 2 meters(m) above
        the ground level in the specified temperature unit.

        #### Params:
        - unit (str): Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """
        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"hourly": "dew_point_2m", "temperature_unit": unit}
        )

    def get_hourly_relative_humidity(self) -> pd.Series:
        """
        Extracts hourly relative humidity percentage(%)
        data at 2 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "relative_humidity_2m"})

    def get_periodical_weather_code(self, frequency: str = "daily") -> pd.DataFrame:
        """
        Extracts periodical weather code data with their corresponding
        descriptions at the specified measurement frequency.

        #### Params:
        - frequency (str): Frequency of the data distribution;
        must be `daily` or `hourly`. Defaults to `daily`.
        """

        if frequency not in constants.FREQUENCIES:
            raise ValueError(f"Invalid frequency specified: {frequency!r}")

        data: pd.Series = self._get_periodical_data(
            {frequency: "weather_code"}, dtype=np.uint8
        )

        # Converting the Series into a pandas.DataFrame object
        # to add a new column for weather code descriptions.
        dataframe = data.to_frame("data")

        # Creating a new column 'description' mapped to the
        # description of the corresponding weather codes.
        dataframe["description"] = dataframe["data"].map(
            lambda code: constants.WEATHER_CODES[str(code)]
        )

        return dataframe

    def get_hourly_rainfall(self, unit: str = "mm") -> pd.Series:
        """
        Extracts hourly rainfall data in the specified precipitation unit.

        #### Params:
        - unit (str): Precipitation unit; must be `mm` or `inch`. Defaults to `mm`.
        """
        self._verify_precipitation_unit(unit)
        return self._get_periodical_data({"hourly": "rain", "precipitation_unit": unit})

    def get_hourly_snowfall(self) -> pd.Series:
        """Extracts hourly snowfall data in centimeters(cm)."""
        return self._get_periodical_data({"hourly": "rain"})

    def get_hourly_pressure(self, level: str = "surface") -> pd.Series:
        """
        Extracts hourly atmospheric pressure data in Hectopascals(hPa)
        at the specified measurement level.

        #### Params:
        - level (str): Desired measurement level; must be `surface`
        or `sealevel`. Defaults to `surface`.
        """

        # Extracts the request metric based on the specified measurement level.
        metric: str | None = constants.PRESSURE_LEVEL_MAPPING.get(level)

        if metric is None:
            raise ValueError(f"Invalid measurement level specified: {level!r}")

        return self._get_periodical_data({"hourly": metric})

    def get_hourly_total_cloud_cover(self) -> pd.Series:
        """Extracts hourly total cloud cover percentage(%) data."""
        return self._get_periodical_data({"hourly": "cloud_cover"})

    def get_hourly_cloud_cover(self, level: str = "low") -> pd.Series:
        """
        Extracts hourly cloud cover percentage(%)
        data at the specified altitude level.

        #### Params:
        - level (str): Altitude level of the desired cloud coverage; must be
        one of the following:
            - `low` (clouds and fog up to an altitude of 3 km)
            - `mid` (clouds at an altitude between 3 km and 8 km)
            - `high` (clouds at an altitude higher than 8 km)

            Defaults to `low`.
        """

        if level not in constants.CLOUD_COVER_LEVELS:
            raise ValueError(f"Invalid altitude level specified: {level!r}")

        return self._get_periodical_data({"hourly": f"cloud_cover_{level}"})

    def get_hourly_precipitation(self, unit: str = "mm") -> pd.Series:
        """
        Extracts hourly precipitation (rain + showers + snowfall)
        data in the specified precipitation unit.

        #### Params:
        - unit (str): Precipitation unit; must be `mm` or `inch`. Defaults to `mm`.
        """
        self._verify_precipitation_unit(unit)

        return self._get_periodical_data(
            {"hourly": "precipitation", "precipitation_unit": unit}
        )

    def get_hourly_wind_gusts(self, unit: str = "kmh") -> pd.Series:
        """
        Extracts hourly wind gusts data at 10 meters(m) above
        the ground level in the specified wind speed unit.

        #### Params:
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `kn` (knots)
            - `ms` (meter per second)

            Defaults to `kmh`.
        """
        self._verify_wind_speed_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"wind_gusts_10m", "wind_speed_unit": unit}
        )

    def get_daily_temperature(
        self, metric: str = "mean", unit: str = "celsius"
    ) -> pd.Series:
        """
        Extracts daily temperature statistical metrics (max, min, mean)
        at 2 meters(m) above ground level in the specified temperature unit.

        #### Params:
        - metric (str): Statistical metric to be extracted;
        must be `min`, `max` or `mean`. Defaults to `mean`.
        - unit: Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """

        if metric not in constants.DAILY_WEATHER_STATISTICAL_METRICS:
            raise ValueError(f"Invalid statistical metric specified: {metric!r}")

        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"daily": f"temperature_2m_{metric}", "temperature_unit": unit}
        )

    def get_daily_apparent_temperature(
        self, metric: str = "mean", unit: str = "celsius"
    ) -> pd.Series:
        """
        Extracts daily apparent temperature statistical metrics (max, min, mean)
        at 2 meters(m) above the ground level in the specified temperature unit.

        #### Params:
        - metric (str): Statistical metric to be extracted;
        must be `min`, `max` or `mean`. Defaults to `mean`.
        - unit: Temperature unit; must be `celsius` or `fahrenheit`.
        Defaults to `celsius`.
        """

        if metric not in constants.DAILY_WEATHER_STATISTICAL_METRICS:
            raise ValueError(f"Invalid statistical metric specified: {metric!r}")

        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"daily": f"apparent_temperature_{metric}", "temperature_unit": unit}
        )

    def get_daily_max_wind_speed(self, unit: str = "kmh") -> pd.Series:
        """
        Extracts daily maximum wind speed data at 2 meters(m) above
        the ground level in the specified wind speed unit.

        #### Params:
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `kn` (knots)
            - `ms` (meter per second)

            Defaults to `kmh`.
        """
        self._verify_wind_speed_unit(unit)
        return self._get_periodical_data({"daily": "wind_speed_10m_max"})

    def get_daily_dominant_wind_direction(self) -> pd.Series:
        """
        Extracts daily dominant wind direction data in
        degrees at 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"daily": "wind_direction_10m_dominant"})

    def get_daily_max_wind_gusts(self, unit: str = "kmh") -> pd.Series:
        """
        Extracts daily maximum wind gusts at 2 meters(m) above
        the ground level in the specified wind speed unit.

        #### Params:
        - unit (str): Wind speed unit; must be one of the following:
            - `kmh` (kilometers per hour)
            - `mph` (miles per hour)
            - `ms` (meter per second)
            - `kn` (knots)

            Defaults to `kmh`.
        """
        self._verify_wind_speed_unit(unit)
        return self._get_periodical_data({"daily": "wind_gusts_10m_max"})

    def get_daily_total_precipitation(self, unit: str = "mm") -> pd.Series:
        """
        Extracts daily total precipitation (rain + showers + snowfall)
        sum data in the specified precipitation unit.

        #### Params:
        - unit (str): Precipitation unit; must be `mm` or `inch`. Defaults to `mm`.
        """
        self._verify_precipitation_unit(unit)

        return self._get_periodical_data(
            {"daily": "precipitation_sum", "precipitation_unit": unit}
        )

    def get_daily_total_rainfall(self, unit: str = "mm") -> pd.Series:
        """
        Extracts daily total rainfall data in the specified precipitation unit.

        #### Params:
        - unit (str): Precipitation unit; must be `mm` or `inch`. Defaults to `mm`.
        """
        self._verify_precipitation_unit(unit)

        return self._get_periodical_data(
            {"daily": "rain_sum", "precipitation_unit": unit}
        )

    def get_daily_total_snowfall(self) -> pd.Series:
        """Extracts daily total snowfall data in centimeters(cm)."""
        return self._get_periodical_data({"daily": "snowfall_sum"})

    def get_daily_sunrise_time(self) -> pd.Series:
        """
        Extracts daily sunrise time in the ISO-8601
        datetime format (YYYY-MM-DDTHH:MM).
        """
        return self._get_periodical_data({"daily": "sunrise"}, dtype=np.object_)

    def get_daily_sunset_time(self) -> pd.Series:
        """
        Extracts daily sunset time in the ISO-8601
        datetime format (YYYY-MM-DDTHH:MM).
        """
        return self._get_periodical_data({"daily": "sunset"}, dtype=np.object_)

    def get_daily_daylight_duration(self) -> pd.Series:
        """Extracts daily daylight duration time in seconds(s)"""
        return self._get_periodical_data({"daily": "daylight_duration"})

    def get_daily_sunshine_duration(self) -> pd.Series:
        """Extracts daily sunlight duration time in seconds(s)."""
        return self._get_periodical_data({"daily": "sunshine_duration"})

    def get_daily_total_shortwave_radiation(self) -> pd.Series:
        """
        Extracts daily shortwave radiation sum
        in Mega Joules per square meter (MJ/m^2).
        """
        return self._get_periodical_data({"daily": "shortwave_radiation_sum"})
