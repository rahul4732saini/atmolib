r"""
Objects Module
--------------

This module comprises classes that serve as foundational components
for various objects and functionalities within the pyweather package.
"""

from typing import Any

import requests
import numpy as np
import pandas as pd

from .common import tools, constants


class BaseMeteor:
    r"""
    Base class for all meteorology classes.
    """

    _session: requests.Session
    _api: str

    __slots__ = "_lat", "_long", "_params"

    def __init__(self, lat: int | float, long: int | float) -> None:

        # `params`` dictionary to be used to store request parameters for API requests.
        self._params: dict[str, Any] = {}

        self.lat = lat
        self.long = long

    @property
    def lat(self) -> int | float:
        return self._lat

    @lat.setter
    def lat(self, __value: int | float) -> None:
        assert -90 <= __value <= 90, ValueError(
            f"`lat` must be in the range of -90 and 90; got {__value}."
        )
        self._lat = self._params["latitude"] = __value

    @property
    def long(self) -> int | float:
        return self._long

    @long.setter
    def long(self, __value: int | float) -> None:
        assert -180 <= __value <= 180, ValueError(
            f"`long` must be in the range of -90 and 90; got {__value}."
        )
        self._long = self._params["longitude"] = __value

    def _get_current_data(self, params: dict[str, Any]) -> int | float:
        r"""
        Uses the specified parameters to request the specified
        Open-Meteo API and returns the current weather data.

        #### Params:
        - params (dict[str, Any]): A dictionary all the necessary parameters except the
        coordinate parameters to request the Open-Meteo Weather API.
        """

        # `_session` and `_api` class attributes must be defined by the child class.
        data: int | float = tools.get_current_data(
            self._session, self._api, params | self._params
        )

        return data

    def _get_periodical_data(
        self, params: dict[str, Any], dtype=np.float16
    ) -> pd.Series:
        r"""
        Uses the specified parameters to request the specified Open-Meteo
        API and returns the periodical weather data as a pandas Series.

        #### Params:
        - params (dict[str, Any]): A dictionary all the necessary parameters except the
        coordinate parameters to request the Open-Meteo Weather API.
        - dtype: Desired numpy dtype of the request meteorology data.
        """

        # `_session` and `_api` class attributes must be defined by the child class.
        data: pd.Series = tools.get_periodical_data(
            self._session, self._api, params | self._params, dtype
        )

        return data


class BaseForecast(BaseMeteor):
    r"""
    Base class for all weather forecast classes.
    """

    # This attribute must be explicitly defined in
    # the child classes as per their customs.
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

        # Asserts if the forecast days value is within the range of the maximum forecast
        # days assigned by the child class with the `_max_forecast_days` class attribute.
        assert __value in range(1, self._max_forecast_days + 1), ValueError(
            f"`forecast_days` must be in the range of 1 and {self._max_forecast_days}; got {__value!r}."
        )
        self._forecast_days = __value

        # Updating the `_params` dictionary with the 'forecast_days' key-value
        # pair to be used as a parameter for requesting the Web API.
        self._params["forecast_days"] = __value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(lat={self._lat}, long={self._long}, "
            f"forecast_days={self._forecast_days})"
        )


