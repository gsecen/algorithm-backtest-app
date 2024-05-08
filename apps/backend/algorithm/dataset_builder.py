"""This module builds the dataset required to run algorithm"""

from utils.algorithm import get_buy_and_condition_data
from historical_data import *
from indicators.sma import sma


# Dictionary containing all indicator functions
functions = {"sma": sma}


def build_dataset(algorithm):
    """Builds dictionary with all the data required to run the algorithm.

    Args:
        algorithm (dict): Full algorithm request.

    Returns:
        dict: Dictionary containing all assets, series', and indicator data to run algorithm.
    """
    dataset = {}
    required_data = get_buy_and_condition_data(algorithm)

    for i in required_data:

        # Getting the ohlcv, or fred data
        if "asset" in i and i["asset"] not in dataset:
            dataset[i["asset"]] = get_ohlcv_data(i["asset"])

        if "series" in i and i["series"] not in dataset:
            dataset[i["series"]] = get_series_data(i["series"])

        # If condition and asset
        if "function" in i and "asset" in i:
            asset_df = dataset[i["asset"]]
            indicator = i["function"]
            indicator_input = i["period"]

            # Updating assets dataframe to include indicators data
            asset_df = functions[indicator](indicator_input, asset_df, "asset")

        # If condition and series
        if "function" in i and "series" in i:
            series_df = dataset[i["series"]]
            indicator = i["function"]
            indicator_input = i["period"]

            # Updating series' dataframe to include indicators data
            series_df = functions[indicator](indicator_input, series_df, "series")

    return dataset
