"""This module calculates the standard deviation of return of an asset standardized to a period of a year"""

from standard_deviation import get_standard_deviation
from math import sqrt


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
