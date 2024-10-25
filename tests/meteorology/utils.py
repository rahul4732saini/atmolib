"""
Utils.py
--------

This module comprises utility functions specifically designed
to support test functions and methods defined within the project.
"""

import pandas as pd


def verify_positive_data_series(series: pd.Series) -> None:
    """
    Verifies that all the values stored within the
    specified pandas Series object are greater than 0.
    """

    assert isinstance(series, pd.Series)
    assert (series >= 0).all()
