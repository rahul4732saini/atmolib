r"""
This module defines the AirQuality class facilitating the retrieval of air quality data from
the Open-Meteo Air Quality API based on latitudinal and longitudinal coordinates of the location.

The AirQuality class allows users to extract various types of air quality information, including 
current air quality index data and up to upcoming 7-days hourly air quality forecast data.
"""

import requests

from common import constants
from objects import BaseWeather


class AirQuality(BaseWeather):
    r"""
    AirQuality class to extract air quality data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Air Quality API to fetch the current or up to upcoming 7-days
    hourly and daily air quality forecast data.
    """

    _session = requests.Session()
    _api = constants.AIR_QUALITY_API

    def get_current_aqi(self, source: constants.AQI_SOURCES = "european") -> int:
        r"""
        Returns the current European air quality index value.

        Params:
        - source: Source of the Air Quality Index. Must be one of the following:
            - 'european' (Extracts the European Air Quality Index)
            - 'us' (Extracts the USA Air Quality Index)
        """

        if source not in ("european", "us"):
            raise ValueError(
                f"Expected `source` to be 'european' or 'us'. Got {source}."
            )

        return self.get_current_weather_data({"current": "european_aqi"})

    def get_current_ammonia_conc(self) -> int | float | None:
        r"""
        Returns the current concentration of ammonia(NH3) in air. Only available for Europe.
        Returns None for Non-European regions.
        """
        return self.get_current_weather_data({"current": "ammonia"})
