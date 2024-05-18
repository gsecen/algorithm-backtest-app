"""This module fetches historical data from fred economics"""

from utils.fred_data import filter_fred_series
from urllib.error import HTTPError
from dotenv import load_dotenv
import pandas as pd
import os

# Loading the env file
load_dotenv()


def get_series_data(series_id):
    """Gets FRED series data.

    Args:
        series_id (str): The series you want the data for.

    Returns:
        df: Pandas dataframe with the series dates and values.
    """
    try:
        query_string = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={os.getenv('FRED_API_KEY')}&file_type=json"
        df = filter_fred_series(pd.read_json(query_string))
        return df

    except HTTPError as e:
        print(
            f"HTTP error in function get_series_data, likely series does not exist: {e}"
        )
        return None

    except Exception as e:
        print(f"Error in function get_series_data: {e}")
        return None
