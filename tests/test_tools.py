r"""
Tests public functions defined within `pyweather/common/tools.py` file.
"""

import pytest
import pyweather


def test_get_elevation_function(
    valid_coordinates: tuple[tuple[float, float], ...]
) -> None:
    r"""
    Tests the `pyweather.tools.get_elevation` function with valid coordinates.
    """

    for i in valid_coordinates:
        assert isinstance(pyweather.get_elevation(*i), float)


def test_get_elevation_function_with_invalid_coordinates(
    invalid_coordinates: tuple[tuple[float, float], ...]
) -> None:
    r"""
    Tests the `pyweather.tools.get_elevation` function with invalid coordinates.
    """

    with pytest.raises(ValueError):

        # Expects a ValueError with invalid coordinates.
        for i in invalid_coordinates:
            pyweather.get_elevation(*i)


def test_city_details_function() -> None:
    r"""
    Tests the `pyweather.tools.get_city_details` function with different city names.
    """

    for i in ("delhi", "moscow", "tokyo", "los angeles", "seoul"):
        assert isinstance(pyweather.get_city_details(i), list)


def test_city_details_function_with_invalid_count() -> None:
    r"""
    Tests the `pyweather.tools.get_city_details` function with invalid `count` parameter.
    """

    with pytest.raises(ValueError):

        # Expects a ValueError with invalid `count` argument.
        for i in (("delhi", 21), ("washington", 0), ("moscow", -10)):
            pyweather.tools.get_city_details(*i)
