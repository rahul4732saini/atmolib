"""
Objects Module
--------------

This module comprises classes serving as foundational components
for the various other classes and functions within the package.
"""

from typing import Any

import requests
import numpy as np
import pandas as pd

from .common import tools, constants


class BaseMeteor:
    """
    Base class for all meteorology classes.
    """

    # The following class attributes are essential for operation and
    # must be explicitly defined by child classes as per requirements.
    _session: requests.Session
    _api: str

    __slots__ = "_lat", "_long", "_params"

    def __init__(self, lat: int | float, long: int | float) -> None:

        # 'params' dictionary to store parameters for API requests.
        self._params: dict[str, Any] = {}

        self.lat = lat
        self.long = long

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

    def _get_current_data(self, params: dict[str, Any]) -> int | float:
        """
        Extracts current meteorology data from Open-Meteo's
        API endpoints based on the specified parameters.

        #### Params:
        - params (dict[str, Any]): API request parameters.
        """
        return tools.get_current_data(self._session, self._api, params | self._params)

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
            self._session, self._api, params | self._params, dtype
        )


class BaseForecast(BaseMeteor):
    """
    Base class for all meteorological forecast classes.
    """

    # This class attribute is essential for operation and must be
    # explicitly defined by child classes as per requirements.
    _max_forecast_days: int

    __slots__ = "_lat", "_long", "_params", "_forecast_days"

    def __init__(
        self, lat: int | float, long: int | float, forecast_days: int = 7
    ) -> None:
        super().__init__(lat, long)
        self.forecast_days = forecast_days

    @property
    def forecast_days(self) -> int:
        return self._forecast_days

    @forecast_days.setter
    def forecast_days(self, __value: int) -> None:

        if __value not in range(1, self._max_forecast_days + 1):
            raise ValueError(
                "'forecast_days' must be an integer between 1 "
                f"and {self._max_forecast_days}."
            )

        # Also updates the request parameters mapping with
        # the forecast days value for usage in API requests.
        self._forecast_days = self._params["forecast_days"] = __value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(lat={self._lat}, long={self._long}, "
            f"forecast_days={self._forecast_days})"
        )


