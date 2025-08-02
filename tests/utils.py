"""
Utils.py
--------

This module comprises utility functions specifically designed
to support test functions and methods defined within the project.
"""

import numpy as np
import pandas as pd


def verify_positive_data_series(series: pd.Series) -> None:
    """
    Verifies that all the values stored within the specified
    pandas Series object are positive or 0.
    """

    assert isinstance(series, pd.Series)
    assert (series >= 0).all()


def verify_positive_or_null_data_series(series: pd.Series) -> None:
    """
    Verifies that all the values stored within the specified
    pandas Series object are either positive integers or None.
    """

    assert isinstance(series, pd.Series)
    assert ((series >= 0) | series.isna()).all()


def verify_temperature_data_series(series: pd.Series) -> None:
    """
    Verifies the temperature data stored within the
    specified pandas Series object.
    """

    verify_positive_data_series(series)

    assert isinstance(series, pd.Series)
    assert issubclass(series.dtype.type, np.integer | np.floating)


def verify_positive_range_data_series(series: pd.Series, end: int) -> None:
    """
    Verifies that all the values stored within the specified pandas
    Series object positive or 0, and less than the specified end.
    """

    verify_positive_data_series(series)
    assert (series <= end).all()
