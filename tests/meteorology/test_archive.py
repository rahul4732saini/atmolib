"""
Tests the classes and methods defined
within `atmolib/meteorology/archive.py`.
"""

from datetime import datetime
from typing import Any

import pytest
import pandas as pd

from .. import utils
from atmolib import WeatherArchive, constants


class TestWeatherArchive:
    """
    Tests the `WeatherArchive` class and its defined methods.
    """

    def test_object_initialization(
        self,
        valid_coordinates: tuple[tuple[float, float], ...],
        valid_archive_dates: tuple[tuple[str, str], ...],
    ) -> None:
        """
        Test the `WeatherArchive` object initialization with valid parameters.
        """

        for lat, long in valid_coordinates:
            WeatherArchive(lat, long, start_date="2020-01-01", end_date="2020-01-10")

        for start, end in valid_archive_dates:
            WeatherArchive(0, 0, start, end)

    def test_object_initialization_with_invalid_parameters(
        self,
        invalid_coordinates: tuple[tuple[float, float], ...],
        invalid_archive_dates: tuple[tuple[str, str], ...],
    ) -> None:
        """
        Tests the `WeatherArchive` object initialization with invalid parameters.
        """

        with pytest.raises(ValueError):

            # Expects a ValueError upon initialization with invalid coordinates.
            for lat, long in invalid_coordinates:
                WeatherArchive(
                    lat, long, start_date="2020-01-01", end_date="2020-01-10"
                )

            # Expects a ValueError upon initialization with
            # invalid start and end date for the archive data.
            for start, end in invalid_archive_dates:
                WeatherArchive(0, 0, start, end)

    # The following block comprises test verification methods.

    @staticmethod
    def _verify_summary_methods(
        archive: WeatherArchive, params: dict[str, Any]
    ) -> None:
        """Verifies the summary extraction methods."""

        hourly = archive.get_hourly_summary(**params)
        daily = archive.get_daily_summary(**params)

        assert isinstance(hourly, pd.DataFrame)
        assert isinstance(daily, pd.DataFrame)

        assert hourly.columns.tolist() == constants.HOURLY_ARCHIVE_SUMMARY_LABELS
        assert daily.columns.tolist() == constants.DAILY_ARCHIVE_SUMMARY_LABELS

    # The following block tests summary data extraction methods.

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_summary_methods_with_different_temperature_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the summary extraction methods
        with different temperature units.
        """
        self._verify_summary_methods(archive, {"temperature_unit": unit})

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_summary_methods_with_different_precipitation_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the summary extraction methods
        with different precipitation units.
        """
        self._verify_summary_methods(archive, {"precipitation_unit": unit})

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_summary_methods_with_different_wind_speed_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the summary extraction methods
        with different wind speed units.
        """
        self._verify_summary_methods(archive, {"wind_speed_unit": unit})

    # The following block tests temperature data extraction methods.

    @pytest.mark.parametrize("altitude", constants.TEMPERATURE_ALTITUDES)
    def test_temperature_methods_with_different_altitudes(
        self, archive: WeatherArchive, altitude: int
    ) -> None:
        """
        Tests the temperature data extraction
        methods with different attitude levels.
        """

        hourly = archive.get_hourly_temperature(altitude=altitude)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_temperature_methods_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the temperature extraction methods
        with different temperature units.
        """

        hourly = archive.get_hourly_temperature(unit=unit)
        daily = archive.get_daily_temperature(unit=unit)

        utils.verify_temperature_data_series(hourly)
        utils.verify_temperature_data_series(daily)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_apparent_temperature_methods_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the apparent temperature extraction
        methods with different temperature units.
        """

        hourly = archive.get_hourly_apparent_temperature(unit=unit)
        daily = archive.get_daily_apparent_temperature(unit=unit)

        utils.verify_temperature_data_series(hourly)
        utils.verify_temperature_data_series(daily)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_soil_temperature_method_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the soil temperature extraction
        methods with different temperature units.
        """

        hourly = archive.get_hourly_soil_temperature(unit=unit)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("depth", (0, 18, 255, 157))
    def test_soil_temperature_methods_with_different_depth(
        self, archive: WeatherArchive, depth: int
    ) -> None:
        """
        Tests the soil temperature extraction
        methods with different soil depths.
        """

        hourly = archive.get_hourly_soil_temperature(depth=depth)
        utils.verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("metric", constants.DAILY_WEATHER_STATISTICAL_METRICS)
    def test_daily_temperature_methods_with_different_metrics(
        self, archive: WeatherArchive, metric: str
    ) -> None:
        """
        Tests the daily temperature and apparent temperature extraction
        methods with different weather statistical metrics.
        """

        temp = archive.get_daily_temperature(metric=metric)
        apparent_temp = archive.get_daily_apparent_temperature(metric=metric)

        utils.verify_temperature_data_series(temp)
        utils.verify_temperature_data_series(apparent_temp)

    # The following block tests precipitation data extraction methods.

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_precipitation_methods_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the precipitation extraction methods
        with different precipitation units.
        """

        hourly = archive.get_hourly_precipitation(unit=unit)
        daily = archive.get_daily_total_precipitation(unit=unit)

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_rainfall_methods_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the rainfall extraction methods
        with different precipitation units.
        """

        hourly = archive.get_hourly_rainfall(unit=unit)
        daily = archive.get_daily_total_rainfall(unit=unit)

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    # The following block tests cloud coverage extraction methods.

    @pytest.mark.parametrize("level", constants.CLOUD_COVER_LEVELS)
    def test_cloud_cover_methods_with_different_levels(
        self, archive: WeatherArchive, level: str
    ) -> None:
        """
        Tests the cloud coverage extraction
        methods with different altitude levels.
        """

        hourly = archive.get_hourly_cloud_cover(level=level)
        utils.verify_positive_range_data_series(hourly, 100)

    # The following block tests wind related data extraction methods.

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_wind_speed_methods_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the wind speed extraction methods
        with different wind speed units.
        """

        hourly = archive.get_hourly_wind_speed(unit=unit)
        daily = archive.get_daily_max_wind_speed(unit=unit)

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    @pytest.mark.parametrize("altitude", constants.ARCHIVE_WIND_ALTITUDES)
    def test_wind_speed_methods_with_different_altitudes(
        self, archive: WeatherArchive, altitude: int
    ) -> None:
        """
        Tests the wind speed extraction methods
        with different altitude levels.
        """

        hourly = archive.get_hourly_wind_speed(altitude=altitude)
        daily = archive.get_daily_max_wind_speed()

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_wind_gusts_methods_with_different_units(
        self, archive: WeatherArchive, unit: str
    ) -> None:
        """
        Tests the wind gusts extraction methods
        with different wind speed units.
        """

        hourly = archive.get_hourly_wind_speed(unit=unit)
        daily = archive.get_daily_max_wind_speed(unit=unit)

        utils.verify_positive_data_series(hourly)
        utils.verify_positive_data_series(daily)

    @pytest.mark.parametrize("altitude", constants.ARCHIVE_WIND_ALTITUDES)
    def test_wind_direction_methods_with_different_altitudes(
        self, archive: WeatherArchive, altitude: int
    ) -> None:
        """
        Tests the wind direction extraction methods
        with different altitude levels.
        """

        hourly = archive.get_hourly_wind_direction(altitude=altitude)
        daily = archive.get_daily_dominant_wind_direction()

        utils.verify_positive_range_data_series(hourly, 360)
        utils.verify_positive_range_data_series(daily, 360)

    # The following block tests weather code extraction methods.

    @pytest.mark.parametrize("frequency", constants.FREQUENCIES)
    def test_periodical_weather_code_method(
        self, archive: WeatherArchive, frequency: str
    ) -> None:
        """
        Tests the periodical weather code extraction
        method with different data frequencies.
        """

        code = archive.get_periodical_weather_code(frequency)

        # Converts the values stored in the 'data' column into strings to verify
        # them with the keys of the `atmolib.constants.WEATHER_CODES` dictionary.
        code["data"] = code["data"].astype(str)

        assert isinstance(code, pd.DataFrame)

        assert code["data"].isin(constants.WEATHER_CODES).all()
        assert code["description"].isin(constants.WEATHER_CODES.values()).all()

    # All other types of weather data extraction
    # methods are tested in the following block.

    def test_relative_humidity_methods(self, archive: WeatherArchive) -> None:
        """Tests the relative humidity extraction methods."""

        hourly = archive.get_hourly_relative_humidity()
        utils.verify_positive_range_data_series(hourly, 100)

    @pytest.mark.parametrize("level", constants.PRESSURE_LEVELS)
    def test_pressure_methods_with_different_levels(
        self, archive: WeatherArchive, level: str
    ) -> None:
        """
        Tests the atmospheric pressure extraction
        method with different measurement levels.
        """

        hourly = archive.get_hourly_pressure(level=level)
        utils.verify_positive_data_series(hourly)

    @pytest.mark.parametrize("depth", (0, 26, 182, 255))
    def test_soil_moisture_methods(self, archive: WeatherArchive, depth: int) -> None:
        """
        Test the soil moisture extraction methods with different soil depths.
        """

        hourly = archive.get_hourly_soil_moisture(depth=depth)
        utils.verify_positive_data_series(hourly)

    def test_daylight_and_sunlight_duration_methods(
        self, archive: WeatherArchive
    ) -> None:
        """
        Tests the daily daylight and sunshine duration extraction methods.
        """

        daylight = archive.get_daily_daylight_duration()
        sunshine = archive.get_daily_sunshine_duration()

        utils.verify_positive_range_data_series(daylight, 86_400)
        utils.verify_positive_range_data_series(sunshine, 86_400)

    def test_sunrise_and_sunset_time_methods(self, archive: WeatherArchive) -> None:
        """
        Tests the daily sunrise and sunset time extraction methods.
        """

        sunrise = archive.get_daily_sunrise_time()
        sunset = archive.get_daily_sunset_time()

        datetime_format = r"%Y-%m-%dT%H:%M"

        assert isinstance(sunrise, pd.Series)
        assert isinstance(sunset, pd.Series)

        for time in pd.concat([sunrise, sunset], ignore_index=True):
            assert datetime.strptime(time, datetime_format)
