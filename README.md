<div align=center>
<img src="https://raw.githubusercontent.com/rahul4732saini/atmolib/main/assets/atmolib.png?raw=true" width=500>
</div>

[![CodeFactor](https://www.codefactor.io/repository/github/rahul4732saini/atmolib/badge)](https://www.codefactor.io/repository/github/rahul4732saini/atmolib)
[![Pytest](https://github.com/rahul4732saini/atmolib/workflows/Pytest/badge.svg)](https://github.com/rahul4732saini/atmolib/actions/workflows/pytest.yml)

[![PythonVersion](https://img.shields.io/badge/python-3.10+-blue?label=Python)](https://www.github.com/rahul4732saini/atmolib)
[![ProjectStatus](https://img.shields.io/badge/status-beta-yellow)](https://www.github.com/rahul4732saini/atmolib)
[![License](https://img.shields.io/badge/License-MIT-green)](https://github.com/rahul4732saini/atmolib/blob/main/LICENSE)

[![PyPI-Version](https://img.shields.io/pypi/v/atmolib.svg?logo=pypi&logoColor=ffa07a&label=PyPI-Version)](https://www.pypi.org/project/atmolib)
[![PyPI-Downloads](https://img.shields.io/pypi/dm/atmolib.svg?label=PyPI-Downloads)](https://www.pypi.org/project/atmolib)

[![StarCount](https://img.shields.io/github/stars/rahul4732saini/atmolib.svg?style=social&label=Star)](https://www.github.com/rahul4732saini/atmolib)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=social&logo=linkedin)](https://www.linkedin.com/in/rahul4732saini)

## Package Description

**Atmolib** is a python package that offers an easy and flexible way to its users to access and parse meteorology data in a pythonic way. It uses Open-Meteo's Web APIs to fetch the data in its backend.

## Installation

Install `atmolib` using `pip`:

```bash
python -m pip install -U atmolib --no-cache-dir
```

[Required Dependencies](./requirements.txt)

## Quick Guide

**Atmolib** offers a series of classes to its users which can be used for meteorology data extraction from Open-Meteo's Web APIs.

The classes along with their corresponding descriptions are mentioned as follows:

- `Weather` provides extensive access to current, hourly, and daily forecast data, including temperature, dew point, weather conditions, soil temperature, visibility, and more.

- `WeatherArchive` enables retrieval of historical weather data, spanning hourly and daily records from 1940 till the present day.

- `MarineWeather` grants access to current, hourly, and daily marine weather forecast data, covering wave height, direction, and period, with a resolution of 5 kilometers.

- `AirQuality` provides current and hourly forecasts for air quality metrics, including AQI, atmospheric gas concentrations, and UV index, with a resolution of 11 kilometers.

The package also provides users with some useful functions as mentioned below:

- `get_elevation` extracts the elevation in meters(m) at the specified coordinates.

- `get_city_details` extracts the city details such as coordinates, country, timezone, etc. based on the specified city name.

## Basic Overview

The following provides a basic overview of the classes defined within the package and highlights some of the generally used methods.
All the methods within the classes are designed to be used with minimal arguments, with default arguments primarily specified in all of them.

```python
>>> import atmolib as atmo
>>>
>>> # Weather class usage
>>>
>>> weather = atmo.Weather(lat=26.91, long=75.78)
>>> weather.get_current_temperature()
31.1
>>> weather.get_daily_max_uv_index()
Date
2025-08-03  7.80
2025-08-04  5.60
...
2025-08-09  2.35
>>>
>>> # WeatherArchive class usage
>>>
>>> archive = atmo.WeatherArchive(lat=25.67, long=91.74, start_date="2010-08-01", end_date="2010-08-03")
>>> archive.get_hourly_precipitation()
Datetime
2010-08-01T00:00    0.1
2010-08-01T01:00    0.4
...
2010-08-03T23:00    0.0
>>>
>>> # MarineWeather class usage
>>>
>>> marine = atmo.MarineWeather(lat=19.41, long=89.30)
>>> marine.get_current_wave_direction()
191
>>> marine.get_daily_wave_height()
Date
2025-08-03  1.76
2025-08-04  1.48
...
2025-08-09  1.78
>>>
>>> # AirQuality class usage
>>>
>>> air = atmo.AirQuality(lat=24.78, long=73.14)
>>> air.get_current_aqi()
70
>>> air.get_hourly_dust_conc()
Datetime
2025-08-03T00:00    89.0
2025-08-03T01:00    83.0
...
2025-08-07T32:00    NaN
```

## Legals

**Atmolib** is distributed under the MIT License. Refer to the [LICENSE](./LICENSE) for more details.

### NOTE

**Atmolib** is an independent project and is not affiliated with, endorsed by, or sponsored by **Open-Meteo**. It's an open-source tool that uses its publicly available meteorology APIs, and is intended for **research and educational purposes only**.

## Call for Contributions

The **Atmolib** project always welcomes your precious expertise and enthusiasm!
The package relies on its community's wisdom and intelligence to investigate bugs and contribute code. We always appreciate improvements and contributions to this project.
