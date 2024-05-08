"""This module builds the dataset required to run algorithm"""

from utils.algorithm import get_buy_and_condition_data, sample_algo_request
from indicators.sma import sma

import pandas as pd

# I want the dataset to consist of the assets and series, followed by that assets or series indicators,
# followed by the period of that indicator, followed by pandas df of dates and values for that specific
# indicator for that asset or series
# This way it is very easy to get the required data for each asset or series needed to run the algorithm
ideal_dataset = {
    "AAPL": {
        "sma": {
            "9": {
                # dataframe of dates and values
            },
            "15": {
                # dataframe of dates and values
            },
        },
        "ema": {
            "20": {
                # dataframe of dates and values
            }
        },
    },
    "MSFT": {
        "ema": {
            "12": {
                # dataframe of dates and values
            }
        }
    },
    "10Y2Y": {
        "sma": {
            "30": {
                # dataframe of dates and values
            }
        }
    },
}

# If we just have the asset or series and 1 df for each, searching for the data will be faster
ideal_dataset2 = {
    "AAPL": "pandas df containing all required data",
    "MSFT": "pandas df containing all required data",
}


# Creating an example df so that I dont have to keep requesting the actual data
# from yahoo finance and fred for testing
dates = [
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
    "2022-01-01",
]
values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
dictionary = {"date": dates, "value": values}
example_df = pd.DataFrame(dictionary)
# print(example_df)

gg = {}

gg["tset"] = sma(4, example_df, "value")

print(gg["tset"])


def build_dataset(algorithm):
    dataset = {}
    required_data = get_buy_and_condition_data(algorithm)

    # Adding the asset/series data to dataset
    # Adding example_df for now but will be yahoo_finance/fred data once finalized
    for i in required_data:
        # Only time 'asset' is not in key is if it is condition of fixed value because in that case
        # asset does not matter

        # Asset - yahoo finance data
        # Series - fred series data
        if "asset" in i:
            dataset[i["asset"]] = {"ohlcv": example_df}

        if "series" in i:
            dataset[i["series"]] = {"fred": example_df}

    print(dataset["MSFT"])


# build_dataset(sample_algo_request)
