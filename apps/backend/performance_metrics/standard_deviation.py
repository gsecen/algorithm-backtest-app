"""This module calculates the standard deviation of an asset"""

from indicators.sample_df import sample_df_v5
from utils.time import get_rows_between_dates
from math import sqrt


def calculate_return(values):
    return ((values[1] / values[0]) * 100) - 100


def calculate_sqrt_deviation(values, mean):

    # Calculating sqaure root of deviation from mean price
    deviation = calculate_return(values) - mean
    squared_deviation = abs(deviation) ** 2

    return squared_deviation


def get_standard_deviation(asset_df, start_date, end_date, column_name="Open"):
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


# print(sample_df_v5)
get_standard_deviation(sample_df_v5, "2000-01-01", "2050-01-01", "value")


# print(0.7996804917520974 * sqrt(3))
