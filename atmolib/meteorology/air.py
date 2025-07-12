"""
Air Quality Module
------------------

This module defines the AirQuality class facilitating extraction
of air quality data from Open-Meteo's Air Quality API.
"""

import pandas as pd

from ..base import BaseForecast
from ..common import constants, tools


class AirQuality(BaseForecast):
    """
    AirQuality class defines methods for the extraction of air quality data
    based on the latitudinal and longitudinal coordinates of the location with
    a resolution of 11 kilometers (km).
    """

    __slots__ = (
        "_lat",
        "_long",
        "_timeout",
        "_params",
        "_timefmt",
        "_forecast_days",
        "_past_days",
    )

    _api = constants.AIR_QUALITY_API

    # Maximum number of days for which forecast data can be extracted.
    _max_forecast_days = 7

    def __init__(
        self,
        lat: int | float,
        long: int | float,
        forecast_days: int = 7,
        past_days: int = constants.DEFAULT_PAST_DAYS,
        timefmt: str = constants.DEFAULT_TIME_FORMAT,
        timeout: int | float | None = constants.DEFAULT_REQUEST_TIMEOUT,
    ) -> None:
        """
        Creates an instance of the AirQuality class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - forecast_days (int): Number of days for which forecast has to
        be extracted; must be in the range of 1 and 7. Defaults to 7.
        - past_days (int): Number of days for which past data has to be
        extracted; must be in the range of 0 and 92. Defaults to 0.
        - timefmt (str): Format of the date & time labels in periodic data
        tables; must be one of the following:
            - `iso8601` (ISO 8601 date & time format)
            - `unixtime` (Unix timestamp)

            Defaults to `iso8601`.
        - timeout (int | float | None): Maximum duration to wait for a response
        from the API endpoint. Must be a number greater than 0 or `None`.
        """
        super().__init__(lat, long, forecast_days, past_days, timefmt, timeout)

    @staticmethod
    def _verify_atmospheric_gas(gas: str) -> None:
        """
        Verifies the specified atmospheric gas and
        raises a ValueError if found invalid.
        """

        if gas not in constants.GASES:
            raise ValueError(f"Invalid atmospheric gas specified: {gas!r}")

    @staticmethod
    def _verify_plant_species(plant: str) -> None:
        """
        Verifies the specified plant species and
        raises a ValueError if found invalid.
        """

        if plant not in constants.PLANTS:
            raise ValueError(f"Invalid plant species specified: {plant!r}")

    def get_current_summary(self) -> pd.Series:
        """
        Extracts current air quality summary data.

        #### The summary data distribution includes the following:
        - European AQI
        - United States AQI
        - Particulate Matter PM 10
        - Particulate Matter PM 2.5
        - Carbon Monoxide[CO] Concentration
        - Nitrogen Dioxide[NO2] Concentration
        - Sulphur Dioxide[SO2] Concentration
        - Ozone[O3] Concentration
        - Dust Concentration
        - UV Index
        - Ammonia[NH3] Concentration (Only available for Europe)
        """

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = f",".join(constants.CURRENT_AIR_QUALITY_SUMMARY_PARAMS)

        return tools.get_current_summary(
            self._session,
            self._api,
            self._params | {"current": data_types},
            constants.CURRENT_AIR_QUALITY_SUMMARY_PARAMS,
            self._timeout,
        )

    def get_hourly_summary(self) -> pd.DataFrame:
        """
        Extracts hourly air quality summary data.

        #### The summary data distribution includes the following:
        - Particulate Matter PM 10
        - Particulate Matter PM 2.5
        - Carbon Monoxide[CO] Concentration
        - Nitrogen Dioxide[NO2] Concentration
        - Sulphur Dioxide[SO2] Concentration
        - Ozone[O3] Concentration
        - Dust Concentration
        - UV Index
        - Ammonia[NH3] Concentration (Only available for Europe)
        """

        # String representation of the summary data types separated
        # by commas as supported for requesting the API endpoint.
        data_types: str = f",".join(constants.HOURLY_AIR_QUALITY_SUMMARY_PARAMS)

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | {"hourly": data_types},
            constants.HOURLY_AIR_QUALITY_SUMMARY_PARAMS,
            self._timeout,
        )

    def get_current_aqi(self, source: str = "european") -> int:
        """
        Extracts current Air Quality Index based on the specified AQI source.

        #### Params:
        - source (str): Source of the Air Quality Index;
        must be one of the following:
            - `european` (Extracts the European Air Quality Index)
            - `us` (Extracts the USA Air Quality Index)

            Defaults to `european`.`
        """

        if source not in constants.AQI_SOURCES:
            raise ValueError(f"Invalid AQI source specified: {source!r}")

        return int(self._get_current_data("european_aqi"))

    def get_current_dust_conc(self) -> int | float:
        """
        Extracts current aerial dust concentration(micro g/m^3)
        at 10 meters(m) above the ground level.
        """
        return self._get_current_data("dust")

    def get_current_gaseous_conc(self, gas: str = "ozone") -> int | float:
        """
        Extracts current aerial concentration(micro g/m^3) of the specified
        atmospheric gas at 10 meters(m) above the ground level.

        #### Params:
        - gas (str): Atmospheric gas whose concentration has to be extracted;
        must be one of `ozone`, `carbon_dioxide`, `carbon_monoxide`, `ammonia`,
        `methane`, `nitrogen_dioxide`, or `sulphur_dioxide`. Defaults to `ozone`.
        """

        self._verify_atmospheric_gas(gas)
        return self._get_current_data(gas)

    def get_current_pm2_5_conc(self) -> int | float:
        """
        Extracts current aerial concentration(micro g/m^3) of particulate
        matter with a diameter smaller than 2.5 micro meter(m) at 10 meters(m)
        above the ground level.
        """
        return self._get_current_data("pm2_5")

    def get_current_pm10_conc(self) -> int | float:
        """
        Extracts current aerial concentration(micro g/m^3) of particulate
        matter with a diameter smaller than 10 micro meter(m) at 10 meters(m)
        above the ground level.
        """
        return self._get_current_data("pm10")

    def get_current_pollen_conc(self, plant: str = "grass") -> int | float | None:
        """
        Extracts current aerial pollen concentration(grains/m^3) of the specified
        plant. Only available for Europe as provided by CAMS European Air Quality
        forecast. Returns None for Non-European regions.

        #### Params:
        - plant (str): Plant whose pollen concentration has to be extracted;
        must be one of `alder`, `birch`, `grass`, `mugwort`, `olive`, `ragweed`.
        Defaults to `grass`.
        """

        self._verify_plant_species(plant)
        return self._get_current_data(f"{plant}_pollen")

    def get_current_uv_index(self) -> int | float:
        """Extracts current Ultra-Violet(UV) radiation index."""
        return self._get_current_data("uv_index")

    def get_current_aerosol_optical_depth(self) -> int | float:
        """
        Extracts current aerosol optical depth at a wavelength of 550nm.

        #### Brief:

        Aerosol optical depth (AOD) at 550 nm is a measure of the extinction of
        solar radiation at a wavelength of 550 nanometers (green-yellow region
        of the visible spectrum) due to aerosol particles in the atmosphere.
        """
        return self._get_current_data("aerosol_optical_depth")

    def get_hourly_dust_conc(self) -> pd.Series:
        """
        Extracts hourly aerial dust concentration(micro g/m^3)
        data at 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "dust"})

    def get_hourly_uv_index(self) -> pd.Series:
        """Extracts hourly Ultra-Violet(UV) radiation index data."""
        return self._get_periodical_data({"hourly": "uv_index"})

    def get_hourly_pm2_5_conc(self) -> pd.Series:
        """
        Extracts hourly aerial concentration(micro g/m^3) data of
        particulate matter with a diameter smaller than 2.5 micro meter(m)
        at 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "pm2_5"})

    def get_hourly_pm10_conc(self) -> pd.Series:
        """
        Extracts hourly aerial concentration(micro g/m^3) data of
        particulate matter with a diameter smaller than 10 micro meter(m)
        at 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "pm10"})

    def get_hourly_pollen_conc(self, plant: str = "grass") -> pd.Series:
        """
        Extracts hourly aerial pollen concentration(grains/m^3) data of
        the specified plant. Only available for Europe as provided by CAMS
        European Air Quality forecast. Returns None for Non-European regions.

        #### Params:
        - plant (str): Plant whose pollen concentration has to be extracted;
        must be one of `alder`, `birch`, `grass`, `mugwort`, `olive`, `ragweed`.
        Defaults to `grass`.
        """

        self._verify_plant_species(plant)
        return self._get_periodical_data({"hourly": f"{plant}_pollen"})

    def get_hourly_aerosol_optical_depth(self) -> pd.Series:
        """
        Extracts hourly aerosol optical depth data at a wavelength of 550nm.

        #### Brief:

        Aerosol optical depth (AOD) at 550 nm is a measure of the extinction of
        solar radiation at a wavelength of 550 nanometers (green-yellow region
        of the visible spectrum) due to aerosol particles in the atmosphere.
        """
        return self._get_periodical_data({"hourly": "aerosol_optical_depth"})

    def get_hourly_gaseous_conc(self, gas: str = "ozone") -> pd.Series:
        """
        Extracts hourly aerial concentration(micro g/m^3) data of the
        specified atmospheric gas at 10 meters(m) above the ground level.

        #### Params:
        - gas (str): Atmospheric gas whose concentration has to be extracted;
        must be one of `ozone`, `carbon_dioxide`, `carbon_monoxide`, `methane`,
        `ammonia`, `nitrogen_dioxide`, or `sulphur_dioxide`. Defaults to `ozone`.
        """

        self._verify_atmospheric_gas(gas)
        return self._get_periodical_data({"hourly": gas})
