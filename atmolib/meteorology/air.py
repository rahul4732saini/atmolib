"""
Air Quality Module
------------------

This module defines the AirQuality class facilitating extraction
of air quality data from Open-Meteo's Air Quality API.
"""

import atexit

import requests
import pandas as pd

from ..base import BaseForecast
from ..common import constants, tools


class AirQuality(BaseForecast):
    """
    AirQuality class defines the mechanism for extraction of air quality data based
    on the latitudinal and longitudinal coordinates of the location. It interacts
    with Open Meteo's Air Quality API to fetch the current or up to upcoming 7-days
    hourly air quality forecast data.
    """

    __slots__ = "_lat", "_long", "_forecast_days"

    _session = requests.Session()
    _api = constants.AIR_QUALITY_API

    # Maximum number of days for which forecast data can be extracted.
    _max_forecast_days = 7

    # Closes the request session upon exit.
    atexit.register(_session.close)

    def __init__(
        self, lat: int | float, long: int | float, forecast_days: int = 7
    ) -> None:
        """
        Creates an instance of the AirQuality class.

        #### Params:
        - lat (int | float): Latitudinal coordinates of the location.
        - long (int | float): Longitudinal coordinates of the location.
        - forecast_days (int): Number of days for which the forecast has to
        be extracted; must be in the range of 1 and 7. Defaults to 7.
        """
        super().__init__(lat, long, forecast_days)

    @staticmethod
    def _verify_atmospheric_gas(gas: constants.GASES) -> None:
        """
        Verifies the specified atmospheric gas and
        raises a ValueError if found invalid.
        """

        if gas not in (
            "ozone",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
        ):
            raise ValueError(f"Invalid atmospheric gas specified: {gas!r}")

    @staticmethod
    def _verify_plant_species(plant: constants.PLANTS) -> None:
        """
        Verifies the specified plant species and
        raises a ValueError if found invalid.
        """

        if plant not in ("alder", "birch", "grass", "mugwort", "olive", "ragweed"):
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
        data_types: str = f",".join(constants.CURRENT_AIR_QUALITY_SUMMARY_DATA_TYPES)

        return tools.get_current_summary(
            self._session,
            self._api,
            self._params | {"current": data_types},
            constants.CURRENT_AIR_QUALITY_SUMMARY_DATA_TYPES,
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
        data_types: str = f",".join(constants.HOURLY_AIR_QUALITY_SUMMARY_DATA_TYPES)

        return tools.get_periodical_summary(
            self._session,
            self._api,
            self._params | {"hourly": data_types},
            constants.HOURLY_AIR_QUALITY_SUMMARY_DATA_TYPES,
        )

    def get_current_aqi(self, source: str = "european") -> int:
        """
        Extracts current Air Quality Index based on the specified AQI source.

        #### Params:
        - source (str): Source of the Air Quality Index;
        must be one of the following:
            - `european` (Extracts the European Air Quality Index)
            - `us` (Extracts the USA Air Quality Index)

            Defaults to `european`.
        """

        if source not in constants.AQI_SOURCES:
            raise ValueError(f"Invalid AQI source specified: {source!r}")

        return int(self._get_current_data({"current": "european_aqi"}))

    def get_current_ammonia_conc(self) -> int | float | None:
        """
        Extracts current aerial ammonia(NH3) concentration (micro g/m^3).
        Only available for Europe. Returns None for Non-European regions.
        """
        return self._get_current_data({"current": "ammonia"})

    def get_current_dust_conc(self) -> int | float:
        """
        Extracts current aerial dust concentration(micro g/m^3)
        at 10 meters(m) above the ground level.
        """
        return self._get_current_data({"current": "dust"})

    def get_current_gaseous_conc(self, gas: constants.GASES = "ozone") -> int | float:
        """
        Extracts current aerial concentration(micro g/m^3) of the specified
        atmospheric gas at 10 meters(m) above the ground level.

        #### Params:
        - gas (str): Atmospheric gas whose concentration has to be extracted;
        must be one of `ozone`, `carbon_dioxide`, `nitrogen_dioxide`,
        or `sulphur_dioxide`. Defaults to `ozone`.
        """
        self._verify_atmospheric_gas(gas)
        return self._get_current_data({"current": gas})

    def get_current_pm2_5_conc(self) -> int | float:
        """
        Extracts current aerial concentration(micro g/m^3) of particulate
        matter with a diameter smaller than 2.5 micro meter(m) at 10 meters(m)
        above the ground level.
        """
        return self._get_current_data({"current": "pm2_5"})

    def get_current_pm10_conc(self) -> int | float:
        """
        Extracts current aerial concentration(micro g/m^3) of particulate
        matter with a diameter smaller than 10 micro meter(m) at 10 meters(m)
        above the ground level.
        """
        return self._get_current_data({"current": "pm10"})

    def get_current_pollen_conc(
        self, plant: constants.PLANTS = "grass"
    ) -> int | float | None:
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
        return self._get_current_data({"current": f"{plant}_pollen"})

    def get_current_uv_index(self) -> int | float:
        """
        Extracts current Ultra-Violet(UV) radiation index.
        """
        return self._get_current_data({"current": "uv_index"})

    def get_current_aerosol_optical_depth(self) -> int | float:
        """
        Extracts current aerosol optical depth at a wavelength of 550nm.

        #### Brief:

        Aerosol optical depth (AOD) at 550 nm is a measure of the extinction of
        solar radiation at a wavelength of 550 nanometers (green-yellow region
        of the visible spectrum) due to aerosol particles in the atmosphere. It
        is commonly used as an indicator of haze or the presence of aerosols in
        the atmosphere.
        """
        return self._get_current_data({"current": "aerosol_optical_depth"})

    def get_hourly_dust_conc(self) -> pd.Series:
        """
        Extracts hourly aerial dust concentration(micro g/m^3)
        data at 10 meters(m) above the ground level.
        """
        return self._get_periodical_data({"hourly": "dust"})

    def get_hourly_uv_index(self) -> pd.Series:
        """
        Extracts hourly Ultra-Violet(UV) radiation index data.
        """
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

    def get_hourly_pollen_conc(self, plant: constants.PLANTS = "grass") -> pd.Series:
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
        of the visible spectrum) due to aerosol particles in the atmosphere. It
        is commonly used as an indicator of haze or the presence of aerosols in
        the atmosphere.
        """
        return self._get_periodical_data({"hourly": "aerosol_optical_depth"})

    def get_hourly_gaseous_conc(self, gas: constants.GASES = "ozone") -> pd.Series:
        """
        Extracts hourly aerial concentration(micro g/m^3) data of the
        specified atmospheric gas at 10 meters(m) above the ground level.

        #### Params:
        - gas (str): Atmospheric gas whose concentration has to be extracted;
        must be one of `ozone`, `carbon_dioxide`, `nitrogen_dioxide`,
        or `sulphur_dioxide`. Defaults to `ozone`.
        """
        self._verify_atmospheric_gas(gas)
        return self._get_periodical_data({"hourly": gas})

    def get_hourly_ammonia_conc(self) -> pd.Series:
        """
        Extracts hourly aerial ammonia concentration(micro g/m^3) data.
        Only available for Europe. Returns None for Non-European regions.
        """
        return self._get_periodical_data({"hourly": "ammonia"})
