"""This module helps with all fred series data related functions"""

import pandas as pd
from utils.dataframe import remove_non_numeric_rows


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

    dictionary = {"Date": dates, "value": values}

    # Converting dictionary of lists to df
    df = pd.DataFrame(dictionary)

    # Removing rows which have values that are not valid
    df = remove_non_numeric_rows(df, "value")

    return df
