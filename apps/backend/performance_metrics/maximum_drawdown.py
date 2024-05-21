"""This module calculates the total drawdown of an asset as a percentage"""

from utils.time import get_rows_between_dates


def get_maximum_drawdown(asset_df, start_date, end_date, column_name="Open"):
    """Gets the maximum drawdown as a percentage of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.

    Returns:
        float: Assets maximum drawdown as a percentage within date range.
    """
    if asset_df is None:
        return

    rows = get_rows_between_dates(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if rows is None:
        return
    else:

        # Keep track of the highest value in dataframe
        max_value = rows[column_name].rolling(len(rows), min_periods=1).max()

        # Calculate drawdowns
        drawdowns = rows[column_name] / max_value - 1

        # Getting the worst drawdown
        return abs(drawdowns.min()) * 100
