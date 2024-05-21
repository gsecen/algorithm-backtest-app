"""This module calculates the standard deviation of an asset"""

from indicators.sample_df import sample_df_v3
from utils.time import get_rows_between_dates
from math import sqrt


# Custom .rolling.appy function to calculate the sqaure root of deviation from mean price
def calculate_sqrt_deviation(data, mean):

    # Calculating sqaure root of deviation from mean price
    deviation = data - mean
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

        # Getting the mean of the values
        mean = asset_df[column_name].mean()

        # Getting the squared deviations from mean price
        squared_deviations = (
            sample_df_v3["value"]
            .rolling(1)
            .apply(lambda x: calculate_sqrt_deviation(x, mean), raw=True)
        )

        # Calculating standard deviation
        mean_of_devaition_squared = squared_deviations.sum() / len(
            asset_df[column_name]
        )
        standard_deviation = sqrt(mean_of_devaition_squared)

        return standard_deviation


print(get_standard_deviation(sample_df_v3, "2000-01-01", "2050-01-01", "value"))
