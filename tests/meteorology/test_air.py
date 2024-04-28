r"""
Tests objects and methods defined within `atmolib/meteorology/air.py` file.
"""

from types import NoneType

import pytest
import pandas as pd

import atmolib


class TestAirQuality:
    r"""
    Tests the `atmolib.AirQuality` class and its defined methods.
    """

    def test_object_initialization(
        self, valid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        r"""
        Test the `atmolib.AirQuality` object initialization with valid parameters.
        """

        for i in valid_coordinates:
            atmolib.AirQuality(*i)

        # Tests the object initialization with different `forecast_days` arguments.
        for days in (1, 4, 7):
            atmolib.AirQuality(0, 0, forecast_days=days)

    def test_object_initialization_with_invalid_parameters(
        self, invalid_coordinates: tuple[tuple[float, float], ...]
    ) -> None:
        r"""
        Test the `atmolib.AirQuality` object initialization with valid parameters.
        """

        with pytest.raises(AssertionError):

            # Expects an AssertionError upon initialization with invalid coorindates.
            for i in invalid_coordinates:
                atmolib.AirQuality(*i)

            # Expects an AssertionError upon initialization with invalid `forecast_days` argument.
            for days in (0, -1, 9):
                atmolib.AirQuality(0, 0, forecast_days=days)

    def test_air_quality_summary_methods(
        self,
        air_quality: atmolib.AirQuality,
    ) -> None:
        r"""
        Tests the air quality summary extraction methods.
        """

        current = air_quality.get_current_summary()
        hourly = air_quality.get_hourly_summary()

        assert isinstance(current, pd.Series) and isinstance(hourly, pd.DataFrame)

        # Verifies the index/columns of the resultant pandas.Series/DataFrame.
        assert (
            current.index.tolist()
            == atmolib.constants.CURRENT_AIR_QUALITY_SUMMARY_DATA_TYPES
            and hourly.columns.tolist()
            == atmolib.constants.HOURLY_AIR_QUALITY_SUMMARY_DATA_TYPES
        )

    @pytest.mark.parametrize("source", ("european", "us"))
    def test_current_aqi_method(
        self, air_quality: atmolib.AirQuality, source: str
    ) -> None:
        r"""
        Tests the `AirQuality.get_current_aqi` method with different sources.
        """

        aqi = air_quality.get_current_aqi(source)

        assert isinstance(aqi, int)
        assert 0 <= aqi <= 500

    @pytest.mark.parametrize(
        "gas", ("ozone", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide")
    )
    def test_gaseous_conc_methods(
        self, air_quality: atmolib.AirQuality, gas: str
    ) -> None:
        r"""
        Test the current and hourly gaseous concentration extraction methods.
        """

        current = air_quality.get_current_gaseous_conc(gas)
        hourly = air_quality.get_hourly_gaseous_conc(gas)

        assert isinstance(current, int | float) and isinstance(hourly, pd.Series)
        assert current >= 0
        assert all((hourly.to_numpy() >= 0) | hourly.isna())

    @pytest.mark.parametrize(
        "plant", ("alder", "birch", "grass", "mugwort", "olive", "ragweed")
    )
    def test_pollen_conc_methods(
        self, air_quality: atmolib.AirQuality, plant: str
    ) -> None:
        r"""
        Tests the current and hourly pollen grains concentration extraction methods.
        """

        current = air_quality.get_current_pollen_conc(plant)
        hourly = air_quality.get_hourly_pollen_conc(plant)

        assert isinstance(current, int | float | NoneType) and isinstance(
            hourly, pd.Series
        )
        assert current is None or current >= 0
        assert all((hourly.to_numpy() >= 0) | hourly.isna())

    def test_current_aqi_method_with_default_parameters(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the `AirQuality.get_current_aqi` method with default parameters.
        """

        aqi = air_quality.get_current_aqi()

        assert isinstance(aqi, int)
        assert 0 <= aqi <= 500

    def test_current_gas_and_pollen_conc_methods_with_default_parameters(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the `AirQuality.get_current_gaseous_conc` and
        `AirQuality.get_current_pollen_conc` methods with default parameters.
        """

        gas_conc = air_quality.get_current_gaseous_conc()
        pollen_conc = air_quality.get_current_pollen_conc()

        assert isinstance(gas_conc, int | float) and isinstance(
            pollen_conc, int | float | NoneType
        )
        assert gas_conc >= 0 and (pollen_conc is None or pollen_conc >= 0)

    def test_current_ammonia_and_dust_conc_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the current ammonia and dust concentration extraction methods.
        """

        ammonia_conc = air_quality.get_current_ammonia_conc()
        dust_conc = air_quality.get_current_dust_conc()

        assert isinstance(dust_conc, int | float) and isinstance(
            ammonia_conc, int | float | NoneType
        )
        assert (ammonia_conc is None or ammonia_conc >= 0) and dust_conc >= 0

    def test_current_particulate_matter_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the current particulate matter 2.5 & 10 extraction methods.
        """

        pm2_5_conc = air_quality.get_current_pm2_5_conc()
        pm10_conc = air_quality.get_current_pm10_conc()

        assert isinstance(pm2_5_conc, int | float) and isinstance(
            pm10_conc, int | float
        )
        assert pm2_5_conc >= 0 and pm10_conc >= 0

    def test_current_optical_methods(self, air_quality: atmolib.AirQuality) -> None:
        r"""
        Tests the current optical related extraction methods.
        """

        uv_index = air_quality.get_current_uv_index()
        optical_depth = air_quality.get_current_aerosol_optical_depth()

        assert isinstance(uv_index, int | float) and isinstance(
            optical_depth, int | float
        )
        assert uv_index >= 0 and optical_depth >= 0

    def test_hourly_gas_and_pollen_conc_methods_with_default_parameters(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the `AirQuality.get_hourly_gaseous_conc` and
        `AirQuality.get_hourly_pollen_conc` methods with default parameters.
        """

        gas_conc = air_quality.get_hourly_gaseous_conc()
        pollen_conc = air_quality.get_hourly_pollen_conc()

        assert isinstance(gas_conc, pd.Series) and isinstance(pollen_conc, pd.Series)
        assert all(gas_conc.to_numpy() >= 0) and all(
            (pollen_conc.to_numpy() >= 0) | pollen_conc.isna()
        )

    def test_hourly_ammonia_and_dust_conc_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the hourly ammonia and dust concentration extraction methods.
        """

        ammonia_conc = air_quality.get_hourly_ammonia_conc()
        dust_conc = air_quality.get_hourly_dust_conc()

        assert isinstance(dust_conc, pd.Series) and isinstance(ammonia_conc, pd.Series)
        assert all(dust_conc.to_numpy() >= 0) and all(
            (ammonia_conc.to_numpy() >= 0) | ammonia_conc.isna()
        )

    def test_hourly_particulate_matter_methods(
        self, air_quality: atmolib.AirQuality
    ) -> None:
        r"""
        Tests the hourly particulate matter 2.5 & 10 extraction methods.
        """

        pm2_5_conc = air_quality.get_hourly_pm2_5_conc()
        pm10_conc = air_quality.get_hourly_pm10_conc()

        assert isinstance(pm2_5_conc, pd.Series) and isinstance(pm10_conc, pd.Series)
        assert all(pm2_5_conc.to_numpy() >= 0) and all(pm10_conc.to_numpy() >= 0)

    def test_hourly_optical_methods(self, air_quality: atmolib.AirQuality) -> None:
        r"""
        Tests the hourly optical related extraction methods.
        """

        uv_index = air_quality.get_hourly_uv_index()
        optical_depth = air_quality.get_hourly_aerosol_optical_depth()

        assert isinstance(uv_index, pd.Series) and isinstance(optical_depth, pd.Series)
        assert all(uv_index.to_numpy() >= 0) and all(optical_depth.to_numpy() >= 0)
