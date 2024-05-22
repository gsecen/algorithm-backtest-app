"""This module calculates the standard deviation of return of an asset"""

from indicators.sample_df import sample_df_v4, sample_df_v5
from utils.time import get_rows_between_dates
from math import sqrt


# Pandas .rolling.appy function
def calculate_return(values):
    """Calculates the return as percentage from two values.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values.
    """
    return ((values[1] / values[0]) * 100) - 100


# Pandas .rolling.apply function
def calculate_sqrt_deviation(values, mean):
    """Calculates the square root of deviation as a percentage from mean return.

    Args:
        values (list): Two values to calculate square root of deviation as a percentage from.
        mean (_type_): Dataframes mean return as a percentage.

    Returns:
        float: Square rooted deviation.
    """

    # Calculating sqaure root of deviation from mean return
    deviation = calculate_return(values) - mean
    squared_deviation = abs(deviation) ** 2

    return squared_deviation


def get_standard_deviation(asset_df, start_date, end_date, column_name="Open"):
    """Gets the standard deviation of return of an asset within date range.

    Args:
        asset_df (df): Pandas dataframe containing assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str, optional): Column name to calculate value from. Defaults to "Open".

    Returns:
        float: Assets standard deviation of return within date range.
    """
    if asset_df is None:
        return

    rows = get_rows_between_dates(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if rows is None:
        return
    else:

        # Getting the mean return of the values
        returns = (
            asset_df[column_name]
            .rolling(2)
            .apply(lambda x: calculate_return(x), raw=True)
        )
        mean_returns = returns.mean()

        # Getting the squared deviations from mean price
        squared_deviations = (
            asset_df["value"]
            .rolling(2)
            .apply(lambda x: calculate_sqrt_deviation(x, mean_returns), raw=True)
        )

        # Calculating standard deviation
        mean_of_devaition_squared = squared_deviations.sum() / len(
            asset_df[column_name]
        )
        standard_deviation = sqrt(mean_of_devaition_squared)

        return standard_deviation
