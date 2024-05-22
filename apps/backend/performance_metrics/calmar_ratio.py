"""This module calculates the calmar ratio of an asset"""

from maximum_drawdown import get_maximum_drawdown
from annualized_return import get_annualized_return


def get_calmar_ratio(asset_df, start_date, end_date, column_name="Open"):
    """Gets an assets calmar ration within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets calmar ratio within date range.
    """

    # Calculating the calmar ratio
    annualized_return = get_annualized_return(
        asset_df, start_date, end_date, column_name
    )
    max_drawdown = get_maximum_drawdown(asset_df, start_date, end_date, column_name)

    return annualized_return / max_drawdown
