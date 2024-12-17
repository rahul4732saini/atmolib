"""
Tests the classes and methods defined
within atmolib/meteorology/marine.py.
"""

import pytest
import pandas as pd

from .. import utils
from atmolib import MarineWeather, constants


class TestMarineWeather:
    """
    Tests the `MarineWeather` class and its defined methods.
    """

    def test_object_initialization_with_valid_coordinates(
        self, valid_marine_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """Test the object initialization with valid coordinates."""

        for lat, long in valid_marine_coordinates:
            MarineWeather(lat, long)

    def test_object_initialization_with_valid_forecast_days(self) -> None:
        """Test the object initialization with valid forecast days."""

        for days in (1, 4, 8):
            MarineWeather(0, 0, forecast_days=days)

    def test_object_initialization_with_invalid_forecast_days(self) -> None:
        """Tests the object initialization with invalid forecast days."""

        with pytest.raises(ValueError):
            for days in (0, -1, 9):
                MarineWeather(0, 0, forecast_days=days)

    def test_object_initialization_wave_type_parameter(self) -> None:
        """Tests the object initialization with different wave types."""

        for type_ in constants.WAVE_TYPES:
            MarineWeather(0, 0, type_)

    @pytest.mark.parametrize("wave_type", constants.WAVE_TYPES)
    def test_marine_weather_summary_methods(self, wave_type: str) -> None:
        """Test the marine weather summary extraction methods."""

        marine_weather = MarineWeather(0, 0, wave_type, forecast_days=2)

        current = marine_weather.get_current_summary()
        daily = marine_weather.get_daily_summary()
        hourly = marine_weather.get_hourly_summary()

        assert isinstance(current, pd.Series)
        assert isinstance(hourly, pd.DataFrame)
        assert isinstance(daily, pd.DataFrame)

        # Verifies the indices and columns of the resultant
        # pandas Series and DataFrame objects.
        assert current.index.tolist() == constants.MARINE_WEATHER_SUMMARY_PARAMS
        assert hourly.columns.tolist() == constants.MARINE_WEATHER_SUMMARY_PARAMS
        assert daily.columns.tolist() == constants.MARINE_WEATHER_SUMMARY_PARAMS

    @pytest.mark.parametrize("wave_type", constants.WAVE_TYPES)
    def test_wave_height_methods(self, wave_type: str) -> None:
        """Tests the wave height extraction methods."""

        marine = MarineWeather(0, 0, wave_type, forecast_days=2)

        current = marine.get_current_wave_height()
        hourly = marine.get_hourly_wave_height()
        daily = marine.get_daily_max_wave_height()

        assert current is None or current >= 0
        utils.verify_positive_or_null_data_series(hourly)
        utils.verify_positive_or_null_data_series(daily)

    @pytest.mark.parametrize("wave_type", constants.WAVE_TYPES)
    def test_wave_direction_methods(self, wave_type: str) -> None:
        """Tests the wave direction extraction methods."""

        marine = MarineWeather(0, 0, wave_type, forecast_days=2)

        current = marine.get_current_wave_direction()
        hourly = marine.get_hourly_wave_direction()
        daily = marine.get_daily_dominant_wave_direction()

        assert current is None or current >= 0
        utils.verify_positive_or_null_data_series(hourly)
        utils.verify_positive_or_null_data_series(daily)

    @pytest.mark.parametrize("wave_type", constants.WAVE_TYPES)
    def test_wave_period_methods(self, wave_type: str) -> None:
        """Tests the wave period extraction methods."""

        marine = MarineWeather(0, 0, wave_type, forecast_days=2)

        current = marine.get_current_wave_period()
        hourly = marine.get_hourly_wave_period()
        daily = marine.get_daily_max_wave_period()

        assert current is None or current >= 0
        utils.verify_positive_or_null_data_series(hourly)
        utils.verify_positive_or_null_data_series(daily)
