<h1 align=center>
<img src="https://raw.githubusercontent.com/rahul4732saini/atmolib/main/assets/atmolib.png?raw=true" width=500>
</h1>

<a href="https://www.codefactor.io/repository/github/rahul4732saini/atmolib"><img src="https://www.codefactor.io/repository/github/rahul4732saini/atmolib/badge" alt="CodeFactor" /></a>
<a href="https://github.com/rahul4732saini/atmolib/actions/workflows/pytest.yml"><img src="https://github.com/rahul4732saini/atmolib/workflows/Pytest/badge.svg" alt="Pytest" /></a>

<a href="https://www.github.com/rahul4732saini/atmolib"><img src="https://img.shields.io/badge/status-beta-yellow?maxAge=60" alt="projectStatus"></a>
<a href="https://www.github.com/rahul4732saini/atmolib"><img src="https://img.shields.io/badge/python-3.10+-blue?label=Python&maxAge=60" alt="pythonVersion"></a>
<a href="https://github.com/rahul4732saini/atmolib/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?maxAge=60" alt="License"></a>

<a href="https://www.pypi.org/project/atmolib"><img src="https://img.shields.io/pypi/v/atmolib.svg?logo=pypi&logoColor=ffa07a&label=PyPI Version&maxAge=60" alt="PyPI-Version"></a>
<a href="https://www.pypi.org/project/atmolib"><img src="https://img.shields.io/pypi/dm/atmolib.svg?label=PyPI Downloads" alt="PyPI-Downloads"></a>

<a href="https://www.github.com/rahul4732saini/atmolib"><img src="https://img.shields.io/github/stars/rahul4732saini/atmolib.svg?style=social&label=Star&maxAge=60" alt="StarProject"></a>
<a href="https://www.twitter.com/rahulsaini4732"><img src="https://img.shields.io/twitter/follow/rahulsaini4732?style=social&label=Follow&maxAge=60" alt="Twitter"></a>
<a href="https://www.linkedin.com/in/rahul-saini-9191a5286/)"><img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=social&logo=linkedin&maxAge=60" alt="Linkedin"></a>

## Package Description

<b>atmolib</b> is a weather package that offers an easy and flexible way to its users to access and parse weather data in a pythonic way. The package uses the Open-Meteo Web APIs to fetch the weather data in its backend.

## Installation

Install `atmolib` using `pip`:

```bash
$ python -m pip install -U atmolib --no-cache-dir
```

[Required Dependencies](./requirements.txt)

## Quick Guide

<b>atmolib</b> offers a series of classes to its users which can be used for meteorology data extraction from Open-Meteo's Web APIs.

The classes along with their corresponding descriptions are mentioned as follows:

- `Weather`<br>
  Provides extensive access to current, hourly, and daily forecast data, including temperature, dew point, weather conditions, soil temperature, visibility, and more.
- `WeatherArchive`<br>
  Enables retrieval of historical weather data, spanning hourly and daily records from 1940 till the present day.
- `MarineWeather`<br>
  Grants access to current, hourly, and daily marine weather forecast data, covering wave height, direction, and period, with a resolution of up to 5 kilometers.
- `AirQuality`<br>
  Supplies current and hourly forecasts for air quality metrics, including AQI, atmospheric gas concentrations, and UV index.

The package also provides users with some useful functions as a part of the package as mentioned below:

- `get_elevation`<br>
  Extracts the elevation in meters(m) at the specified coordinates.

- `get_city_details`<br>
  Extracts the city details such as coordinates, country, timezone, etc. based on the specified city name.

## Basic Usage

This guide provides the basic usage of the atmolib package and highlights some of the generally used methods. All the methods in the package are designed to be used with minimal arguments with default
arguments primarily specified in all of them.

- `Weather` class usage:

```python
import atmolib as atmo

# 'forecast_days' is an optional argument and specifies the number
# of days for which forecast data is desired to be extracted.
weather = atmo.Weather(lat=26.91, long=75.54, forecast_days=10)

# Extracts a summary of weather forecast data.
weather.get_current_summary()
weather.get_hourly_summary()
weather.get_daily_summary()

# Extracts the current weather conditions.
weather.get_current_temperature()
weather.get_current_weather_code()
weather.get_current_cloud_cover()
weather.get_current_wind_speed()
weather.get_current_pressure()
weather.get_current_precipitation()
weather.get_current_relative_humidity()

# Extracts the hourly weather forecast data.
weather.get_hourly_temperature()
weather.get_hourly_visibility()
weather.get_hourly_wind_speed()
weather.get_hourly_precipitation_probability()
weather.get_hourly_soil_temperature()

# Extracts the daily weather forecast data.
weather.get_daily_temperature()
weather.get_daily_max_precipitation_probability()
weather.get_daily_max_uv_index()
weather.get_daily_max_wind_speed()
weather.get_daily_total_precipitation()
weather.get_daily_sunshine_duration()
```

- `WeatherArchive` provides the same methods as `Weather` class as a part of a data range with slight modifications in some methods.

- `MarineWeather` class usage:

```python
import atmolib as atmo

# 'forecast_days' is an optional argument and specifies the number
# of days for which forecast data is desired to be extracted.
# 'wave_type' refers to the type of waves for which marine
# weather data is desired to be extracted.
marine = atmo.MarineWeather(lat=0, long=0, wave_type='wind', forecast_days=7)

# Extracts a summary of marine weather forecast data.
marine.get_current_summary()
marine.get_hourly_summary()
marine.get_daily_summary()

# Extracts the current weather conditions.
marine.get_current_wave_height()
marine.get_current_wave_direction()
marine.get_current_wave_period()

# Extracts the hourly weather forecast data.
marine.get_hourly_wave_height()
marine.get_hourly_wave_direction()
marine.get_hourly_wave_period()

# Extracts the daily weather forecast data.
marine.get_daily_max_wave_height()
marine.get_daily_dominant_wave_direction()
marine.get_daily_max_wave_period()
```

- `AirQuality` class usage:

```python
import atmolib as atmo

air = atmo.AirQuality(lat=26.91, long=75.54, forecast_days=7)

# Extracts a summary of air quality forecast data.
air.get_current_summary()
air.get_hourly_summary()

# Extracts the current weather conditions.
air.get_current_aqi()
air.get_current_pm2_5_conc()
air.get_current_pm10_conc()
air.get_current_uv_index()
air.get_hourly_dust_conc()

# Extracts the hourly weather forecast data.
air.get_hourly_uv_index()
air.get_hourly_uv_index()
air.get_hourly_pm2_5_conc()
air.get_hourly_pm10_conc()
air.get_hourly_aerosol_optical_depth()
```

## Legals

<b>atmolib</b> is distributed under the MIT License. Refer to the [LICENSE](./LICENSE) for more details.

#### NOTE:

<b>atmolib</b> is not affiliated, endorsed, or vetted by <b>Open-Meteo</b>. It's an open-source tool that uses Open-Meteo's publicly available meteorology APIs, and is intended for <b>research and educational purposes only</b>.

## Call for Contributions

The <b>atmolib</b> project always welcomes your precious expertise and enthusiasm!
The package relies on its community's wisdom and intelligence to investigate bugs and contribute code. We always appreciate improvements and contributions to this project.