class BaseWeather(BaseMeteor):
    """
    Baseclass for all weather classes.
    """

    @staticmethod
    def _verify_temperature_unit(unit: constants.TEMPERATURE_UNITS) -> None:
        """
        Verifies the specified temperature unit
        and raises a ValueError if found invalid.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(f"Invalid temperature unit {unit!r}")

    @staticmethod
    def _verify_precipitation_unit(unit: constants.PRECIPITATION_UNITS) -> None:
        """
        Verifies the specified precipitation unit
        and raises a ValueError if found invalid.
        """

        if unit not in ("mm", "inch"):
            raise ValueError(f"Invalid precipitation unit {unit!r}")

    @staticmethod
    def _verify_wind_speed_unit(unit: constants.WIND_SPEED_UNITS) -> None:
        """
        Verifies the specified wind speed unit
        and raises a ValueError if found invalid.
        """

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(f"Invalid wind speed unit {unit!r}")

    def _verify_units(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS,
        precipitation_unit: constants.PRECIPITATION_UNITS,
        wind_speed_unit: constants.WIND_SPEED_UNITS,
    ) -> None:
        """
        Verifies the specified temperature, precipitation and wind speed units.
        """

        self._verify_temperature_unit(temperature_unit)
        self._verify_precipitation_unit(precipitation_unit)
        self._verify_wind_speed_unit(wind_speed_unit)

    def get_hourly_temperature(
        self,
        altitude: constants.TEMPERATURE_ALTITUDE = 2,
        unit: constants.TEMPERATURE_UNITS = "celsius",
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

        if altitude not in (2, 80, 120, 180):
            raise ValueError(
                f"Expected `altitude` to be 2, 80, 120 or 180; got {altitude}."
            )

        return self._get_periodical_data(
            {"hourly": f"temperature_{altitude}m", "temperature_unit": unit}
        )

    def get_hourly_apparent_temperature(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.Series:
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

    def get_hourly_dew_point(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.Series:
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

    def get_periodical_weather_code(
        self, frequency: constants.FREQUENCY = "daily"
    ) -> pd.DataFrame:
        """
        Extracts periodical weather code data with their
        corresponding descriptions at the specified frequency.

        #### Params:
        - frequency (str): Frequency of the data distribution;
        must be `daily` or `hourly`. Defaults to `daily`.
        """

        if frequency not in ("hourly", "daily"):
            raise ValueError(
                f"Expected `frequency` to be 'hourly' or 'daily'; got {frequency!r}."
            )

        data: pd.Series = self._get_periodical_data(
            {frequency: "weather_code"}, dtype=np.uint8
        )

        # Converting the Series into a pandas.DataFrame to
        # add a new column for weather code description.
        dataframe = data.to_frame("data")

        # Creating a new column 'description' mapped to the
        # description of the corresponding weather code.
        dataframe["description"] = dataframe.data.map(
            lambda x: constants.WEATHER_CODES[str(x)]
        )

        return dataframe

    def get_hourly_rainfall(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly rainfall data
        in mm/inch at the specified coordinates.

        #### Params:
        - unit (str): Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)
        return self._get_periodical_data({"hourly": "rain", "precipitation_unit": unit})

    def get_hourly_snowfall(self) -> pd.Series:
        """
        Returns a pandas Series of hourly snowfall data
        in centimeters(cm) at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "rain"})

    def get_hourly_pressure(
        self, level: constants.PRESSURE_LEVELS = "surface"
    ) -> pd.Series:
        """
        Returns a pandas Series of the hourly atmospheric pressure data
        in Hectopascal (hPa) at the specified coordinates.

        #### Params:
        - level (str): Desired level of the atmospheric data; must be 'surface' or 'sealevel'.
        """

        # Mapped value of the specified pressure level.
        pressure: str | None = constants.PRESSURE_LEVEL_MAPPING.get(level)

        if pressure is None:
            raise ValueError(
                f"Expected `level` to be 'sealevel' or 'surface'; got {level!r}."
            )

        return self._get_periodical_data({"hourly": pressure})

    def get_hourly_total_cloud_cover(self) -> pd.Series:
        """
        Returns a pandas Series of hourly total cloud cover percentage(%) data
        at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "cloud_cover"})

    def get_hourly_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly cloud cover percentage(%) data
        at the specified level and coordinates.

        #### Params:
        - level (str): Altitude level of the desired cloud coverage; must be
        one of the following:
            - 'low' (clouds and fog up to an altitude of 3 km.)
            - 'mid' (clouds at an altitude between 3 km and 8 km.)
            - 'high' (clouds at an altitude higher than 8 km.)
        """

        if level not in ("low", "mid", "high"):
            raise ValueError(
                f"Expected `level` to be 'low', 'mid' or 'high'; got {level!r}."
            )

        return self._get_periodical_data({"hourly": f"cloud_cover_{level}"})

    def get_hourly_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly precipitation (sum of rain, showers, and snowfall)
        data at the specified coordinates.

        #### Params:
        - unit (str): Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)

        return self._get_periodical_data(
            {"hourly": "precipitation", "precipitation_unit": unit}
        )

    def get_hourly_wind_gusts(
        self, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> pd.Series:
        """
        Returns a pandas Series of hourly wind gusts data 10 meters(m) above the
        ground level at the specified coordinates.

        #### Params:
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """
        self._verify_wind_speed_unit(unit)

        return self._get_periodical_data(
            {"hourly": f"wind_gusts_10m", "wind_speed_unit": unit}
        )

    def get_daily_temperature(
        self,
        type_: constants.DAILY_WEATHER_REQUEST_TYPES = "mean",
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.Series:
        """
        Returns a pandas Series of daily maximum, minimum or mean temperature data
        2 meters(m) above the ground level at the specified coordinates.

        #### Params:
        - type (str): The type of daily temperature to be extracted; must be 'min', 'max' or 'mean'.
            - 'min': Daily minimum temperature.
            - 'max': Daily maximum temperature.
            - 'mean': Daily mean temperature.
        - unit: Temperature unit; must be 'celsius' or 'fahrenheit'.
        """

        if type_ not in ("max", "min", "mean"):
            raise ValueError(f"Expected `type` to be 'min' or 'max'; got {type_!r}.")

        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"daily": f"temperature_2m_{type_}", "temperature_unit": unit}
        )

    def get_daily_apparent_temperature(
        self,
        type_: constants.DAILY_WEATHER_REQUEST_TYPES = "mean",
        unit: constants.TEMPERATURE_UNITS = "celsius",
    ) -> pd.Series:
        """
        Returns a pandas Series of daily maximum, minimum or mean apparent temperature
        data 2 meters(m) above the ground level at the specified coordinates.

        #### Params:
        - type (str): Specifies the type of daily apparent temperature to
        be retrieved; must be 'min', 'max' or 'mean'.
            - 'min': Daily minimum apparent temperature.
            - 'max': Daily maximum apparent temperature.
            - 'mean': Daily mean apparent temperature.
        - unit: Temperature unit; must be 'celsius' or 'fahrenheit'.
        """

        if type_ not in ("max", "min", "mean"):
            raise ValueError(f"Expected `type` to be 'min' or 'max'; got {type_!r}.")

        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"daily": f"apparent_temperature_{type_}", "temperature_unit": unit}
        )

    def get_daily_max_wind_speed(
        self, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> pd.Series:
        """
        Returns a pandas Series of daily maximum wind speed 2 meters(m)
        above the ground level at the specified coordinates.

        #### Params:
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """
        self._verify_wind_speed_unit(unit)
        return self._get_periodical_data({"daily": "wind_speed_10m_max"})

    def get_daily_dominant_wind_direction(self) -> pd.Series:
        """
        Returns a pandas Series of daily dominant wind direction in degrees data
        10 meters(m) above the ground level at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "wind_direction_10m_dominant"})

    def get_daily_max_wind_gusts(
        self, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> pd.Series:
        """
        Returns a pandas Series daily maximum wind gusts 2 meters(m)
        above the ground level at the specified coordinates.

        #### Params:
        - unit (str): Wind speed unit; must be one of the following:
            - 'kmh' (kilometers per hour)
            - 'mph' (miles per hour)
            - 'ms' (meter per second)
            - 'kn' (knots)
        """
        self._verify_wind_speed_unit(unit)
        return self._get_periodical_data({"daily": "wind_gusts_10m_max"})

    def get_daily_total_precipitation(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> pd.Series:
        """
        Returns a pandas Series of daily precipitation (sum of rain, showers, and snowfall)
        data at the specified coordinates.

        #### Params:
        - unit (str): Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)

        return self._get_periodical_data(
            {"daily": "precipitation_sum", "precipitation_unit": unit}
        )

    def get_daily_total_rainfall(
        self, unit: constants.PRECIPITATION_UNITS = "mm"
    ) -> pd.Series:
        """
        Returns a pandas Series of daily rainfall data
        in mm/inch at the specified coordinates.

        #### Params:
        - unit (str): Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)

        return self._get_periodical_data(
            {"daily": "rain_sum", "precipitation_unit": unit}
        )

    def get_daily_total_snowfall(self) -> pd.Series:
        """
        Returns a pandas Series of daily rainfall data in
        centimeters(m) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "snowfall_sum"})

    def get_daily_sunrise_time(self) -> pd.Series:
        """
        Returns a pandas Series of daily sunrise time in the ISO-8601 datetime
        format (YYYY-MM-DDTHH:MM) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "sunrise"}, dtype=np.object_)

    def get_daily_sunset_time(self) -> pd.Series:
        """
        Returns a pandas Series of daily sunset time in the ISO-8601 datetime
        format (YYYY-MM-DDTHH:MM) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "sunset"}, dtype=np.object_)

    def get_daily_daylight_duration(self) -> pd.Series:
        """
        Returns a pandas Series of daily daylight duration
        in seconds(s) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "daylight_duration"})

    def get_daily_sunshine_duration(self) -> pd.Series:
        """
        Returns a pandas Series of daily sunshine duration
        in seconds(s) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "sunshine_duration"})

    def get_daily_total_shortwave_radiation(self) -> pd.Series:
        """
        Returns a pandas Series of daily sum of shortwave radiation in Mega
        Joules per square meter (MJ/m^2) sat the specified coordinates.
        """
        return self._get_periodical_data({"daily": "shortwave_radiation_sum"})
