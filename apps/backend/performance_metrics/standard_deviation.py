"""This module calculates the standard deviation of return of an asset"""

from utils.time import get_rows_between_dates
from statistics import stdev
from math import sqrt


# Pandas .rolling.appy function
def calculate_return(values):
    """Calculates the return as percentage from two values.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values.
    """
    return ((values[1] / values[0]) * 100) - 100


def get_standard_deviation(asset_df, start_date, end_date, column_name="Open"):
    """Gets the standard deviation of return of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets standard deviation of return within date range.
    """
    if asset_df is None:
        return

    rows = get_rows_between_dates(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if rows is None:
        return
    else:

        # Getting the returns of the values
        returns = (
            asset_df[column_name]
            .rolling(2)
            .apply(lambda x: calculate_return(x), raw=True)
        )

        # Getting standard deviation
        # Doing returns[1:] becuase first value in returns always nan
        return stdev(returns[1:])


def get_annualized_standard_deviation(
    asset_df, start_date, end_date, column_name="Open"
):
    """Gets the annualized standard deviation of return of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets annualized standard deviation of return within date range.
    """

    # Calculate annualized standard deviation
    annualized_standard_deviation = get_standard_deviation(
        asset_df, start_date, end_date, column_name
    ) * sqrt(365.25)

    return annualized_standard_deviation
