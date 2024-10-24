"""
Tests the classes and methods defined
within `atmolib/meteorology/air.py`.
"""

from types import NoneType

import pytest
import pandas as pd

import atmolib
from atmolib import constants


class TestAirQuality:
    """
    Tests the `atmolib.AirQuality` class and its defined methods.
    """

    def test_object_initialization(
        self, valid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """
        Test the `atmolib.AirQuality` object initialization with valid parameters.
        """

        for lat, long in valid_coordinates:
            atmolib.AirQuality(lat, long)

        # Tests the object initialization with different `forecast_days` arguments.
        for days in (1, 4, 7):
            atmolib.AirQuality(0, 0, forecast_days=days)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """
        Test the `atmolib.AirQuality` object initialization with invalid parameters.
        """

        with pytest.raises(ValueError):

            # Expects an ValueError upon initialization with invalid coorindates.
            for lat, long in invalid_coordinates:
                atmolib.AirQuality(lat, long)

            # Expects an ValueError upon initialization with
            # invalid `forecast_days` argument.
            for days in (0, -1, 9):
                atmolib.AirQuality(0, 0, forecast_days=days)

    def test_air_quality_summary_methods(self, air_quality: atmolib.AirQuality) -> None:
        """Tests the air quality summary extraction methods."""

        current = air_quality.get_current_summary()
        hourly = air_quality.get_hourly_summary()

        assert isinstance(current, pd.Series)
        assert isinstance(hourly, pd.DataFrame)

        # Verifies the indices and columns of the resultant
        # pandas.Series and DataFrame objects.
        assert current.index.tolist() == constants.CURRENT_AIR_QUALITY_SUMMARY_PARAMS
        assert hourly.columns.tolist() == constants.HOURLY_AIR_QUALITY_SUMMARY_PARAMS

    @pytest.mark.parametrize("source", constants.AQI_SOURCES)
    def test_current_aqi_extraction_method(
        self, air_quality: atmolib.AirQuality, source: str
    ) -> None:
        """
        Tests the `AirQuality.get_current_aqi` method with different AQI sources.
        """

        aqi = air_quality.get_current_aqi(source)

        assert isinstance(aqi, int)
        assert 0 <= aqi <= 500

    @pytest.mark.parametrize("gas", constants.GASES)
    def test_gaseous_conc_extraction_methods(
        self, air_quality: atmolib.AirQuality, gas: str
    ) -> None:
        """
        Test the current and hourly gaseous concentration extraction methods.
        """

        current = air_quality.get_current_gaseous_conc(gas)
        hourly = air_quality.get_hourly_gaseous_conc(gas)

        assert isinstance(current, int | float)
        assert isinstance(hourly, pd.Series)

        assert current >= 0
        assert ((hourly >= 0) | hourly.isna()).all()

    @pytest.mark.parametrize("plant", constants.PLANTS)
    def test_pollen_conc_extraction_methods(
        self, air_quality: atmolib.AirQuality, plant: str
    ) -> None:
        """
        Tests the current and hourly pollen grains concentration extraction methods.
        """

        current = air_quality.get_current_pollen_conc(plant)
        hourly = air_quality.get_hourly_pollen_conc(plant)

        assert isinstance(current, int | float | NoneType)
        assert isinstance(hourly, pd.Series)

        assert current is None or current >= 0
        assert ((hourly >= 0) | hourly.isna()).all()

    def test_dust_conc_extraction_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        """
        Tests the current and hourly dust concentration extraction methods.
        """

        current = air_quality.get_current_dust_conc()
        hourly = air_quality.get_hourly_dust_conc()

        assert isinstance(hourly, pd.Series)

        assert current >= 0
        assert (hourly >= 0).all()

    def test_ammonia_conc_extraction_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        """
        Tests the current and hourly ammonia concentration extraction methods.
        """

        current = air_quality.get_current_ammonia_conc()
        hourly = air_quality.get_hourly_ammonia_conc()

        assert isinstance(hourly, pd.Series)

        assert current is None or current >= 0
        assert ((hourly >= 0) | hourly.isna()).all()

    def test_current_particulate_matter_extraction_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        """
        Tests the current particulate matter 2.5 & 10 extraction methods.
        """

        pm2_5_conc = air_quality.get_current_pm2_5_conc()
        pm10_conc = air_quality.get_current_pm10_conc()

        assert isinstance(pm2_5_conc, int | float)
        assert isinstance(pm10_conc, int | float)

        assert pm2_5_conc >= 0 and pm10_conc >= 0

    def test_hourly_particulate_matter_extraction_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        """
        Tests the hourly particulate matter 2.5 & 10 extraction methods.
        """

        pm2_5_conc = air_quality.get_hourly_pm2_5_conc()
        pm10_conc = air_quality.get_hourly_pm10_conc()

        assert isinstance(pm2_5_conc, pd.Series)
        assert isinstance(pm10_conc, pd.Series)

        assert (pm2_5_conc >= 0).all()
        assert (pm10_conc >= 0).all()

    def test_uv_index_extraction_methods(self, air_quality: atmolib.AirQuality) -> None:
        """
        Tests the current and hourly UV index extraction methods.
        """

        current = air_quality.get_current_uv_index()
        hourly = air_quality.get_hourly_uv_index()

        assert isinstance(hourly, pd.Series)

        assert current >= 0
        assert (hourly >= 0).all()

    def test_aerosol_optial_depth_extraction_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        "Tests the current and hourly optical depth extraction methods."

        current = air_quality.get_current_aerosol_optical_depth()
        hourly = air_quality.get_hourly_aerosol_optical_depth()

        assert isinstance(hourly, pd.Series)

        assert current >= 0
        assert (hourly >= 0).all()
