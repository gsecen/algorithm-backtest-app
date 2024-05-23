"""This module calculates the beta of two assets"""

from utils.time import get_rows_between_dates
from utils.dataframe import get_shared_rows
from utils.custom_apply import calculate_return
import numpy as np


def get_beta(asset1_df, asset2_df, start_date, end_date, column_name):
    """Gets the beta of two assets within date range.

    Args:
        asset1_df (df): Pandas dataframe containing first assets data.
        asset2_df (df): Pandas dataframe containing second assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str): Column name to calculate value from.

    Returns:
        float: Beta of assets within date range.
    """
    if asset1_df is None or asset2_df is None:
        return

    asset1_rows = get_rows_between_dates(asset1_df, start_date, end_date)
    asset2_rows = get_rows_between_dates(asset2_df, start_date, end_date)

    # If either asset does not have data within start and end date
    if asset1_rows is None or asset2_rows is None:
        return
    else:

        # Getting the shared rows (which are in date range) between assets
        shared_rows = get_shared_rows(asset1_rows, asset2_rows, column_name="Date")

        # If there are no shared rows
        if shared_rows is None:
            return

        asset1_shared_rows, asset2_shared_rows = shared_rows

        # Getting the returns of the values of asset 1 and asset 2
        asset1_returns = (
            asset1_shared_rows[column_name]
            .rolling(2)
            .apply(lambda x: calculate_return(x), raw=True)
        )
        asset2_returns = (
            asset2_shared_rows[column_name]
            .rolling(2)
            .apply(lambda x: calculate_return(x), raw=True)
        )

        # Calculating the beta
        # Doing returns[1:] becuase first value in returns always nan
        covariance = np.cov(asset1_returns[1:], asset2_returns[1:])
        beta = covariance[0, 1] / covariance[1, 1]

        return beta
