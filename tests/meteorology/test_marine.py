r"""
Tests the objects and methods defined within `pyweather/meteorology/marine.py` file.
"""

import pytest
import pandas as pd

import pyweather


class TestMarineWeather:
    r"""
    Tests the `pyweather.MarineWeather` class and its defined methods.
    """

    def test_object_initialization(
        self, valid_marine_coordinates: tuple[tuple[int, int]]
    ) -> None:
        r"""
        Test the `pyweather.MarineWeather` object initialization with valid parameters.
        """

        for i in valid_marine_coordinates:
            pyweather.MarineWeather(*i)

        # Tests the initialization with different `wave_type` and `forecast_days` arguments.
        for type_, days in zip(("composite", "wind", "swell"), (1, 5, 8)):
            pyweather.MarineWeather(0, 0, wave_type=type_, forecast_days=days)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_marine_coordinates: tuple[tuple[int, int]]
    ) -> None:
        r"""
        Tests the `pyweather.MarineWeather` object initialization with invalid parameters.
        """

        with pytest.raises(pyweather.errors.RequestError):

            # Expects a RequestError upon initialization with invalid coordinates.
            for i in invalid_marine_coordinates:
                pyweather.MarineWeather(*i)

        with pytest.raises(AssertionError):

            # Expects a ValueError upon initialization with invalid `wave_type` argument.
            for i in (0, -1, 9):
                pyweather.MarineWeather(0, 0, forecast_days=i)

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_marine_weather_summary_extraction_methods(self, wave_type: str) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = pyweather.MarineWeather(0, 0, wave_type=wave_type)

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
            == pyweather.constants.MARINE_WEATHER_SUMMARY_DATA_TYPES
        )

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_current_marine_weather_extraction_methods(self, wave_type: str) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = pyweather.MarineWeather(0, 0, wave_type=wave_type)

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
    def test_hourly_marine_weather_extraction_methods(self, wave_type: str) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = pyweather.MarineWeather(0, 0, wave_type=wave_type)

        height = marine_weather.get_hourly_wave_height()
        direction = marine_weather.get_hourly_wave_direction()
        period = marine_weather.get_hourly_wave_period()

        assert (
            isinstance(height, pd.Series)
            and isinstance(direction, pd.Series)
            and isinstance(period, pd.Series)
        )
        assert (
            all(height >= 0)
            and all((direction >= 0) & (direction < 360))
            and all(period >= 0)
        )

    @pytest.mark.parametrize("wave_type", ("composite", "wind", "swell"))
    def test_daily_marine_weather_extraction_methods(self, wave_type: str) -> None:
        r"""
        Test the marine weather summary extraction methods.
        """

        marine_weather = pyweather.MarineWeather(0, 0, wave_type=wave_type)

        height = marine_weather.get_daily_max_wave_height()
        direction = marine_weather.get_daily_dominant_wave_direction()
        period = marine_weather.get_daily_max_wave_period()

        assert (
            isinstance(height, pd.Series)
            and isinstance(direction, pd.Series)
            and isinstance(period, pd.Series)
        )
        assert (
            all(height >= 0)
            and all((direction >= 0) & (direction < 360))
            and all(period >= 0)
        )
