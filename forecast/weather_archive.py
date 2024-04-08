r"""
This module defines the Archive class facilitating the retrieval of historical weather data from
the Open-Meteo Weather History API based on latitudinal and longitudinal coordinates of the location.

The Archive class allows users to extract vaious types of historical weather data information
ranging from 1940 till the present.
"""

from objects import BaseWeather


class Archive(BaseWeather):
    r"""
    Archive class to extract historical weather data based on latitude and longitude coordinates of
    the location within the specified date range. It interacts with the Open-Meteo Weather History
    API to fetch the weather data ranging from 1940 till the present.
    """
