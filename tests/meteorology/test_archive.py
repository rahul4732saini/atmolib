r"""
Tests the objects and methods defined within `atmolib/meteorology/archive.py` file.
"""

from datetime import datetime

import pytest
import numpy as np
import pandas as pd

import atmolib


class TestWeatherArchive:
    r"""
    Tests the `atmolib.WeatherArchive` class and its defined methods.
    """

    def test_object_initialization(
        self,
        valid_coordinates: tuple[tuple[float, float], ...],
        valid_archive_dates: tuple[tuple[str, str], ...],
    ) -> None:
        r"""
        Test the `atmolib.WeatherArchive` object initialization with valid parameters.
        """

        for i in valid_coordinates:
            atmolib.WeatherArchive(*i, start_date="2020-01-01", end_date="2020-01-10")

        for dates in valid_archive_dates:
            atmolib.WeatherArchive(0, 0, *dates)

    def test_object_initialization_with_invalid_parameters(
        self,
        invalid_coordinates: tuple[tuple[float, float], ...],
        invalid_archive_dates: tuple[tuple[str, str], ...],
    ) -> None:
        r"""
        Tests the `atmolib.WeatherArchive` object initialization with invalid parameters.
        """

        with pytest.raises(AssertionError):

            # Expects an AssertionError upon initialization with invalid coordinates.
            for i in invalid_coordinates:
                atmolib.WeatherArchive(
                    *i, start_date="2020-01-01", end_date="2020-01-10"
                )

            # Expects an AssertionError upon initialization with
            # invalid `start_date` and `end_date` argument.
            for dates in invalid_archive_dates:
                atmolib.WeatherArchive(0, 0, *dates)

    @staticmethod
    def _verify_summary_methods(hourly: pd.DataFrame, daily: pd.DataFrame) -> None:
        r"""
        Verifies the execution of hourly and daily summary extraction methods.
        """

        assert isinstance(hourly, pd.DataFrame) and isinstance(daily, pd.DataFrame)

        assert (
            hourly.columns.tolist()
            == atmolib.constants.HOURLY_ARCHIVE_SUMMARY_COLUMN_LABELS
        ) and (
            daily.columns.tolist()
            == atmolib.constants.DAILY_ARCHIVE_SUMMARY_COLUMN_LABELS
        )

    @staticmethod
    def _verify_temp_and_apparent_temp_methods(
        temp: pd.Series, apparent_temp: pd.Series
    ) -> None:
        r"""
        Verifies the `Weather.get_hourly_temperature` and
        `Weather.get_hourly_apparent_temperature` methods.
        """

        assert isinstance(temp, pd.Series) and isinstance(apparent_temp, pd.Series)
        assert issubclass(temp.dtype.type, np.integer | np.floating) and issubclass(
            apparent_temp.dtype.type, np.integer | np.floating
        )

    @staticmethod
    def _verify_cloud_cover_methods(hourly: pd.Series) -> None:
        r"""
        Verifies the cloud cover extraction methods.
        """
        assert isinstance(hourly, pd.Series)
        assert all((hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100))

    @staticmethod
    def _verify_hourly_temperature_methods(
        temp: pd.Series, apparent_temp: pd.Series, soil_temp: pd.Series
    ) -> None:
        r"""
        Verifies the hourly temperature extraction methods.
        """
        assert (
            isinstance(temp, pd.Series)
            and isinstance(apparent_temp, pd.Series)
            and isinstance(soil_temp, pd.Series)
        )
        assert (
            issubclass(temp.dtype.type, np.integer | np.floating)
            and issubclass(apparent_temp.dtype.type, np.integer | np.floating)
            and issubclass(soil_temp.dtype.type, np.integer | np.floating)
        )

    # The following block tests methods related to summary extraction methods.

    @pytest.mark.parametrize(
        ("temp_unit", "precipitation_unit"),
        (("celsius", "mm"), ("fahrenheit", "inch")),
    )
    def test_summary_methods_with_temperature_and_precipitation_unit_parameters(
        self,
        archive: atmolib.WeatherArchive,
        temp_unit: atmolib.constants.TEMPERATURE_UNITS,
        precipitation_unit: atmolib.constants.PRECIPITATION_UNITS,
    ) -> None:
        r"""
        Tests the hourly and daily summary extraction methods with
        different `temperature_unit` and `precipitation_unit` parameters.
        """
        self._verify_summary_methods(
            archive.get_hourly_summary(temp_unit, precipitation_unit),
            archive.get_daily_summary(temp_unit, precipitation_unit),
        )

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_summary_methods_with_wind_speed_unit_parameters(
        self,
        archive: atmolib.WeatherArchive,
        unit: atmolib.constants.WIND_SPEED_UNITS,
    ) -> None:
        r"""
        Tests the hourly and daily summary extraction
        methods with different `wind_speed` unit arguments.
        """
        self._verify_summary_methods(
            archive.get_hourly_summary(wind_speed_unit=unit),
            archive.get_daily_summary(wind_speed_unit=unit),
        )

    def test_summary_methods_with_default_parameters(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
        Tests the hourly and daily summary
        extraction methods with default parameters.
        """
        self._verify_summary_methods(
            archive.get_hourly_summary(), archive.get_daily_summary()
        )

    # The following block tests methods related to temperature extraction methods.

    @pytest.mark.parametrize("altitude", (2, 80, 120, 180))
    def test_temperature_methods_altitude_parameter(
        self, archive: atmolib.WeatherArchive, altitude
    ) -> None:
        r"""
        Tests the `WeatherArchive.get_hourly_temperature`
        method with different `altitude` arguments.
        """

        hourly = archive.get_hourly_temperature(altitude=altitude)

        assert isinstance(hourly, pd.Series)
        assert issubclass(hourly.dtype.type, np.integer | np.floating)

    @pytest.mark.parametrize("unit", ("celsius", "fahrenheit"))
    def test_hourly_temperature_methods_unit_parameter(
        self,
        archive: atmolib.WeatherArchive,
        unit: atmolib.constants.TEMPERATURE_UNITS,
    ) -> None:
        r"""
        Tests the hourly temperature extraction methods with different `unit` parameters.
        """

        temp = archive.get_hourly_temperature(unit=unit)
        apparent_temp = archive.get_hourly_apparent_temperature(unit=unit)
        soil_temp = archive.get_hourly_soil_temperature(unit=unit)

        self._verify_hourly_temperature_methods(temp, apparent_temp, soil_temp)

    @pytest.mark.parametrize("depth", (0, 56, 128, 255))
    def test_hourly_soil_temperature_method_depth_parameter(
        self, archive: atmolib.WeatherArchive, depth: int
    ) -> None:
        r"""
        Tests the `WeatherArchive.get_hourly_soil_temperature`
        with different `depth` arguments.
        """

        temp = archive.get_hourly_soil_temperature(depth=depth)

        assert isinstance(temp, pd.Series)
        assert issubclass(temp.dtype.type, np.integer | np.floating)

    @pytest.mark.parametrize("unit", ("celsius", "fahrenheit"))
    def test_daily_temperature_methods_unit_parameter(
        self,
        archive: atmolib.WeatherArchive,
        unit: atmolib.constants.TEMPERATURE_UNITS,
    ) -> None:
        r"""
        Tests the daily temperature extraction methods with different `unit` arguments.
        """
        self._verify_temp_and_apparent_temp_methods(
            archive.get_daily_temperature(unit=unit),
            archive.get_daily_apparent_temperature(unit=unit),
        )

    @pytest.mark.parametrize("type_", ("mean", "max", "min"))
    def test_daily_temperature_methods_type_parameter(
        self,
        archive: atmolib.WeatherArchive,
        type_: atmolib.constants.DAILY_WEATHER_REQUEST_TYPES,
    ) -> None:
        r"""
        Tests the daily temperature extraction methods with different `type_` arguments.
        """
        self._verify_temp_and_apparent_temp_methods(
            archive.get_daily_temperature(type_=type_),
            archive.get_daily_apparent_temperature(type_=type_),
        )

    def test_hourly_temperature_methods_with_default_parameters(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
        Tests the hourly temperature extraction methods with default parameters.
        """

        temp = archive.get_hourly_temperature()
        apparent_temp = archive.get_hourly_apparent_temperature()
        soil_temp = archive.get_hourly_soil_temperature()

        self._verify_hourly_temperature_methods(temp, apparent_temp, soil_temp)

    def test_daily_temperature_methods_with_default_parameters(
        self, archive: atmolib.Weather
    ) -> None:
        r"""
        Tests the daily temperature extraction methods with default parameters.
        """
        self._verify_temp_and_apparent_temp_methods(
            archive.get_daily_temperature(), archive.get_daily_apparent_temperature()
        )

    # The following block tests precipitation extraction related methods.

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_periodical_precipitation_methods_unit_parameter(
        self,
        archive: atmolib.WeatherArchive,
        unit: atmolib.constants.PRECIPITATION_UNITS,
    ) -> None:
        r"""
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

    def test_periodical_precipitation_methods_with_default_parameters(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
        Tests the hourly and daily precipitation extraction methods with default parameters.
        """

        hourly_precipitation = archive.get_hourly_precipitation()
        hourly_rainfall = archive.get_hourly_rainfall()
        hourly_snowfall = archive.get_hourly_snowfall()

        daily_precipitation = archive.get_daily_total_precipitation()
        daily_rainfall = archive.get_daily_total_rainfall()

        # Tests the hourly precipitation methods.
        assert (
            isinstance(hourly_precipitation, pd.Series)
            and isinstance(hourly_rainfall, pd.Series)
            and isinstance(hourly_snowfall, pd.Series)
        )
        assert (
            all(hourly_precipitation.to_numpy() >= 0)
            and all(hourly_rainfall.to_numpy() >= 0)
            and all(hourly_snowfall.to_numpy() >= 0)
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
        self,
        archive: atmolib.WeatherArchive,
        level: atmolib.constants.PRESSURE_LEVELS,
    ) -> None:
        r"""
        Tests the `WeatherArchive.get_hourly_pressure` with different `level` arguments.
        """
        hourly = archive.get_hourly_pressure(level=level)
        assert isinstance(hourly, pd.Series) and all(hourly.to_numpy() >= 0)

    # The following block tests cloud coverage extraction related methods.

    @pytest.mark.parametrize("level", ("low", "mid", "high"))
    def test_cloud_cover_methods_level_parameter(
        self, weather: atmolib.Weather, level: atmolib.constants.CLOUD_COVER_LEVEL
    ) -> None:
        r"""
        Tests the `WeatherArchive.get_hourly_cloud_cover`
        method with different `level` arguments.
        """
        self._verify_cloud_cover_methods(weather.get_hourly_cloud_cover(level=level))

    def test_cloud_cover_methods_with_default_parameters(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
        Tests the hourly cloud cover extraction methods with default parameters.
        """
        self._verify_cloud_cover_methods(archive.get_hourly_cloud_cover())
        self._verify_cloud_cover_methods(archive.get_hourly_total_cloud_cover())

    # The following block tests wind related extraction methods.

    @pytest.mark.parametrize("altitude", (10, 100))
    def test_hourly_wind_methods_altitude_parameter(
        self,
        archive: atmolib.WeatherArchive,
        altitude: atmolib.constants.ARCHIVE_WIND_ALTITUDES,
    ) -> None:
        r"""
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
        self,
        archive: atmolib.WeatherArchive,
        unit: atmolib.constants.WIND_SPEED_UNITS,
    ) -> None:
        r"""
        Tests the hourly wind related extraction
        methods with different `unit` arguments.
        """

        speed = archive.get_hourly_wind_speed(unit=unit)
        gusts = archive.get_hourly_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_daily_wind_methods_unit_parameter(
        self,
        archive: atmolib.WeatherArchive,
        unit: atmolib.constants.WIND_SPEED_UNITS,
    ) -> None:
        r"""
        Tests the daily wind related extraction
        methods with different `unit` arguments.
        """

        speed = archive.get_daily_max_wind_speed(unit=unit)
        gusts = archive.get_daily_max_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    def test_hourly_wind_methods_with_default_parameters(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
        Tests the hourly wind related extraction methods with default parameters.
        """

        speed = archive.get_hourly_wind_speed()
        direction = archive.get_hourly_wind_direction()
        gusts = archive.get_hourly_wind_gusts()

        assert (
            isinstance(speed, pd.Series)
            and isinstance(direction, pd.Series)
            and isinstance(gusts, pd.Series)
        )
        assert (
            all(speed.to_numpy() >= 0)
            and all((direction.to_numpy() >= 0) & (direction.to_numpy() <= 360))
            and all(gusts.to_numpy() >= 0)
        )

    def test_daily_wind_methods_with_default_parameters(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
        Tests the daily wind related extraction methods with default parameters.
        """

        speed = archive.get_daily_max_wind_speed()
        direction = archive.get_daily_dominant_wind_direction()
        gusts = archive.get_daily_max_wind_gusts()

        assert (
            isinstance(speed, pd.Series)
            and isinstance(direction, pd.Series)
            and isinstance(gusts, pd.Series)
        )
        assert (
            all(speed.to_numpy() >= 0)
            and all((direction.to_numpy() >= 0) & (direction.to_numpy() < 360))
            and all(gusts.to_numpy() >= 0)
        )

    # The following block tests weather code extraction methods.

    @pytest.mark.parametrize("frequency", ("hourly", "daily"))
    def test_periodical_weather_code_method(
        self,
        archive: atmolib.WeatherArchive,
        frequency: atmolib.constants.FREQUENCY,
    ) -> None:
        r"""
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
        r"""
        Tests the `WeatherArchive.get_hourly_relative_humidity` method.
        """
        hourly = weather.get_hourly_relative_humidity()
        assert isinstance(hourly, pd.Series)
        assert all((hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100))

    @pytest.mark.parametrize("depth", (0, 56, 128, 255))
    def test_hourly_soil_moisture_method(
        self, archive: atmolib.WeatherArchive, depth: int
    ) -> None:
        r"""
        Tests the hourly soil moisture extractions methods.
        """
        moisture = archive.get_hourly_soil_moisture(depth=depth)
        assert isinstance(moisture, pd.Series) and all(moisture.to_numpy() >= 0)

    def test_daylight_and_sunlight_duration_methods(
        self, archive: atmolib.WeatherArchive
    ) -> None:
        r"""
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
        r"""
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
