"""This module calculates the trailing return of an asset over a given period as a percentage"""

from utils.time import (
    get_date_range_bounds,
    calculate_days_passed,
    subtract_days_from_date,
    get_next_available_date,
)
from utils.dataframe import get_value_by_date


# Keep in mind there are about 21 trading days a month
# Get trailing return calculates trailing return for approximately x days, cannot always be exact
def get_trailing_return(asset_df, start_date, end_date, days, column_name="Open"):
    """Gets the trailing return as a percentage of an asset within date range for approximately
    however many days.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        days (int): How many days (approximately) to calculate trailing return for.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets trailing return as a percentage within date range for period.
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

        # If the date range is not large enough to calculate trailing return
        if calculate_days_passed(valid_start_date, valid_end_date) <= days:
            return

        # Getting the date to start calculation on (try to be x periods before end date)
        target_date = subtract_days_from_date(valid_end_date, days)
        calculation_start_date = get_next_available_date(
            asset_df["Date"].values, target_date
        )

        # Calculating trailing return as a percentage
        start_price = get_value_by_date(asset_df, calculation_start_date, column_name)
        end_price = get_value_by_date(asset_df, valid_end_date, column_name)

        return (((end_price - start_price) / end_price)) * 100
