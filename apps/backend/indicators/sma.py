"""This module builds the simple moving average indicator"""

import pandas as pd


def sma(period, df, metric_type):
    """Calculates and adds simple moving average indicator to dataframe.

    Args:
        period (int): Length of sma.
        df (df): Dataframe which you want sma for.
        metric_type (str): Yahoo finance ("asset") or fred series ("series")

    Returns:
        df: Pandas dataframe with new sma data.
    """

    # Make sure column does not exist
    if f"sma {period}" not in df.columns:

        # # If yahoo finance df calculate based on Close column
        # if metric_type == "asset":
        #     column_name = "Close"

        # # If fred df calculate based on value column
        # if metric_type == "series":
        #     column_name = "value"
        column_name = "value"

        # Adding new column
        df[f"sma {period}"] = df[column_name].rolling(period).mean()

    return df
