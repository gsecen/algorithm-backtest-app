"""This module calculates the sharp ratio of an asset"""

from annualized_return import get_annualized_return
from standard_deviation import get_annualized_standard_deviation


def get_sharp_ratio(asset_df, start_date, end_date, column_name="Open"):
    """Gets the sharp ratio of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets sharp ratio within date range.
    """

    # Calculating sharp ratio
    annualized_return = get_annualized_return(
        asset_df, start_date, end_date, column_name
    )
    annualized_standard_deviation = get_annualized_standard_deviation(
        asset_df, start_date, end_date, column_name
    )

    sharp_ratio = annualized_return / annualized_standard_deviation

    return sharp_ratio
