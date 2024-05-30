"""This module calculates the historical returns of an asset"""

from utils.time import get_rows_between_dates
from utils.custom_apply import calculate_cumulative_return


def get_historical_cumulative_returns(
    asset_df, start_date, end_date, column_name="Open"
):
    """Calculates the historical cumulative returns of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        dict: Dates as keys and assets historical cumulative returns as values.
    """
    if asset_df is None:
        return

    rows = get_rows_between_dates(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if rows is None:
        return
    else:

        # Getting the starting value so we can calculate cumulative return of every value
        starting_value = rows[column_name].iloc[0]

        # Getting the historical cumulative returns of the values
        cumulative_returns = (
            rows[column_name]
            .rolling(1)
            .apply(lambda x: calculate_cumulative_return(x, starting_value), raw=True)
        )

        # Converting series' to dict with dates as keys and historical cumluative returns as values
        historical_returns_dict = dict(zip(rows["Date"], cumulative_returns))

        return historical_returns_dict
