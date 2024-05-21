"""This module calculates the annualized rate of return of an asset"""

from utils.time import get_date_range_bounds, calculate_years_passed
from utils.dataframe import get_value_by_date


def get_annualized_return(asset_df, start_date, end_date):
    """Gets the annualized rate of return of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.

    Returns:
        float: Assets annualized rate of return within date range.
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

        # Calculating the annualized rate of return
        start_price = get_value_by_date(asset_df, valid_start_date, "Close")
        end_price = get_value_by_date(asset_df, valid_end_date, "Close")
        years_passed = calculate_years_passed(valid_start_date, valid_end_date)

        return ((end_price / start_price) ** (1 / years_passed) - 1) * 100
