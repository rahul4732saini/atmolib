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
    def _verify_cloud_cover_methods(current: int | float, hourly: pd.Series) -> None:
        """
        Verifies the cloud cover extraction methods.
        """

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert 0 <= current <= 100 and all(
            (hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100)
        )

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

    # The following block tests methods related to temperature extraction methods.

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

    # The following block tests precipitation extraction related methods.

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_current_precipitation_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current precipitation extraction
        methods with different `unit` arguments.
        """

        precipitation = weather.get_current_precipitation(unit=unit)
        rainfall = weather.get_current_rainfall(unit=unit)

        assert isinstance(precipitation, int | float) and isinstance(
            rainfall, int | float
        )
        assert precipitation >= 0 and rainfall >= 0

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_periodical_precipitation_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the hourly and daily precipitation extraction
        methods with different `unit` arguments.
        """

        hourly_precipitation = weather.get_hourly_precipitation(unit=unit)
        hourly_rainfall = weather.get_hourly_rainfall(unit=unit)

        daily_precipitation = weather.get_daily_total_precipitation(unit=unit)
        daily_rainfall = weather.get_daily_total_rainfall(unit=unit)

        # Tests the hourly precipitation methods.
        assert isinstance(hourly_precipitation, pd.Series) and isinstance(
            hourly_rainfall, pd.Series
        )
        assert all(hourly_precipitation.to_numpy() >= 0) and all(
            hourly_rainfall.to_numpy() >= 0
        )

        # Tests the daily precipitation methods.
        assert isinstance(daily_precipitation, pd.Series) and isinstance(
            daily_rainfall, pd.Series
        )
        assert all(daily_precipitation.to_numpy() >= 0) and all(
            daily_rainfall.to_numpy() >= 0
        )

    def test_precipitation_probability_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the precipitation probability extraction methods.
        """

        hourly = weather.get_hourly_precipitation_probability()
        daily = weather.get_daily_max_precipitation_probability()

        assert isinstance(hourly, pd.Series) and isinstance(daily, pd.Series)
        assert all((hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100)) and all(
            (daily.to_numpy() >= 0) & (daily.to_numpy() <= 100)
        )

    @pytest.mark.parametrize("level", ("surface", "sealevel"))
    def test_atmospheric_pressure_extraction_methods(
        self, weather: atmolib.Weather, level: str
    ) -> None:
        """
        Tests the current and hourly atmospheric pressure
        extraction methods with different `level` arguments.
        """

        current = weather.get_current_pressure(level=level)
        hourly = weather.get_hourly_pressure(level=level)

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert current >= 0 and all(hourly.to_numpy() >= 0)

    # The following block tests cloud coverage extraction related methods.

    @pytest.mark.parametrize("level", ("low", "mid", "high"))
    def test_cloud_cover_methods_level_parameter(
        self, weather: atmolib.Weather, level: str
    ) -> None:
        """
        Tests the current and hourly cloud cover extraction
        methods with different `level` arguments.
        """
        self._verify_cloud_cover_methods(
            weather.get_current_cloud_cover(level=level),
            weather.get_hourly_cloud_cover(level=level),
        )

    def test_total_cloud_cover_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the current and hourly total cloud cover extraction methods.
        """
        self._verify_cloud_cover_methods(
            weather.get_current_total_cloud_cover(),
            weather.get_hourly_total_cloud_cover(),
        )

    # The following block tests wind related extraction methods.

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_current_wind_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the current wind speed/gusts extraction
        methods with different `unit` arguments.
        """

        speed = weather.get_current_wind_speed(unit=unit)
        gusts = weather.get_current_wind_gusts(unit=unit)

        assert isinstance(speed, int | float) and isinstance(gusts, int | float)
        assert speed >= 0 and gusts >= 0

    @pytest.mark.parametrize("altitude", (10, 80, 120, 180))
    def test_current_wind_methods_altitude_parameter(
        self, weather: atmolib.Weather, altitude: int
    ) -> None:
        """
        Test the current wind related extraction
        methods with different `altitude` parameters.
        """

        speed = weather.get_current_wind_speed(altitude=altitude)
        direction = weather.get_current_wind_direction(altitude=altitude)
        gusts = weather.get_current_wind_gusts(altitude=altitude)

        assert (
            isinstance(speed, int | float)
            and isinstance(direction, int | float)
            and isinstance(gusts, int | float)
        )

        assert speed >= 0 and 0 <= direction <= 360 and gusts >= 0

    @pytest.mark.parametrize("altitude", (10, 80, 120, 180))
    def test_hourly_wind_methods_altitude_parameter(
        self, weather: atmolib.Weather, altitude: int
    ) -> None:
        """
        Tests the hourly wind related extraction
        methods with different `altitude` arguments.
        """

        speed = weather.get_hourly_wind_speed(altitude=altitude)
        direction = weather.get_hourly_wind_direction(altitude=altitude)

        assert isinstance(speed, pd.Series) and isinstance(direction, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(
            (direction.to_numpy() >= 0) & (direction.to_numpy() <= 360)
        )

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_hourly_wind_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the hourly wind related extraction
        methods with different `unit` arguments.
        """

        speed = weather.get_hourly_wind_speed(unit=unit)
        gusts = weather.get_hourly_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_daily_wind_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        """
        Tests the daily wind related extraction
        methods with different `unit` arguments.
        """

        speed = weather.get_daily_max_wind_speed(unit=unit)
        gusts = weather.get_daily_max_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    # The following block tests weather code extraction methods.

    def test_current_weather_code_method(self, weather: atmolib.Weather) -> None:
        """
        Tests the `Weather.get_current_weather_code` method.
        """

        code = weather.get_current_weather_code()

        assert isinstance(code, tuple)
        assert str(code[0]) in atmolib.constants.WEATHER_CODES
        assert code[1] in atmolib.constants.WEATHER_CODES.values()

    @pytest.mark.parametrize("frequency", ("hourly", "daily"))
    def test_periodical_weather_code_method(
        self, weather: atmolib.Weather, frequency: str
    ) -> None:
        """
        Tests the `Weather.get_periodical_weather_code` method with different `frequency` arguments.
        """

        code = weather.get_periodical_weather_code(frequency)

        # Converting integers into strings in the `data` column to be used for
        # verification with the `atmolib.constants.WEATHER_CODES` dictionary.
        code["data"] = code["data"].astype(np.object_)
        code["data"] = code["data"].map(lambda x: str(x))

        assert isinstance(code, pd.DataFrame)
        assert code["data"].isin(atmolib.constants.WEATHER_CODES.keys()).all()
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
