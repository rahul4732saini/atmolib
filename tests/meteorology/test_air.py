"""
Tests the classes and methods defined
within atmolib/meteorology/air.py.
"""

import pytest
import pandas as pd

from .. import utils
from atmolib import AirQuality, constants


class TestAirQuality:
    """Tests the `AirQuality` class and its defined methods."""

    def test_object_initialization(
        self, valid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """
        Test the `AirQuality` object initialization with valid parameters.
        """

        for lat, long in valid_coordinates:
            AirQuality(lat, long)

        # Tests the object initialization with different forecast days.
        for days in (1, 4, 7):
            AirQuality(0, 0, forecast_days=days)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        """
        Test the `AirQuality` object initialization with invalid parameters.
        """

        with pytest.raises(ValueError):

            # Expects an ValueError upon initialization with invalid coorindates.
            for lat, long in invalid_coordinates:
                AirQuality(lat, long)

            # Expects a ValueError upon initialization
            # with invalid forecast days specifications.
            for days in (0, -1, 9):
                AirQuality(0, 0, forecast_days=days)

    def test_air_quality_summary_methods(self, air_quality: AirQuality) -> None:
        """Tests the air quality summary extraction methods."""

        current = air_quality.get_current_summary()
        hourly = air_quality.get_hourly_summary()

        assert isinstance(current, pd.Series)
        assert isinstance(hourly, pd.DataFrame)

        # Verifies the indices and columns of the resultant
        # pandas Series and DataFrame objects.
        assert current.index.tolist() == constants.CURRENT_AIR_QUALITY_SUMMARY_PARAMS
        assert hourly.columns.tolist() == constants.HOURLY_AIR_QUALITY_SUMMARY_PARAMS

    @pytest.mark.parametrize("source", constants.AQI_SOURCES)
    def test_aqi_methods(self, air_quality: AirQuality, source: str) -> None:
        """Tests the AQI extraction methods with different AQI sources."""

        current = air_quality.get_current_aqi(source)

        # Effectively verifies that the AQI is an integer
        # and lies within the below specified range.
        assert current in range(0, 501)

    @pytest.mark.parametrize("gas", constants.GASES)
    def test_gaseous_conc_methods(self, air_quality: AirQuality, gas: str) -> None:
        """Test the gaseous concentration extraction methods."""

        current = air_quality.get_current_gaseous_conc(gas)
        hourly = air_quality.get_hourly_gaseous_conc(gas)

        assert current >= 0
        utils.verify_positive_data_series(hourly)

    @pytest.mark.parametrize("plant", constants.PLANTS)
    def test_pollen_conc_methods(self, air_quality: AirQuality, plant: str) -> None:
        """Tests the pollen grains concentration extraction methods."""

        current = air_quality.get_current_pollen_conc(plant)
        hourly = air_quality.get_hourly_pollen_conc(plant)

        assert current is None or current >= 0
        utils.verify_positive_or_null_data_series(hourly)

    def test_dust_conc_methods(self, air_quality: AirQuality) -> None:
        """Tests the dust concentration extraction methods."""

        current = air_quality.get_current_dust_conc()
        hourly = air_quality.get_hourly_dust_conc()

        assert current >= 0
        utils.verify_positive_data_series(hourly)

    def test_ammonia_conc_methods(self, air_quality: AirQuality) -> None:
        """Tests the ammonia concentration extraction methods."""

        current = air_quality.get_current_ammonia_conc()
        hourly = air_quality.get_hourly_ammonia_conc()

        assert current is None or current >= 0
        utils.verify_positive_or_null_data_series(hourly)

    def test_pm2_5_methods(self, air_quality: AirQuality) -> None:
        """Tests the particulate matter 2.5 extraction methods."""

        current = air_quality.get_current_pm2_5_conc()
        hourly = air_quality.get_hourly_pm10_conc()

        assert current >= 0
        utils.verify_positive_data_series(hourly)

    def test_pm10_methods(self, air_quality: AirQuality) -> None:
        """Tests the particulate matter 10 extraction methods."""

        current = air_quality.get_current_pm10_conc()
        hourly = air_quality.get_hourly_pm10_conc()

        assert current >= 0
        utils.verify_positive_data_series(hourly)

    def test_uv_index_methods(self, air_quality: AirQuality) -> None:
        """Tests the UV index extraction methods."""

        current = air_quality.get_current_uv_index()
        hourly = air_quality.get_hourly_uv_index()

        assert current >= 0
        utils.verify_positive_data_series(hourly)

    def test_aerosol_optial_depth_methods(self, air_quality: AirQuality) -> None:
        """Tests the optical depth extraction methods."""

        current = air_quality.get_current_aerosol_optical_depth()
        hourly = air_quality.get_hourly_aerosol_optical_depth()

        assert current >= 0
        utils.verify_positive_data_series(hourly)
