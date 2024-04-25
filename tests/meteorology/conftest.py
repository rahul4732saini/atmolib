import pytest
import pyweather


@pytest.fixture
def air_quality() -> pyweather.AirQuality:
    return pyweather.AirQuality(0, 0, forecast_days=2)


@pytest.fixture
def valid_marine_coordinates() -> tuple[tuple[int, int]]:
    return ((49.10, -39.55), (-8.30, 68.19), (-57.29, 122.78), (-44.62, -5.57))


@pytest.fixture
def invalid_marine_coordinates() -> tuple[tuple[int, int]]:
    return ((26.91, 75.54), (68.46, 118.64), (-2.93, -61.77), (-24.89, 144.93))
