r"""
This module defines the AirQuality class facilitating the retrieval of air quality data from
the Open-Meteo Air Quality API based on latitudinal and longitudinal coordinates of the location.

The AirQuality class allows users to extract various types of air quality information, including 
current air quality index data and up to upcoming 7-days hourly air quality forecast data.
"""

from objects import BaseWeather


class AirQuality(BaseWeather):
    r"""
    AirQuality class to extract air quality data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Air Quality API to fetch the current or up to upcoming 7-days
    hourly and daily air quality forecast data.
    """
