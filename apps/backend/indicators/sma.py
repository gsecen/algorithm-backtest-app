"""This module builds the simple moving average indicator"""


def sma(period, df, column_name):
    """Calculates and adds simple moving average indicator to dataframe.

    Args:
        period (int): Length of sma.
        df (df): Dataframe which you want sma for.
        metric_type (str): Yahoo finance ("asset") or fred series ("series")
        column_name (str): Column name to calculate values from.

    Returns:
        df: Pandas dataframe with new sma data.
    """
    if df is None:
        return

    # Make sure column does not exist
    if f"sma {period}" not in df.columns:

        # Adding new column
        df[f"sma {period}"] = df[column_name].rolling(period).mean()

    return df