class BaseWeather(BaseMeteor):
    r"""
    Baseclass for all weather classes.
    """

    @staticmethod
    def _verify_temperature_unit(unit: constants.TEMPERATURE_UNITS) -> None:
        r"""
        Verifies the specified temperature unit. Raises a ValueError if the
        argument provided is not a valid unit.
        """

        if unit not in ("celsius", "fahrenheit"):
            raise ValueError(
                f"Expected `unit` to be 'celsius' or 'fahrenheit'; got {unit!r}."
            )

    @staticmethod
    def _verify_precipitation_unit(unit: constants.PRECIPITATION_UNITS) -> None:
        r"""
        Verifies the specified precipitation unit. Raises a ValueError if the
        argument provided is not a valid unit.
        """

        if unit not in ("mm", "inch"):
            raise ValueError(f"Expected `unit` to be 'mm' or 'inch'; got {unit!r}.")

    @staticmethod
    def _verify_wind_speed_unit(unit: constants.WIND_SPEED_UNITS) -> None:
        r"""
        Verifies the specified wind speed unit. Raises a ValueError if the
        argument provided is not a valid unit.
        """

        if unit not in ("kmh", "mph", "ms", "kn"):
            raise ValueError(
                f"Expected `unit` to be 'kmh', 'mph', 'ms' or 'kn'; got {unit!r}."
            )

    def _verify_units(
        self,
        temperature_unit: constants.TEMPERATURE_UNITS,
        precipitation_unit: constants.PRECIPITATION_UNITS,
        wind_speed_unit: constants.WIND_SPEED_UNITS,
    ) -> None:
        r"""
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
        r"""
        Returns a pandas Series of temperature data 2 meters(m) above
        the ground level at the specified coordinates.

        #### Params:
        - altitude (int): Altitude from the ground level; must be 2, 80, 120 or 180.
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
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
        r"""
        Returns a pandas Series of apparent temperature 2 meters(m) above
        the ground level data at the specified coordinates.

        #### Params:
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
        """
        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"hourly": "apparent_temperature", "temperature_unit": unit}
        )

    def get_hourly_dew_point(
        self, unit: constants.TEMPERATURE_UNITS = "celsius"
    ) -> pd.Series:
        r"""
        Returns a pandas Series of hourly dew point data 2 meters(m) above the
        ground level at the specified coordinates.

        #### Params:
        - unit (str): Temperature unit; must be 'celsius' or 'fahrenheit'.
        """
        self._verify_temperature_unit(unit)

        return self._get_periodical_data(
            {"hourly": "dew_point_2m", "temperature_unit": unit}
        )

    def get_hourly_relative_humidity(self) -> pd.Series:
        r"""
        Returns a pandas Series of hourly relative humidity percentage(%) data
        2 meters(m) above the ground level at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "relative_humidity_2m"})

    def get_periodical_weather_code(
        self, frequency: constants.FREQUENCY = "daily"
    ) -> pd.DataFrame:
        r"""
        Returns a pandas DataFrame of hourly weather code data with its corresponding
        description at the specified coordinates.

        #### Params:
        - frequency (str): Frequency of the data distribution; must be 'daily' or 'hourly'.

        #### Columns:
        - data: weather code at the corresponding hour (timeline as a part of the index).
        - description: description of the corresponding weather code.
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
        r"""
        Returns a pandas Series of hourly rainfall data
        in mm/inch at the specified coordinates.

        #### Params:
        - unit (str): Precipitation unit; must be 'mm' or 'inch'.
        """
        self._verify_precipitation_unit(unit)
        return self._get_periodical_data({"hourly": "rain", "precipitation_unit": unit})

    def get_hourly_snowfall(self) -> pd.Series:
        r"""
        Returns a pandas Series of hourly snowfall data
        in centimeters(cm) at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "rain"})

    def get_hourly_pressure(
        self, level: constants.PRESSURE_LEVELS = "surface"
    ) -> pd.Series:
        r"""
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
        r"""
        Returns a pandas Series of hourly total cloud cover percentage(%) data
        at the specified coordinates.
        """
        return self._get_periodical_data({"hourly": "cloud_cover"})

    def get_hourly_cloud_cover(
        self, level: constants.CLOUD_COVER_LEVEL = "low"
    ) -> pd.Series:
        r"""
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
        r"""
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
        r"""
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
        r"""
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
        r"""
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
        r"""
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
        r"""
        Returns a pandas Series of daily dominant wind direction in degrees data
        10 meters(m) above the ground level at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "wind_direction_10m_dominant"})

    def get_daily_max_wind_gusts(
        self, unit: constants.WIND_SPEED_UNITS = "kmh"
    ) -> pd.Series:
        r"""
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
        r"""
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
        r"""
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
        r"""
        Returns a pandas Series of daily rainfall data in
        centimeters(m) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "snowfall_sum"})

    def get_daily_sunrise_time(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily sunrise time in the ISO-8601 datetime
        format (YYYY-MM-DDTHH:MM) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "sunrise"}, dtype=np.object_)

    def get_daily_sunset_time(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily sunset time in the ISO-8601 datetime
        format (YYYY-MM-DDTHH:MM) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "sunset"}, dtype=np.object_)

    def get_daily_daylight_duration(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily daylight duration
        in seconds(s) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "daylight_duration"})

    def get_daily_sunshine_duration(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily sunshine duration
        in seconds(s) at the specified coordinates.
        """
        return self._get_periodical_data({"daily": "sunshine_duration"})

    def get_daily_total_shortwave_radiation(self) -> pd.Series:
        r"""
        Returns a pandas Series of daily sum of shortwave radiation in Mega
        Joules per square meter (MJ/m^2) sat the specified coordinates.
        """
        return self._get_periodical_data({"daily": "shortwave_radiation_sum"})
