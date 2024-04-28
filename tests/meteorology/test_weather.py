r"""
Tests the objects and methods defined within `atmolib/meteorology/weather.py` file.
"""

from datetime import datetime

import pytest
import numpy as np
import pandas as pd

import atmolib


class TestWeather:
    r"""
    Tests the `atmolib.Weather` class and its defined methods.
    """

    def test_object_initialization(
        self, valid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        r"""
        Test the `atmolib.Weather` object initialization with valid parameters.
        """

        for i in valid_coordinates:
            atmolib.Weather(*i)

        for i in (1, 10, 16):
            atmolib.Weather(0, 0, forecast_days=i)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        r"""
        Tests the `atmolib.Weather` object initialization with invalid parameters.
        """

        with pytest.raises(AssertionError):

            # Expects an AssertionError upon initialization with invalid coordinates.
            for i in invalid_coordinates:
                atmolib.Weather(*i)

            # Expects an AssertionError upon initialization with invalid `forecast_days` argument.
            for i in (0, -1, 17):
                atmolib.Weather(0, 0, forecast_days=i)

    @staticmethod
    def _verify_summary_methods(
        current: pd.Series, hourly: pd.DataFrame, daily: pd.DataFrame
    ) -> None:
        r"""
        Verifies the execution of summary extraction methods.
        """

        assert (
            isinstance(current, pd.Series)
            and isinstance(hourly, pd.DataFrame)
            and isinstance(daily, pd.DataFrame)
        )

        assert (
            (
                current.index.tolist()
                == atmolib.constants.CURRENT_WEATHER_SUMMARY_INDEX_LABELS
            )
            and (
                hourly.columns.tolist()
                == atmolib.constants.HOURLY_WEATHER_SUMMARY_COLUMN_LABELS
            )
            and (
                daily.columns.tolist()
                == atmolib.constants.DAILY_WEATHER_SUMMARY_COLUMN_LABELS
            )
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
    def _verify_cloud_cover_methods(current: int | float, hourly: pd.Series) -> None:
        r"""
        Verifies the cloud cover extraction methods.
        """

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert 0 <= current <= 100 and all(
            (hourly.to_numpy() >= 0) & (hourly.to_numpy() <= 100)
        )

    # The following block tests methods related to summary extraction methods.

    @pytest.mark.parametrize(
        ("temp_unit", "precipitation_unit"),
        (("celsius", "mm"), ("fahrenheit", "inch")),
    )
    def test_summary_methods_with_temperature_and_precipitation_unit_parameters(
        self, weather: atmolib.Weather, temp_unit: str, precipitation_unit: str
    ) -> None:
        r"""
        Tests the current, hourly and daily summary extraction methods with
        different `temperature_unit` and `precipitation_unit` parameters.
        """
        self._verify_summary_methods(
            weather.get_current_summary(
                temperature_unit=temp_unit, precipitation_unit=precipitation_unit
            ),
            weather.get_hourly_summary(
                temperature_unit=temp_unit, precipitation_unit=precipitation_unit
            ),
            weather.get_daily_summary(
                temperature_unit=temp_unit, precipitation_unit=precipitation_unit
            ),
        )

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_summary_methods_with_wind_speed_unit_parameters(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        r"""
        Tests the current, hourly and daily summary extraction
        methods with different `wind_speed` unit arguments.
        """
        self._verify_summary_methods(
            weather.get_current_summary(wind_speed_unit=unit),
            weather.get_hourly_summary(wind_speed_unit=unit),
            weather.get_daily_summary(wind_speed_unit=unit),
        )

    def test_summary_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the current, hourly and daily summary
        extraction methods with default parameters.
        """
        self._verify_summary_methods(
            weather.get_current_summary(),
            weather.get_hourly_summary(),
            weather.get_daily_summary(),
        )

    # The following block tests methods related to temperature extraction methods.

    @pytest.mark.parametrize("altitude", (2, 80, 120, 180))
    def test_temperature_methods_altitude_parameter(
        self, weather: atmolib.Weather, altitude: int
    ) -> None:
        r"""
        Tests the current and hourly temperature extraction
        methods with different `altitude` arguments.
        """

        current = weather.get_current_temperature(altitude=altitude)
        hourly = weather.get_hourly_temperature(altitude=altitude)

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert issubclass(hourly.dtype.type, np.integer | np.floating)

    @pytest.mark.parametrize("unit", ("celsius", "fahrenheit"))
    def test_current_temperature_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        r"""
        Tests the current temperature extraction
        methods with different `unit` arguments.
        """

        temp = weather.get_current_temperature(unit=unit)
        apparent_temp = weather.get_current_apparent_temperature(unit=unit)

        assert isinstance(temp, int | float) and isinstance(apparent_temp, int | float)

    @pytest.mark.parametrize("unit", ("celsius", "fahrenheit"))
    def test_hourly_temperature_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        r"""
        Tests the hourly temperature methods with different `unit` parameters.
        """

        temp = weather.get_hourly_temperature(unit=unit)
        apparent_temp = weather.get_hourly_apparent_temperature(unit=unit)
        soil_temp = weather.get_hourly_soil_temperature(unit=unit)

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

    @pytest.mark.parametrize("depth", (0, 6, 18, 54))
    def test_hourly_soil_temperature_method_depth_parameter(
        self, weather: atmolib.Weather, depth: int
    ) -> None:
        r"""
        Tests the `Weather.get_hourly_soil_temperature` with different `depth` arguments.
        """
        temp = weather.get_hourly_soil_temperature(depth=depth)

        assert isinstance(temp, pd.Series)
        assert issubclass(temp.dtype.type, np.integer | np.floating)

    @pytest.mark.parametrize("unit", ("celsius", "fahrenheit"))
    def test_daily_temperature_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        r"""
        Tests the daily temperature extraction methods with different `unit` arguments.
        """
        self._verify_temp_and_apparent_temp_methods(
            weather.get_daily_temperature(), weather.get_daily_apparent_temperature()
        )

    @pytest.mark.parametrize("type_", ("mean", "max", "min"))
    def test_daily_temperature_methods_type_parameter(
        self, weather: atmolib.Weather, type_: str
    ) -> None:
        r"""
        Tests the daily temperature extraction methods with different `type_` arguments.
        """
        self._verify_temp_and_apparent_temp_methods(
            weather.get_daily_temperature(type_=type_),
            weather.get_daily_apparent_temperature(type_=type_),
        )

    def test_current_temperature_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the current temperature extraction methods with default parameters.
        """
        temp = weather.get_current_temperature()
        apparent_temp = weather.get_current_apparent_temperature()

        assert isinstance(temp, int | float) and isinstance(apparent_temp, int | float)

    def test_hourly_temperature_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the hourly temperature extraction methods with default parameters.
        """

        temp = weather.get_hourly_temperature()
        apparent_temp = weather.get_hourly_apparent_temperature()
        soil_temp = weather.get_hourly_soil_temperature()

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

    def test_daily_temperature_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the daily temperature extraction methods with default parameters.
        """
        self._verify_temp_and_apparent_temp_methods(
            weather.get_daily_temperature(), weather.get_daily_apparent_temperature()
        )

    # The following block tests precipitation extraction related methods.

    @pytest.mark.parametrize("unit", ("mm", "inch"))
    def test_current_precipitation_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        r"""
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
        r"""
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

    def test_current_percipitation_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the precipitation extraction methods with default parameters.
        """

        precipitation = weather.get_current_precipitation()
        rainfall = weather.get_current_rainfall()
        snowfall = weather.get_current_snowfall()

        assert (
            isinstance(precipitation, int | float)
            and isinstance(rainfall, int | float)
            and isinstance(snowfall, int | float)
        )

        assert precipitation >= 0 and rainfall >= 0 and snowfall >= 0

    def test_periodical_precipitation_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the hourly and daily precipitation extraction methods with default parameters.
        """

        hourly_precipitation = weather.get_hourly_precipitation()
        hourly_rainfall = weather.get_hourly_rainfall()
        hourly_snowfall = weather.get_hourly_snowfall()

        daily_precipitation = weather.get_daily_total_precipitation()
        daily_rainfall = weather.get_daily_total_rainfall()

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

    def test_precipitation_probability_methods(self, weather: atmolib.Weather) -> None:
        r"""
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
        r"""
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
        r"""
        Tests the current and hourly cloud cover extraction
        methods with different `level` arguments.
        """
        self._verify_cloud_cover_methods(
            weather.get_current_cloud_cover(level=level),
            weather.get_hourly_cloud_cover(level=level),
        )

    def test_cloud_cover_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the current and hourly cloud cover
        extraction methods with default parameters.
        """
        self._verify_cloud_cover_methods(
            weather.get_current_cloud_cover(),
            weather.get_hourly_cloud_cover(),
        )

    def test_total_cloud_cover_methods(self, weather: atmolib.Weather) -> None:
        r"""
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
        r"""
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
        r"""
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

        assert speed >= 0 and direction in range(360) and gusts >= 0

    @pytest.mark.parametrize("altitude", (10, 80, 120, 180))
    def test_hourly_wind_methods_altitude_parameter(
        self, weather: atmolib.Weather, altitude: int
    ) -> None:
        r"""
        Tests the hourly wind related extraction
        methods with different `altitude` arguments.
        """

        speed = weather.get_hourly_wind_speed(altitude=altitude)
        direction = weather.get_hourly_wind_direction(altitude=altitude)

        assert isinstance(speed, pd.Series) and isinstance(direction, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(
            (direction.to_numpy() >= 0) & (direction.to_numpy() < 360)
        )

    @pytest.mark.parametrize("unit", ("kmh", "mph", "ms", "kn"))
    def test_hourly_wind_methods_unit_parameter(
        self, weather: atmolib.Weather, unit: str
    ) -> None:
        r"""
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
        r"""
        Tests the daily wind related extraction
        methods with different `unit` arguments.
        """

        speed = weather.get_daily_max_wind_speed(unit=unit)
        gusts = weather.get_daily_max_wind_gusts(unit=unit)

        assert isinstance(speed, pd.Series) and isinstance(gusts, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(gusts.to_numpy() >= 0)

    def test_current_wind_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the current wind related extraction methods with default parameters.
        """

        speed = weather.get_current_wind_speed()
        direction = weather.get_current_wind_direction()
        gusts = weather.get_current_wind_gusts()

        assert (
            isinstance(speed, int | float)
            and isinstance(direction, int | float)
            and isinstance(gusts, int | float)
        )

        assert speed >= 0 and direction in range(360) and gusts >= 0

    def test_hourly_wind_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the hourly wind related extraction methods with default parameters.
        """

        speed = weather.get_hourly_wind_speed()
        direction = weather.get_hourly_wind_direction()

        assert isinstance(speed, pd.Series) and isinstance(direction, pd.Series)
        assert all(speed.to_numpy() >= 0) and all(
            (direction.to_numpy() >= 0) & (direction.to_numpy() < 360)
        )

    def test_daily_wind_methods_with_default_parameters(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
        Tests the daily wind related extraction methods with default parameters.
        """

        speed = weather.get_daily_max_wind_speed()
        direction = weather.get_daily_dominant_wind_direction()
        gusts = weather.get_daily_max_wind_gusts()

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

    def test_current_weather_code_method(self, weather: atmolib.Weather) -> None:
        r"""
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
        r"""
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
        r"""
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
        r"""
        Tests the hourly soil moisture extractions methods.
        """
        moisture = weather.get_hourly_soil_moisture(depth=depth)
        assert isinstance(moisture, pd.Series) and all(moisture.to_numpy() >= 0)

    def test_daily_max_uv_index_method(self, weather: atmolib.Weather) -> None:
        r"""
        Tests the `atmolib.get_daily_max_uv_index` method.
        """
        daily = weather.get_daily_max_uv_index()
        assert isinstance(daily, pd.Series) and all(daily.to_numpy() >= 0)

    def test_is_day_or_night_method(self, weather: atmolib.Weather) -> None:
        r"""
        Tests the `atmolib.is_day_or_night` method.
        """
        is_day_or_night = weather.is_day_or_night()
        assert is_day_or_night in (1, 0)

    def test_visibility_methods(self, weather: atmolib.Weather) -> None:
        r"""
        Tests the current and hourly visibility extraction methods.
        """

        current = weather.get_current_visibility()
        hourly = weather.get_hourly_visibility()

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert current >= 0 and all(hourly.to_numpy() >= 0)

    def test_daylight_and_sunlight_duration_methods(
        self, weather: atmolib.Weather
    ) -> None:
        r"""
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
        r"""
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
