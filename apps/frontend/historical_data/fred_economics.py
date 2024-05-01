"""This module fetches historical data from fred economics"""

from dotenv import load_dotenv
from utils.fred_data import filter_fred_series
import pandas as pd
import os

# Loading the env file
load_dotenv()


def get_series_data(series_id):
    """Gets FRED economics data series

    Args:
        series_id (str): Data series code.
        start_date (str): Date you want data to begin from. Format must be YYYY-DD-MM.
        end_date (str): Date you want data to end to. Format must be YYYY-DD-MM.

    Returns:
        df: Pandas dataframe containing the series data.
    """
    query_string = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={os.getenv('FRED_API_KEY')}&file_type=json"

    df = filter_fred_series(pd.read_json(query_string))

    return df
