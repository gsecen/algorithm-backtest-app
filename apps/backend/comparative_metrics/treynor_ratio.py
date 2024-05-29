"""This module calculates the treynor ratio of an asset"""

from comparative_metrics.beta import get_beta
from performance_metrics.annualized_return import get_annualized_return


def get_treynor_ratio(asset1_df, asset2_df, start_date, end_date, column_name="Open"):
    """Gets the treynor ratio of an asset within date range.

    Args:
        asset1_df (df): Pandas dataframe containing first assets data.
        asset2_df (df): Pandas dataframe containing second assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str): Column name to calculate value from.

    Returns:
        float: Treynor ratio of asset within date range.
    """

    # Calculating the treynor ratio
    annualized_return = get_annualized_return(
        asset1_df, start_date, end_date, column_name
    )
    beta = get_beta(asset1_df, asset2_df, start_date, end_date, column_name)
    treynor_ratio = annualized_return / beta

    return treynor_ratio
