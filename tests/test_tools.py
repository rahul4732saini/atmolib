"""
Tests public functions defined within atmolib/common/tools.py.
"""

import pytest
import atmolib


def test_get_elevation_function_with_valid_coordinates(
    valid_coordinates: tuple[tuple[float, float], ...]
) -> None:
    """
    Tests the `atmolib.tools.get_elevation` function with valid coorindates.
    """

    for lat, long in valid_coordinates:
        assert isinstance(atmolib.get_elevation(lat, long), float)


def test_get_elevation_function_with_invalid_coordinates(
    invalid_coordinates: tuple[tuple[float, float], ...]
) -> None:
    """
    Tests the `atmolib.tools.get_elevation` function with invalid coordinates.
    """

    with pytest.raises(ValueError):

        # Expects a ValueError with invalid coordinates.
        for lat, long in invalid_coordinates:
            atmolib.get_elevation(lat, long)


def test_city_details_function() -> None:
    """
    Tests the `atmolib.tools.get_city_details` function with different city names.
    """

    for city in ("delhi", "moscow", "tokyo", "los angeles", "seoul"):
        assert isinstance(atmolib.get_city_details(city), list)


def test_city_details_function_with_invalid_count() -> None:
    """
    Tests the `atmolib.tools.get_city_details` function with invalid `count` parameter.
    """

    with pytest.raises(ValueError):

        # Expects a ValueError with invalid `count` argument.
        for city, count in (("delhi", 21), ("washington", 0), ("moscow", -10)):
            atmolib.tools.get_city_details(city, count)
