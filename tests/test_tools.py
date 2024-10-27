"""
Tests the public functions defined within atmolib/common/tools.py.
"""

import pytest
from atmolib import tools


def test_get_elevation_function_with_valid_coordinates(
    valid_coordinates: tuple[tuple[float, float], ...]
) -> None:
    """
    Tests the `atmolib.tools.get_elevation` function with valid coorindates.
    """

    for lat, long in valid_coordinates:
        assert isinstance(tools.get_elevation(lat, long), float)


def test_get_elevation_function_with_invalid_coordinates(
    invalid_coordinates: tuple[tuple[float, float], ...]
) -> None:
    """
    Tests the `atmolib.tools.get_elevation` function with invalid coordinates.
    """

    with pytest.raises(ValueError):

        # Expects a ValueError with invalid coordinates.
        for lat, long in invalid_coordinates:
            tools.get_elevation(lat, long)


def test_city_details_function(cities: tuple[str]) -> None:
    """
    Tests the `atmolib.tools.get_city_details` function with different city names.
    """

    for city in cities:
        assert isinstance(tools.get_city_details(city), list)


def test_city_details_function_with_invalid_count(
    invalid_city_counts: tuple[int | float],
) -> None:
    """
    Tests the `atmolib.tools.get_city_details` function
    with invalid city count arguments.
    """

    with pytest.raises(ValueError):

        # Expects a ValueError with invalid city count arguments.
        for count in invalid_city_counts:
            tools.get_city_details("delhi", count)
