r"""
Tests the objects and methods defined within `atmolib/meteorology/marine.py` file.
"""

import pytest
import pandas as pd

import atmolib


class TestMarineWeather:
    r"""
    Tests the `atmolib.MarineWeather` class and its defined methods.
    """

    def test_object_initialization(
        self, valid_marine_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        r"""
        Test the `atmolib.MarineWeather` object initialization with valid parameters.
        """

        for i in valid_marine_coordinates:
            atmolib.MarineWeather(*i)

    @pytest.mark.parametrize("type_", ("composite", "wind", "swell"))
    def test_object_intialization_wave_type_parameter(
        self, type_: atmolib.constants.WAVE_TYPES
    ) -> None:
        r"""
        Tests the `atmolib.MarineWeather` object initialization
        with different `wave_type` arguments.
        """
        atmolib.MarineWeather(0, 0, wave_type=type_)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_marine_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        r"""
        Tests the `atmolib.MarineWeather` object initialization with invalid parameters.
        """

        with pytest.raises(atmolib.errors.RequestError):

            # Expects a RequestError upon initialization with invalid coordinates.
            for i in invalid_marine_coordinates:
                atmolib.MarineWeather(*i)

        with pytest.raises(AssertionError):

            # Expects a ValueError upon initialization with invalid `wave_type` argument.
            for days in (0, -1, 9):
                atmolib.MarineWeather(0, 0, forecast_days=days)

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_marine_weather_summary_methods(
        self, wave_type: atmolib.constants.WAVE_TYPES
    ) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = atmolib.MarineWeather(
            0, 0, wave_type=wave_type, forecast_days=2
        )

        current = marine_weather.get_current_summary()
        hourly = marine_weather.get_hourly_summary()
        daily = marine_weather.get_daily_summary()

        assert (
            isinstance(current, pd.Series)
            and isinstance(hourly, pd.DataFrame)
            and isinstance(daily, pd.DataFrame)
        )

        # Verifies the index/columns of the resultant pandas.Series/DataFrame.
        assert (
            current.index.tolist()
            == hourly.columns.tolist()
            == daily.columns.tolist()
            == atmolib.constants.MARINE_WEATHER_SUMMARY_DATA_TYPES
        )

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_current_marine_weather_methods(
        self, wave_type: atmolib.constants.WAVE_TYPES
    ) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = atmolib.MarineWeather(
            0, 0, wave_type=wave_type, forecast_days=2
        )

        height = marine_weather.get_current_wave_height()
        direction = marine_weather.get_current_wave_direction()
        period = marine_weather.get_current_wave_period()

        assert (
            isinstance(height, int | float)
            and isinstance(direction, int | float)
            and isinstance(period, int | float)
        )
        assert height >= 0 and direction in range(360) and period >= 0

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_hourly_marine_weather_methods(
        self, wave_type: atmolib.constants.WAVE_TYPES
    ) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = atmolib.MarineWeather(
            0, 0, wave_type=wave_type, forecast_days=2
        )

        height = marine_weather.get_hourly_wave_height()
        direction = marine_weather.get_hourly_wave_direction()
        period = marine_weather.get_hourly_wave_period()

        assert (
            isinstance(height, pd.Series)
            and isinstance(direction, pd.Series)
            and isinstance(period, pd.Series)
        )
        assert (
            all(height.to_numpy() >= 0)
            and all((direction.to_numpy() >= 0) & (direction.to_numpy() < 360))
            and all(period.to_numpy() >= 0)
        )

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_daily_marine_weather_methods(
        self, wave_type: atmolib.constants.WAVE_TYPES
    ) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = atmolib.MarineWeather(
            0, 0, wave_type=wave_type, forecast_days=2
        )

        height = marine_weather.get_daily_max_wave_height()
        direction = marine_weather.get_daily_dominant_wave_direction()
        period = marine_weather.get_daily_max_wave_period()

        assert (
            isinstance(height, pd.Series)
            and isinstance(direction, pd.Series)
            and isinstance(period, pd.Series)
        )
        assert (
            all(height.to_numpy() >= 0)
            and all((direction.to_numpy() >= 0) & (direction.to_numpy() < 360))
            and all(period.to_numpy() >= 0)
        )
