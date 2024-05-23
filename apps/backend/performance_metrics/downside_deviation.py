"""This module calculates the downside deviation of return of an asset"""

from utils.time import get_rows_between_dates
from statistics import stdev
from math import sqrt


# Pandas .rolling.appy function
def get_negative_return(values):
    """Gets the negative return as percentage from two values. Will ignore positive returns.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values. Will only return negative values or nan.
    """
    return_percentage = ((values[1] / values[0]) * 100) - 100

    # If it is a positive return
    if return_percentage >= 0:
        return float("nan")
    else:
        return return_percentage


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
            .apply(lambda x: get_negative_return(x), raw=True)
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
