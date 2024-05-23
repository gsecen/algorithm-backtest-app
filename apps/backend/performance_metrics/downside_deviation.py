"""This module calculates the downside deviation of return of an asset"""

from utils.time import get_rows_between_dates
from utils.custom_apply import calculate_negative_return
from statistics import stdev
from math import sqrt


def get_downside_deviation(asset_df, start_date, end_date, column_name="Open"):
    """Gets the downside deviation of return of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets downside deviation of return within date range.
    """
    if asset_df is None:
        return

    rows = get_rows_between_dates(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if rows is None:
        return
    else:

        # Getting the returns of the values
        negative_returns = (
            asset_df[column_name]
            .rolling(2)
            .apply(lambda x: calculate_negative_return(x), raw=True)
        )

        # Getting rid of all the nan in returns
        negative_returns.dropna(inplace=True)

        # Getting downside deviation
        return stdev(negative_returns)


def get_annualized_downside_deviation(
    asset_df, start_date, end_date, column_name="Open"
):
    """Gets the annualized downside deviation of return of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets annualized downside deviation of return within date range.
    """

    # Calculate annualized downside deviation
    annualized_downside_deviation = get_downside_deviation(
        asset_df, start_date, end_date, column_name
    ) * sqrt(365.25)

    return annualized_downside_deviation
