"""This module calculates the total cumulative return of an asset as a percentage"""

from utils.time import get_date_range_bounds
from utils.dataframe import get_value_by_date


def get_total_cumulative_return(asset_df, start_date, end_date):
    """Gets the total cumulative return as a percentage of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.

    Returns:
        float: Assets total cumulative return as a percentage within date range.
    """

    if asset_df is None:
        return

    date_range = get_date_range_bounds(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if date_range is None:
        return
    else:

        # Gettting the asset dates available within the range
        valid_start_date, valid_end_date = date_range

        # Calculating total cumulative return as a percentage
        start_price = get_value_by_date(asset_df, valid_start_date, "Close")
        end_price = get_value_by_date(asset_df, valid_end_date, "Close")
        return (((end_price - start_price) / end_price)) * 100
