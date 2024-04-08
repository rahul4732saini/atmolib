r"""
This module defines the MarineWeather class facilitating the retrieval of marine weather data from
the Open-Meteo Marine Weather API based on latitudinal and longitudinal coordinates of the location.

The MarineWeather class allows users to extract various types of marine weather information, including 
current marine weather data and up to upcoming 8-days hourly and daily marine weather forecast data.
"""

import requests

from common import constants
from objects import BaseWeather


class MarineWeather(BaseWeather):
    r"""
    MarineWeather class to extract marine weather data based on latitude and longitude coordinates.
    It interacts with the Open-Meteo Marine Weather API to fetch the current or up to upcoming 8-days
    hourly and daily marine weather forecast data.
    """

    _session = requests.Session()
    _api = constants.MARINE_API
