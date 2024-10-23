"""
Tests the classes and methods defined
within `atmolib/meteorology/weather.py`.
"""

from datetime import datetime
from typing import Any

import pytest
import numpy as np
import pandas as pd

import atmolib
from atmolib import constants


class TestWeather:
    """
    Tests the `atmolib.Weather` class and its defined methods.
    """

    def test_object_initialization(
        self, valid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """
        Test the `atmolib.Weather` object initialization with valid parameters.
        """

        for lat, long in valid_coordinates:
            atmolib.Weather(lat, long)

        for days in (1, 10, 16):
            atmolib.Weather(0, 0, days)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """
        Tests the `atmolib.Weather` object initialization with invalid parameters.
        """

        with pytest.raises(ValueError):

            # Expects an ValueError upon initialization with invalid coordinates.
            for lat, long in invalid_coordinates:
                atmolib.Weather(lat, long)

            # Expects an ValueError upon initialization with invalid forecast days.
            for days in (0, -1, 17):
                atmolib.Weather(0, 0, days)

    @staticmethod
    def _verify_summary_methods(
        current: pd.Series, hourly: pd.DataFrame, daily: pd.DataFrame
    ) -> None:
        """Verifies the execution of summary extraction methods."""

        assert isinstance(current, pd.Series)
        assert isinstance(hourly, pd.DataFrame)
        assert isinstance(daily, pd.DataFrame)

        assert current.index.tolist() == constants.CURRENT_WEATHER_SUMMARY_LABELS
        assert hourly.columns.tolist() == constants.HOURLY_WEATHER_SUMMARY_LABELS
        assert daily.columns.tolist() == constants.DAILY_WEATHER_SUMMARY_LABELS

    @staticmethod
    def _verify_temperature_data_series(series: pd.Series) -> None:
        """
        Verifies the temperature data within
        the specified pandas Series object.
        """

        assert isinstance(series, pd.Series)
        assert issubclass(series.dtype.type, np.integer | np.floating)

    @staticmethod
    def _verify_positive_data_series(series: pd.Series) -> None:
        """
        Verifies that all the values stored within the
        specified pandas Series object are greater than 0.
        """

        assert isinstance(series, pd.Series)
        assert all(series.to_numpy() >= 0)

    @staticmethod
    def _verify_cloud_cover_methods(current: int | float, hourly: pd.Series) -> None:
        """Verifies the current and hourly cloud coverage extraction methods."""

        assert isinstance(current, int | float)
        assert isinstance(hourly, pd.Series)

        assert 0 <= current <= 100
        assert ((hourly >= 0) & (hourly <= 100)).all()

    # The following block tests methods related to summary extraction methods.

    def _examine_summary_methods(
        self, weather: atmolib.Weather, params: dict[str, Any]
    ) -> None:
        """
        Examines the current, hourly, and daily weather summary
        extraction methods with the specified parameters.
        """

        self._verify_summary_methods(
            weather.get_current_summary(**params),
            weather.get_hourly_summary(**params),
            weather.get_daily_summary(**params),
        )

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_summary_methods_with_temperature_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Test the current, hourly, and daily weather summary
        extraction methods with different temperature units.
        """
        self._examine_summary_methods(weather, {"temperature_unit": unit})

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_summary_methods_with_precipitation_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Test the current, hourly, and daily weather summary
        extraction methods with different precipitation units.
        """
        self._examine_summary_methods(weather, {"precipitation_unit": unit})

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_summary_methods_with_wind_speed_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Test the current, hourly, and daily weather summary
        extraction methods with different wind speed units.
        """
        self._examine_summary_methods(weather, {"wind_speed_unit": unit})

    # The following block tests temperature data extraction methods.

    @pytest.mark.parametrize("altitude", constants.TEMPERATURE_ALTITUDES)
    def test_temperature_methods_with_different_altitudes(
        self, weather: atmolib.Weather, altitude: int
    ) -> None:
        """
        Tests the current and hourly temperature extraction
        methods with different altitudes levels.
        """

        current = weather.get_current_temperature(altitude=altitude)
        hourly = weather.get_hourly_temperature(altitude=altitude)

        assert isinstance(current, int | float)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_temperature_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current and hourly temperature extraction
        methods with different temperature units.
        """

        current = weather.get_current_temperature(unit=unit)
        hourly = weather.get_hourly_temperature(unit=unit)

        assert isinstance(current, int | float)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_apparent_temperature_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current and hourly apparent temperature
        extraction methods with different temperature units.
        """

        current = weather.get_current_apparent_temperature(unit=unit)
        hourly = weather.get_hourly_apparent_temperature(unit=unit)

        assert isinstance(current, int | float)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_hourly_soild_temperature_method_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the hourly soil temperature extraction
        method with different temperture units.
        """

        hourly = weather.get_hourly_soil_temperature(unit=unit)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("depth", constants.SOIL_TEMP_DEPTH)
    def test_hourly_soil_temperature_method_with_different_depths(
        self, weather: atmolib.Weather, depth: int
    ) -> None:
        """
        Tests the hourly soil temperature extraction
        method with different soil depths.
        """

        hourly = weather.get_hourly_soil_temperature(depth=depth)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_daily_temperature_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the daily temperature extraction methods
        with different temperature units.
        """

        self._verify_temperature_data_series(weather.get_daily_temperature(unit=unit))
        self._verify_temperature_data_series(
            weather.get_daily_apparent_temperature(unit=unit)
        )

    @pytest.mark.parametrize("metric", constants.DAILY_WEATHER_STATISTICAL_METRICS)
    def test_daily_temperature_methods_with_different_metrics(
        self, weather: atmolib.Weather, metric: str
    ) -> None:
        """
        Tests the daily temperature extraction methods
        with different weather statistical metrices.
        """

        self._verify_temperature_data_series(
            weather.get_daily_temperature(metric=metric)
        )
        self._verify_temperature_data_series(
            weather.get_daily_apparent_temperature(metric=metric)
        )

    # The following block tests precipitation and pressure data extraction methods.

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_precipitation_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current, hourly and daily precipitaion
        extraction methods with different temperature units.
        """

        current = weather.get_current_precipitation(unit=unit)
        hourly = weather.get_hourly_precipitation(unit=unit)
        daily = weather.get_daily_total_precipitation(unit=unit)

        assert isinstance(current, int | float)
        assert current >= 0

        self._verify_positive_data_series(hourly)
        self._verify_positive_data_series(daily)

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_rainfall_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current, hourly, and daily rainfall extraction
        methods with different temperature units.
        """

        current = weather.get_current_rainfall(unit=unit)
        hourly = weather.get_hourly_rainfall(unit=unit)
        daily = weather.get_daily_total_rainfall(unit=unit)

        assert isinstance(current, int | float)
        assert current >= 0

        self._verify_positive_data_series(hourly)
        self._verify_positive_data_series(daily)

    def test_precipitation_probability_methods(self, weather: atmolib.Weather) -> None:
        """Tests the hourly and daily precipitation probability extraction methods"""

        hourly = weather.get_hourly_precipitation_probability()
        daily = weather.get_daily_max_precipitation_probability()

        assert isinstance(hourly, pd.Series)
        assert isinstance(daily, pd.Series)

        assert all((hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100))
        assert all((daily.to_numpy() >= 0) & (daily.to_numpy() <= 100))

    @pytest.mark.parametrize("level", ("surface", "sealevel"))
    def test_atmospheric_pressure_extraction_methods(
        self, weather: atmolib.Weather, level: str
    ) -> None:
        """
        Tests the current and hourly atmospheirc pressure
        extraction methods with different measurement levels.
        """

        current = weather.get_current_pressure(level=level)
        hourly = weather.get_hourly_pressure(level=level)

        assert isinstance(current, int | float)
        assert current >= 0

        self._verify_positive_data_series(hourly)

    # The following block tests cloud coverage data extraction methods.

    @pytest.mark.parametrize("level", ("low", "mid", "high"))
    def test_cloud_cover_methods_level_parameter(
        self, weather: atmolib.Weather, level: str
    ) -> None:
        """
        Test the current and hourly cloud cover extraction
        methods with different altitude levels.
        """
        self._verify_cloud_cover_methods(
            weather.get_current_cloud_cover(level=level),
            weather.get_hourly_cloud_cover(level=level),
        )

    def test_total_cloud_cover_methods(self, weather: atmolib.Weather) -> None:
        """
        Test the current and hourly total cloud cover
        extraction methods with different altitude levels.
        """
        self._verify_cloud_cover_methods(
            weather.get_current_total_cloud_cover(),
            weather.get_hourly_total_cloud_cover(),
        )

    # The following block tests wind data extraction methods.

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_wind_speed_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current, hourly, and daily wind speed
        extraction methods with different wind speed units.
        """

        current = weather.get_current_wind_speed(unit=unit)
        hourly = weather.get_hourly_wind_speed(unit=unit)
        daily = weather.get_daily_max_wind_speed(unit=unit)

        assert isinstance(current, int | float)
        assert current >= 0

        self._verify_positive_data_series(hourly)
        self._verify_positive_data_series(daily)

    def test_wind_direction_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the current, hourly, and daily
        wind direction extraction methods.
        """

        current = weather.get_current_wind_direction()
        hourly = weather.get_hourly_wind_direction()
        daily = weather.get_daily_dominant_wind_direction()

        assert isinstance(current, int | float)
        assert current >= 0

        self._verify_positive_data_series(hourly)
        self._verify_positive_data_series(daily)

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_winds_gust_methods_with_different_units(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current, hourly, and daily wind gusts
        extraction methods with different wind speed units.
        """

        current = weather.get_current_wind_gusts(unit=unit)
        hourly = weather.get_hourly_wind_gusts(unit=unit)
        daily = weather.get_daily_max_wind_gusts(unit=unit)

        assert isinstance(current, int | float)
        assert current >= 0

        self._verify_positive_data_series(hourly)
        self._verify_positive_data_series(daily)

    # The following block tests weather code extraction methods.

    def test_current_weather_code_method(self, weather: atmolib.Weather) -> None:
        """
        Tests the `Weather.get_current_weather_code` method.
        """

        code = weather.get_current_weather_code()

        assert isinstance(code, tuple)
        assert str(code[0]) in atmolib.constants.WEATHER_CODES
        assert code[1] in atmolib.constants.WEATHER_CODES.values()

    @pytest.mark.parametrize("frequency", constants.FREQUENCIES)
    def test_periodical_weather_code_method(
        self, weather: atmolib.Weather, frequency: str
    ) -> None:
        """
        Tests the `Weather.get_periodical_weather_code` method with different `frequency` arguments.
        """

        code = weather.get_periodical_weather_code(frequency)

        # Converts the values stored in the 'data' column into strings to verify
        # them with the keys of the `atmolib.constants.WEATHER_CODES` dictionary.
        code["data"] = code["data"].astype(str)

        assert isinstance(code, pd.DataFrame)

        assert code["data"].isin(atmolib.constants.WEATHER_CODES).all()
        assert code["description"].isin(atmolib.constants.WEATHER_CODES.values()).all()

    # All other types of weather data extraction
    # methods are tested in the following block.

    def test_relative_humidity_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the current and hourly relative humidity extraction methods.
        """

        current = weather.get_current_relative_humidity()
        hourly = weather.get_hourly_relative_humidity()

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert 0 <= current <= 100 and all(
            (hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100)
        )

    @pytest.mark.parametrize("depth", (0, 2, 8, 26, 57, 81))
    def test_hourly_soil_moisture_method(
        self, weather: atmolib.Weather, depth: int
    ) -> None:
        """
        Tests the hourly soil moisture extractions methods.
        """
        moisture = weather.get_hourly_soil_moisture(depth=depth)
        assert isinstance(moisture, pd.Series) and all(moisture.to_numpy() >= 0)

    def test_daily_max_uv_index_method(self, weather: atmolib.Weather) -> None:
        """
        Tests the `atmolib.get_daily_max_uv_index` method.
        """
        daily = weather.get_daily_max_uv_index()
        assert isinstance(daily, pd.Series) and all(daily.to_numpy() >= 0)

    def test_is_day_or_night_method(self, weather: atmolib.Weather) -> None:
        """
        Tests the `atmolib.is_day_or_night` method.
        """
        is_day_or_night = weather.is_day_or_night()
        assert is_day_or_night in (1, 0)

    def test_visibility_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the current and hourly visibility extraction methods.
        """

        current = weather.get_current_visibility()
        hourly = weather.get_hourly_visibility()

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert current >= 0 and all(hourly.to_numpy() >= 0)

    def test_daylight_and_sunlight_duration_methods(
        self, weather: atmolib.Weather
    ) -> None:
        """
        Tests the `Weather.get_daily_daylight_duration` and
        `Weather.get_sunshine_duration` methods.
        """

        daylight = weather.get_daily_daylight_duration()
        sunshine = weather.get_daily_sunshine_duration()

        assert isinstance(daylight, pd.Series) and isinstance(sunshine, pd.Series)
        assert all(
            (daylight.to_numpy() >= 0) & (daylight.to_numpy() <= 86_400)
        ) and all((sunshine.to_numpy() >= 0) & (sunshine.to_numpy() <= 86_400))

    def test_sunrise_and_sunset_time_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the `Weather.get_daily_sunrise_time` and
        `Weather.get_daily_sunset_time` methods.
        """

        sunrise = weather.get_daily_sunrise_time()
        sunset = weather.get_daily_sunset_time()

        datetime_format = r"%Y-%m-%dT%H:%M"

        assert isinstance(sunrise, pd.Series) and isinstance(sunset, pd.Series)

        # Maps the `sunrise` and `sunset` Series to verify
        # the datetime format of the resultant Series.
        sunrise.map(lambda x: datetime.strptime(x, datetime_format))
        sunset.map(lambda x: datetime.strptime(x, datetime_format))
