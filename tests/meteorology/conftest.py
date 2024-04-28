from datetime import date, timedelta

import pytest
import atmolib


@pytest.fixture
def weather() -> atmolib.Weather:
    return atmolib.Weather(0, 0, forecast_days=2)


@pytest.fixture
def archive() -> atmolib.WeatherArchive:
    return atmolib.WeatherArchive(0, 0, "2020-01-01", "2020-01-10")


@pytest.fixture
def air_quality() -> atmolib.AirQuality:
    return atmolib.AirQuality(0, 0, forecast_days=2)


@pytest.fixture
def valid_marine_coordinates() -> tuple[tuple[float, float], ...]:
    return (49.10, -39.55), (-8.30, 68.19), (-57.29, 122.78), (-44.62, -5.57)


@pytest.fixture
def invalid_marine_coordinates() -> tuple[tuple[float, float], ...]:
    return (26.91, 75.54), (68.46, 118.64), (-2.93, -61.77), (-24.89, 144.93)


@pytest.fixture
def valid_archive_dates() -> tuple[tuple[str, str], ...]:
    return (
        ("1940-01-01", "1940-02-01"),
        ("2022-09-15", "2022-10-02"),
        ("2003-12-13", "2003-12-31"),
        ("2001-04-24", "2001-04-25"),
    )


@pytest.fixture
def invalid_archive_dates() -> tuple[tuple[str, str], ...]:
    return (
        (
            date.today().strftime("%Y-%m-%d"),
            (date.today() + timedelta(days=2)).strftime("%Y-%m-%d"),
        ),
        ("1939-01-01", "1939-01-10"),
        ("1939-12-21", "1993-12-31"),
    )
