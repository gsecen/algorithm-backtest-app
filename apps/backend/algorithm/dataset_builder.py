"""This module builds the dataset required to run algorithm"""

from utils.algorithm import get_buy_and_condition_data, sample_algo_request
from pandas import pd

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


# Creating an example df so that I dont have to keep requesting the actual data
# from yahoo finance and fred for testing
dates = ["2022-01-01", "2022-01-01", "2022-01-01"]
values = [3, 3.1, 3.2]
dictionary = {"date": dates, "value": values}
example_df = pd.DataFrame(dictionary)


def build_dataset(algorithm):
    required_data = get_buy_and_condition_data(algorithm)
    for i in required_data:
        print(i)


build_dataset(sample_algo_request)
