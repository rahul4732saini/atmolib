"""
Tests the public functions defined within atmolib/common/tools.py.
"""

import pytest
from atmolib import tools


def test_get_elevation_function_with_valid_coordinates(
    valid_coordinates: tuple[tuple[float, float], ...],
) -> None:
    """
    Tests the 'tools.get_elevation' function with valid coordinates.
    """

    for lat, long in valid_coordinates:
        assert isinstance(tools.get_elevation(lat, long), float)


def test_get_elevation_function_with_invalid_coordinates(
    invalid_coordinates: tuple[tuple[float, float], ...],
) -> None:
    """
    Tests the 'tools.get_elevation' function with invalid coordinates.
    """

    with pytest.raises(ValueError):
        for lat, long in invalid_coordinates:
            tools.get_elevation(lat, long)


def test_get_elevation_function_with_valid_timeouts(
    valid_timeouts: tuple[int | float | None, ...],
) -> None:
    """
    Tests the 'tools.get_elevation' function with valid request timeouts.
    """

    for timeout in valid_timeouts:
        tools.get_elevation(0, 0, timeout)


def test_get_elevation_function_with_invalid_timeouts(
    invalid_timeouts: tuple[int | float | None, ...],
) -> None:
    """
    Tests the 'tools.get_elevation' function with invalid request timeouts.
    """

    with pytest.raises(ValueError):
        for timeout in invalid_timeouts:
            tools.get_elevation(0, 0, timeout)


def test_city_details_function(cities: tuple[str, ...]) -> None:
    """
    Tests the 'tools.get_city_details' function with different city names.
    """

    for city in cities:
        assert isinstance(tools.get_city_details(city), list)


def test_city_details_function_with_invalid_count(
    invalid_city_counts: tuple[int | float, ...],
) -> None:
    """
    Tests the 'tools.get_city_details' function with an
    invalid city count argument.
    """

    with pytest.raises(ValueError):
        for count in invalid_city_counts:
            tools.get_city_details("delhi", count)


def test_city_details_function_with_valid_timeouts(
    valid_timeouts: tuple[int | float | None, ...],
) -> None:
    """
    Tests the 'tools.get_city_details' function with
    valid request timeouts.
    """

    for timeout in valid_timeouts:
        tools.get_city_details("delhi", timeout=timeout)


def test_city_details_function_with_invalid_timeouts(
    invalid_timeouts: tuple[int | float | None],
) -> None:
    """
    Tests the 'tools.get_city_details' function with
    invalid request timeouts.
    """

    with pytest.raises(ValueError):
        for timeout in invalid_timeouts:
            tools.get_city_details("delhi", timeout=timeout)
