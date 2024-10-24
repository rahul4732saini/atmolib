"""
Tests the classes and methods defined
within `atmolib/meteorology/archive.py`.
"""

from datetime import datetime
from typing import Any

import pytest
import numpy as np
import pandas as pd

import atmolib
from atmolib import constants


class TestWeatherArchive:
    """
    Tests the `atmolib.WeatherArchive` class and its defined methods.
    """

    def test_object_initialization(
        self,
        valid_coordinates: tuple[tuple[float, float], ...],
        valid_archive_dates: tuple[tuple[str, str], ...],
    ) -> None:
        """
        Test the `atmolib.WeatherArchive` object initialization with valid parameters.
        """

        for lat, long in valid_coordinates:
            atmolib.WeatherArchive(
                lat, long, start_date="2020-01-01", end_date="2020-01-10"
            )

        for start, end in valid_archive_dates:
            atmolib.WeatherArchive(0, 0, start, end)

    def test_object_initialization_with_invalid_parameters(
        self,
        invalid_coordinates: tuple[tuple[float, float], ...],
        invalid_archive_dates: tuple[tuple[str, str], ...],
    ) -> None:
        """
        Tests the `atmolib.WeatherArchive` object initialization with invalid parameters.
        """

        with pytest.raises(ValueError):

            # Expects a ValueError upon initialization with invalid coordinates.
            for lat, long in invalid_coordinates:
                atmolib.WeatherArchive(
                    lat, long, start_date="2020-01-01", end_date="2020-01-10"
                )

            # Expects a ValueError upon initialization with
            # invalid state end date for the archive data.
            for start, end in invalid_archive_dates:
                atmolib.WeatherArchive(0, 0, start, end)

    @staticmethod
    def _verify_summary_methods(
        archive: atmolib.WeatherArchive, params: dict[str, Any]
    ) -> None:
        """Verifies the hourly anda daily summary extraction methods."""

        hourly = archive.get_hourly_summary(**params)
        daily = archive.get_daily_summary(**params)

        assert isinstance(hourly, pd.DataFrame)
        assert isinstance(daily, pd.DataFrame)

        assert (
            hourly.columns.tolist() == atmolib.constants.HOURLY_ARCHIVE_SUMMARY_LABELS
        )
        assert daily.columns.tolist() == atmolib.constants.DAILY_ARCHIVE_SUMMARY_LABELS

    @staticmethod
    def _verify_temperature_data_series(series: pd.Series) -> None:
        """
        Verifies the temperature data within the specified pandas Series object.
        """

        assert isinstance(series, pd.Series)
        assert issubclass(series.dtype.type, np.integer | np.floating)

    @staticmethod
    def _verify_cloud_cover_methods(hourly: pd.Series) -> None:
        """Verifies the cloud cover extraction methods."""

        assert isinstance(hourly, pd.Series)
        assert ((hourly >= 0) & (hourly <= 100)).all()

    # The following block tests summary data extraction methods.

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_summary_methods_with_different_temperature_units(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly and daily summary extraction
        methods with different temperature units.
        """
        self._verify_summary_methods(archive, {"temperature_unit": unit})

    @pytest.mark.parametrize("unit", constants.PRECIPITATION_UNITS)
    def test_summary_methods_with_different_precipitation_units(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly and daily summary extraction
        methods with different precipitation units.
        """
        self._verify_summary_methods(archive, {"precipitation_unit": unit})

    @pytest.mark.parametrize("unit", constants.WIND_SPEED_UNITS)
    def test_summary_methods_with_different_wind_speed_units(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly and daily summary extraction
        methods with different wind speed units.
        """
        self._verify_summary_methods(archive, {"wind_speed_unit": unit})

    # The following block tests temperature data extraction methods.

    @pytest.mark.parametrize("altitude", constants.TEMPERATURE_ALTITUDES)
    def test_hourly_temperature_method_with_different_altitudes(
        self, archive: atmolib.WeatherArchive, altitude: int
    ) -> None:
        """
        Tests the hourly temperature data extraction
        method with different atltitude levels.
        """

        hourly = archive.get_hourly_temperature(altitude=altitude)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_tempeature_methods_with_different_units(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly and daily temperature extraction
        methods with different temperature units.
        """

        hourly = archive.get_hourly_temperature(unit=unit)
        daily = archive.get_daily_temperature(unit=unit)

        self._verify_temperature_data_series(hourly)
        self._verify_temperature_data_series(daily)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_apparent_temperature_methods_with_different_units(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly and daily apparent temperature
        extraction methods with different temperature units.
        """

        hourly = archive.get_hourly_apparent_temperature(unit=unit)
        daily = archive.get_daily_apparent_temperature(unit=unit)

        self._verify_temperature_data_series(hourly)
        self._verify_temperature_data_series(daily)

    @pytest.mark.parametrize("unit", constants.TEMPERATURE_UNITS)
    def test_hourly_soil_temperature_method_with_different_units(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly soil temperature extraction
        method with different temperature units.
        """

        hourly = archive.get_hourly_soil_temperature(unit=unit)
        self._verify_temperature_data_series(hourly)

    @pytest.mark.parametrize("metric", constants.DAILY_WEATHER_STATISTICAL_METRICS)
    def test_daily_temperature_methods_with_different_metrics(
        self, archive: atmolib.WeatherArchive, metric: str
    ) -> None:
        """
        Tests the daily temperature and apparent temperature extraction
        methods with different weather statistical metrics.
        """

        temp = archive.get_daily_temperature(metric=metric)
        apparent_temp = archive.get_daily_apparent_temperature(metric=metric)

        self._verify_temperature_data_series(temp)
        self._verify_temperature_data_series(apparent_temp)

    # The following block tests precipitation data extraction methods.

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_periodical_precipitation_methods_unit_parameter(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly and daily precipitation extraction
        methods with different `unit` arguments.
        """

        hourly_precipitation = archive.get_hourly_precipitation(unit=unit)
        hourly_rainfall = archive.get_hourly_rainfall(unit=unit)

        daily_precipitation = archive.get_daily_total_precipitation(unit=unit)
        daily_rainfall = archive.get_daily_total_rainfall(unit=unit)

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

    @pytest.mark.parametrize("level", ("surface", "sealevel"))
    def test_hourly_atmospheric_pressure_method(
        self, archive: atmolib.WeatherArchive, level: str
    ) -> None:
        """
        Tests the `WeatherArchive.get_hourly_pressure` with different `level` arguments.
        """
        hourly = archive.get_hourly_pressure(level=level)
        assert isinstance(hourly, pd.Series) and all(hourly.to_numpy() >= 0)

    # The following block tests cloud coverage extraction methods.

    @pytest.mark.parametrize("level", ("low", "mid", "high"))
    def test_cloud_cover_methods_level_parameter(
        self, weather: atmolib.Weather, level: str
    ) -> None:
        """
        Tests the `WeatherArchive.get_hourly_cloud_cover`
        method with different `level` arguments.
        """
        self._verify_cloud_cover_methods(weather.get_hourly_cloud_cover(level=level))

    # The following block tests wind related data extraction methods.

    @pytest.mark.parametrize("altitude", (10, 100))
    def test_hourly_wind_methods_altitude_parameter(
        self, archive: atmolib.WeatherArchive, altitude: int
    ) -> None:
        """
        Tests the hourly wind related extraction
        methods with different `altitude` arguments.
        """

        speed = archive.get_hourly_wind_speed(altitude=altitude)
        direction = archive.get_hourly_wind_direction(altitude=altitude)

        assert isinstance(speed, pd.Series) and isinstance(direction, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(
            (direction.to_numpy() >= 0) & (direction.to_numpy() <= 360)
        )

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_hourly_wind_methods_unit_parameter(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the hourly wind related extraction
        methods with different `unit` arguments.
        """

        speed = archive.get_hourly_wind_speed(unit=unit)
        gusts = archive.get_hourly_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_daily_wind_methods_unit_parameter(
        self, archive: atmolib.WeatherArchive, unit: str
    ) -> None:
        """
        Tests the daily wind related extraction
        methods with different `unit` arguments.
        """

        speed = archive.get_daily_max_wind_speed(unit=unit)
        gusts = archive.get_daily_max_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    # The following block tests weather code extraction methods.

    @pytest.mark.parametrize("frequency", ("hourly", "daily"))
    def test_periodical_weather_code_method(
        self, archive: atmolib.WeatherArchive, frequency: str
    ) -> None:
        """
        Tests the `WeatherArchive.get_periodical_weather_code`
        method with different `frequency` arguments.
        """

        code = archive.get_periodical_weather_code(frequency)

        # Converting integers into strings in the `data` column to be used for
        # verification with the `atmolib.constants.WEATHER_CODES` dictionary.
        code["data"] = code["data"].astype(np.object_)
        code["data"] = code["data"].map(lambda x: str(x))

        assert isinstance(code, pd.DataFrame)
        assert code["data"].isin(atmolib.constants.WEATHER_CODES).all()
        assert code["description"].isin(atmolib.constants.WEATHER_CODES.values()).all()

    # All other types of weather data extraction
    # methods are tested in the following block.

    def test_relative_humidity_methods(self, weather: atmolib.Weather) -> None:
        """
        Tests the `WeatherArchive.get_hourly_relative_humidity` method.
        """
        hourly = weather.get_hourly_relative_humidity()
        assert isinstance(hourly, pd.Series)
        assert all((hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100))

    @pytest.mark.parametrize("depth", (0, 56, 128, 255))
    def test_hourly_soil_moisture_method(
        self, archive: atmolib.WeatherArchive, depth: int
    ) -> None:
        """
        Tests the hourly soil moisture extractions methods.
        """
        moisture = archive.get_hourly_soil_moisture(depth=depth)
        assert isinstance(moisture, pd.Series) and all(moisture.to_numpy() >= 0)

    def test_daylight_and_sunlight_duration_methods(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        """
        Tests the `WeatherArchive.get_daily_daylight_duration` and
        `WeatherArchive.get_sunshine_duration` methods.
        """

        daylight = archive.get_daily_daylight_duration()
        sunshine = archive.get_daily_sunshine_duration()

        assert isinstance(daylight, pd.Series) and isinstance(sunshine, pd.Series)
        assert all(
            (daylight.to_numpy() >= 0) & (daylight.to_numpy() <= 86_400)
        ) and all((sunshine.to_numpy() >= 0) & (sunshine.to_numpy() <= 86_400))

    def test_sunrise_and_sunset_time_methods(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        """
        Tests the `WeatherArchive.get_daily_sunrise_time` and
        `WeatherArchive.get_daily_sunset_time` methods.
        """

        sunrise = archive.get_daily_sunrise_time()
        sunset = archive.get_daily_sunset_time()

        datetime_format = r"%Y-%m-%dT%H:%M"

        assert isinstance(sunrise, pd.Series) and isinstance(sunset, pd.Series)

        # Maps the `sunrise` and `sunset` Series to verify
        # the datetime format of the resultant Series.
        sunrise.map(lambda x: datetime.strptime(x, datetime_format))
        sunset.map(lambda x: datetime.strptime(x, datetime_format))
