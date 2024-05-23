"""This module calculates the sortino ratio of an asset"""

from annualized_return import get_annualized_return
from downside_deviation import get_annualized_downside_deviation


def get_sortino_ratio(asset_df, start_date, end_date, column_name="Open"):
    """Gets the sortino ratio of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets sortino ratio within date range.
    """

    # Calculating sortino ratio
    annualized_return = get_annualized_return(
        asset_df, start_date, end_date, column_name
    )
    annualized_standard_deviation = get_annualized_downside_deviation(
        asset_df, start_date, end_date, column_name
    )

    sortino_ratio = annualized_return / annualized_standard_deviation

    return sortino_ratio
