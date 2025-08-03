"""
Tests the classes and methods defined within
atmolib/meteorology/weather.py.
"""

from datetime import datetime
from typing import Any

import pytest
import pandas as pd

from .. import utils
from atmolib import Weather, constants


class TestWeather:
    """Tests the 'Weather' class."""

    def test_init_with_valid_coordinates(
        self, valid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """Tests object initialization with valid coordinates."""

        for lat, long in valid_coordinates:
            Weather(lat, long)

    def test_init_with_valid_forecast_days(self) -> None:
        """Tests object initialization with valid forecast days."""

        for days in (1, 10, 16):
            Weather(0, 0, days)

    def test_init_with_invalid_coordinates(
        self, invalid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """Tests object initialization with invalid coordinates."""

        with pytest.raises(ValueError):
            for lat, long in invalid_coordinates:
                Weather(lat, long)

    def test_init_with_invalid_forecast_days(self) -> None:
        """Tests object initialization with invalid forecast days."""

        with pytest.raises(ValueError):
            for days in (0, -1, 17):
                Weather(0, 0, days)

    # The following block comprises test verification methods.

    @staticmethod
    def _verify_summary_methods(weather: Weather, params: dict[str, Any]) -> None:
        """
        Verifies the summary extraction methods with the specified parameters.
        """

        current = weather.get_current_summary(**params)
        daily = weather.get_daily_summary(**params)
        hourly = weather.get_hourly_summary(**params)

        assert isinstance(current, pd.Series)
        assert isinstance(hourly, pd.DataFrame)
        assert isinstance(daily, pd.DataFrame)

        assert current.index.tolist() == constants.CURRENT_WEATHER_SUMMARY_LABELS
        assert hourly.columns.tolist() == constants.HOURLY_WEATHER_SUMMARY_LABELS
        assert daily.columns.tolist() == constants.DAILY_WEATHER_SUMMARY_LABELS

    # The following block tests summary data extraction methods.

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_summary_methods_with_temperature_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Test the weather summary extraction methods
        with different temperature units.
        """
        self._verify_summary_methods(weather, {"temperature_unit": unit})

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_summary_methods_with_precipitation_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Test the weather summary extraction methods
        with different precipitation units.
        """
        self._verify_summary_methods(weather, {"precipitation_unit": unit})

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_summary_methods_with_wind_speed_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Test the weather summary extraction methods
        with different wind speed units.
        """
        self._verify_summary_methods(weather, {"wind_speed_unit": unit})

    # The following block tests temperature data extraction methods.

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_temperature_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the temperature extraction methods
        with different temperature units.
        """

        current = weather.get_current_temperature(unit=unit)
        daily = weather.get_daily_temperature(unit=unit)
        hourly = weather.get_hourly_temperature(unit=unit)

        assert isinstance(current, int | float)

        utils.verify_temperature_data_series(daily)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("altitude", constants.TEMPERATURE_ALTITUDES)
    def test_temperature_methods_with_different_altitudes(
        self, weather: Weather, altitude: int
    ) -> None:
        """
        Tests the temperature extraction methods
        with different altitudes levels.
        """

        current = weather.get_current_temperature(altitude=altitude)
        hourly = weather.get_hourly_temperature(altitude=altitude)

        assert isinstance(current, int | float)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_apparent_temperature_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the apparent temperature extraction
        methods with different temperature units.
        """

        current = weather.get_current_apparent_temperature(unit=unit)
        daily = weather.get_daily_apparent_temperature(unit=unit)
        hourly = weather.get_hourly_apparent_temperature(unit=unit)

        assert isinstance(current, int | float)

        utils.verify_temperature_data_series(daily)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("metric", constants.DAILY_WEATHER_STATISTICAL_METRICS)
    def test_daily_temperature_methods_with_different_metrics(
        self, weather: Weather, metric: str
    ) -> None:
        """
        Tests the daily temperature extraction methods
        with different weather statistical metrics.
        """

        temp = weather.get_daily_temperature(metric=metric)
        apparent_temp = weather.get_daily_apparent_temperature(metric=metric)

        utils.verify_temperature_data_series(temp)
        utils.verify_temperature_data_series(apparent_temp)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_soil_temperature_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the soil temperature extraction
        methods with different temperature units.
        """

        hourly = weather.get_hourly_soil_temperature(unit=unit)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("depth", constants.SOIL_TEMP_DEPTH)
    def test_soil_temperature_methods_with_different_depths(
        self, weather: Weather, depth: int
    ) -> None:
        """
        Tests the soil temperature extraction
        methods with different soil depths.
        """

        hourly = weather.get_hourly_soil_temperature(depth=depth)
        utils.verify_temperature_data_series(hourly)

    # The following block tests precipitation data extraction methods.

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_precipitation_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the precipitation extraction methods with different temperature units.
        """

        current = weather.get_current_precipitation(unit=unit)
        hourly = weather.get_hourly_precipitation(unit=unit)
        daily = weather.get_daily_total_precipitation(unit=unit)

        assert current >= 0

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_rainfall_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the rainfall extraction methods with different temperature units.
        """

        current = weather.get_current_rainfall(unit=unit)
        hourly = weather.get_hourly_rainfall(unit=unit)
        daily = weather.get_daily_total_rainfall(unit=unit)

        assert current >= 0

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    def test_precipitation_probability_methods(self, weather: Weather) -> None:
        """Tests the precipitation probability extraction methods"""

        hourly = weather.get_hourly_precipitation_probability()
        daily = weather.get_daily_max_precipitation_probability()

        utils.verify_positive_range_data_series(hourly, 100)
        utils.verify_positive_range_data_series(daily, 100)

    # The following block tests cloud coverage data extraction methods.

    @pytest.mark.parametrize("level", constants.CLOUD_COVER_LEVELS)
    def test_cloud_cover_methods_level_parameter(
        self, weather: Weather, level: str
    ) -> None:
        """
        Test the cloud cover extraction methods with different altitude levels.
        """

        current = weather.get_current_cloud_cover(level=level)
        hourly = weather.get_hourly_cloud_cover(level=level)

        assert 0 <= current <= 100
        utils.verify_positive_range_data_series(hourly, 100)

    def test_total_cloud_cover_methods(self, weather: Weather) -> None:
        """
        Test the total cloud cover extraction
        methods with different altitude levels.
        """

        current = weather.get_current_total_cloud_cover()
        hourly = weather.get_hourly_total_cloud_cover()

        assert 0 <= current <= 100
        utils.verify_positive_range_data_series(hourly, 100)

    # The following block tests wind data extraction methods.

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_wind_speed_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the wind speed extraction methods with different wind speed units.
        """

        current = weather.get_current_wind_speed(unit=unit)
        hourly = weather.get_hourly_wind_speed(unit=unit)
        daily = weather.get_daily_max_wind_speed(unit=unit)

        assert current >= 0

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    def test_wind_direction_methods(self, weather: Weather) -> None:
        """Tests wind direction extraction methods."""

        current = weather.get_current_wind_direction()
        hourly = weather.get_hourly_wind_direction()
        daily = weather.get_daily_dominant_wind_direction()

        assert current >= 0

        utils.verify_positive_range_data_series(hourly, 360)
        utils.verify_positive_range_data_series(daily, 360)

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_winds_gust_methods_with_different_units(
        self, weather: Weather, unit: str
    ) -> None:
        """
        Tests the wind gusts extraction methods with different wind speed units.
        """

        current = weather.get_current_wind_gusts(unit=unit)
        hourly = weather.get_hourly_wind_gusts(unit=unit)
        daily = weather.get_daily_max_wind_gusts(unit=unit)

        assert current >= 0

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    # The following block tests weather code extraction methods.

    def test_current_weather_code_method(self, weather: Weather) -> None:
        """Tests the current weather code extraction method."""

        code = weather.get_current_weather_code()

        assert isinstance(code, tuple)
        assert str(code[0]) in constants.WEATHER_CODES
        assert code[1] in constants.WEATHER_CODES.values()

    @pytest.mark.parametrize("frequency", constants.FREQUENCIES)
    def test_periodical_weather_code_method(
        self, weather: Weather, frequency: str
    ) -> None:
        """Tests the periodical weather code extraction method."""

        code = weather.get_periodical_weather_code(frequency)

        # Converts the values stored in the 'data' column into strings to verify
        # them with the keys of the `atmolib.constants.WEATHER_CODES` dictionary.
        code["data"] = code["data"].astype(str)

        assert isinstance(code, pd.DataFrame)

        assert code["data"].isin(constants.WEATHER_CODES).all()
        assert code["description"].isin(constants.WEATHER_CODES.values()).all()

    # All other types of weather data extraction
    # methods are tested in the following block.

    @pytest.mark.parametrize("level", constants.PRESSURE_LEVELS)
    def test_atmospheric_pressure_extraction_methods(
        self, weather: Weather, level: str
    ) -> None:
        """
        Tests the atmospheric pressure extraction
        methods with different measurement levels.
        """

        current = weather.get_current_pressure(level=level)
        hourly = weather.get_hourly_pressure(level=level)

        assert current >= 0
        utils.verify_positive_data_series(hourly)

    def test_relative_humidity_methods(self, weather: Weather) -> None:
        """Tests the relative humidity extraction methods."""

        current = weather.get_current_relative_humidity()
        hourly = weather.get_hourly_relative_humidity()

        assert 0 <= current <= 100
        utils.verify_positive_range_data_series(hourly, 100)

    @pytest.mark.parametrize("depth", (0, 10, 18, 78, 81))
    def test_soil_moisture_methods(self, weather: Weather, depth: int) -> None:
        """Tests the soil moisture extraction methods."""

        moisture = weather.get_hourly_soil_moisture(depth=depth)
        utils.verify_positive_data_series(moisture)

    def test_daily_max_uv_index_method(self, weather: Weather) -> None:
        """Tests the `Weather.get_daily_max_uv_index` method."""

        uv = weather.get_daily_max_uv_index()
        utils.verify_positive_data_series(uv)

    def test_is_day_or_night_method(self, weather: Weather) -> None:
        """Test the `Weather.is_day_or_night` method."""

        is_day_or_night = weather.is_day_or_night()
        assert is_day_or_night in (1, 0)

    def test_visibility_methods(self, weather: Weather) -> None:
        """Tests the visibility extraction methods."""

        current = weather.get_current_visibility()
        hourly = weather.get_hourly_visibility()

        assert isinstance(current, int | float)
        assert current >= 0

        utils.verify_positive_data_series(hourly)

    def test_daylight_and_sunlight_duration_methods(self, weather: Weather) -> None:
        """Test the daily daylight and sunshine duration extraction methods."""

        daylight = weather.get_daily_daylight_duration()
        sunshine = weather.get_daily_sunshine_duration()

        utils.verify_positive_range_data_series(daylight, 86_400)
        utils.verify_positive_range_data_series(sunshine, 86_400)

    def test_sunrise_and_sunset_time_methods(self, weather: Weather) -> None:
        """Tests the daily sunrise and sunset time extraction methods."""

        sunrise = weather.get_daily_sunrise_time()
        sunset = weather.get_daily_sunset_time()

        datetime_format = r"%Y-%m-%dT%H:%M"

        assert isinstance(sunrise, pd.Series)
        assert isinstance(sunset, pd.Series)

        # Iterates through the pandas Series objects and
        # verifies the datetime format at each iteration.
        for time in pd.concat([sunrise, sunset], ignore_index=True):
            datetime.strptime(time, datetime_format)
