"""This module calculates the historical returns of an asset"""

from utils.time import get_rows_between_dates
from utils.custom_apply import calculate_return


def get_historical_returns(asset_df, start_date, end_date, column_name="Open"):
    """Calculates the historical returns of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        dict: Dates as keys and assets historical returns as values.
    """
    if asset_df is None:
        return

    rows = get_rows_between_dates(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if rows is None:
        return
    else:

        # Getting the returns of the values
        returns = (
            asset_df[column_name]
            .rolling(2)
            .apply(lambda x: calculate_return(x), raw=True)
        )

        # Getting the cumulative sum of the returns
        historical_returns = returns.cumsum()

        # Converting series' to dict with dates as keys and historical returns as values
        historical_returns_dict = dict(zip(rows["Date"], historical_returns))

        return historical_returns_dict
