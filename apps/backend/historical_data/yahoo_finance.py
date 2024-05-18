"""This module fetchs historical data from yahoo finance"""

import pandas as pd
from urllib.error import HTTPError
from utils.time import date_to_epoch


def get_ohlcv_data(
    symbol, interval="1d", start_date="1900-01-01", end_date="2050-01-01"
):
    """Gets historical open, high, low, close, adjusted close, volume data for symbol on yahoo finance

    Args:
        symbol (str): Symbol you want data for.
        start_date (str, optional): Date you want data to begin from. Defaults to "1900-01-01".
        end_date (str, optional): Date you want data to end to. Defaults to "2050-01-01".
        interval (str, optional): Get the daily(1d), weekly(1wk), or monthly(1mo) data. Defaults to "1d".

    Returns:
        df: Pandas dataframe containing all the data.
    """
    # Turning dates into seconds since epoch
    start = date_to_epoch(start_date)
    end = date_to_epoch(end_date)

    # Fetching the dataframe
    try:
        query_string = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={start}&period2={end}&interval={interval}&events=history&includeAdjustedClose=true"
        df = pd.read_csv(query_string)
        return df
    except HTTPError as e:
        print(f"HTTP error in function get_ohlcv_data: {e}")
        return None


print(get_ohlcv_data("sikdfj"))
