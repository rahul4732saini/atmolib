import pytest


@pytest.fixture
def valid_coordinates() -> tuple[tuple[float, float], ...]:
    return (
        (26.91, 75.54),
        (38.96, -112.66),
        (-67.47, 119.18),
        (-0.76, -21.46),
    )


@pytest.fixture
def invalid_coordinates() -> tuple[tuple[float, float], ...]:
    return (
        (-90.1, 85.4),
        (26.91, -180.1),
        (90.1, 154.44),
        (75.54, 180.1),
    )


@pytest.fixture
def cities() -> tuple[str, ...]:
    return (
        "delhi",
        "moscow",
        "tokyo",
        "los angeles",
        "seoul",
    )


@pytest.fixture
def invalid_city_counts() -> tuple[int | float, ...]:
    return 21, 0, -1, 2.5, 20.9
