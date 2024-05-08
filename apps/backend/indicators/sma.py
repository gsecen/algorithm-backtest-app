"""This module builds the simple moving average indicator"""

import pandas as pd


def sma(period, df, column_name):
    """Calculates and adds simple moving average indicator to dataframe.

    Args:
        period (int): Length of sma.
        df (df): Dataframe which you want sma for.
        column_name (str): Column in dataframe which you want to calculate sma for.

    Returns:
        df: Pandas dataframe with new sma data.
    """
    # Make sure column does not exist
    if f"sma {period}" not in df.columns:
        df[f"sma {period}"] = df[column_name].rolling(period).mean()

    return df
