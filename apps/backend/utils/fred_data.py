"""This module helps with all fred series data related functions"""

import pandas as pd


def filter_fred_series(series):
    """Cleans up the fred data series df, removes unwanted data.

    Args:
        series (df): Pandas dataframe to be cleaned.

    Returns:
        df: Pandas dataframe with cleaned up data.
    """
    dates = []
    values = []

    # Adding needed values to lists
    for i in series["observations"]:
        dates.append(i["date"])
        values.append(i["value"])

    dictionary = {"date": dates, "value": values}

    # Converting dictionary of lists to df
    df = pd.DataFrame(dictionary)

    return df
