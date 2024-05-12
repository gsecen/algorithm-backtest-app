"""This module helps with all time related functions"""

from datetime import datetime
import pandas as pd


def date_to_epoch(date, date_format="%Y-%m-%d"):
    """Converts date to seconds since epoch (January 1, 1970).

    Args:
        date (str): Date which you want converted.
        date_format (str, optional): Format which the date string is in. Defaults to "%Y-%m-%d".

    Returns:
        int: Seconds since epoch.
    """
    epoch = datetime(1970, 1, 1)

    # Converting date string to datetime object
    datetime_object = datetime.strptime(date, date_format)

    # Calculating how many seconds have past since epoch
    diff = datetime_object - epoch

    return int(diff.total_seconds())


def get_trading_days(start_date, end_date):

    # Gets all SPX data from 1928 until now
    query_string = f"https://query1.finance.yahoo.com/v7/finance/download/^SPX?period1=-999999999999999&period2=9999999999999999&interval=1d&events=history&includeAdjustedClose=true"
    df = pd.read_csv(query_string)
    print(df["Date"])
    for i in df["Date"]:
        print(i)


# get_trading_days("2020-01-01", "2021-01-01")


dates = [
    "2020-01-01",
    "2020-01-02",
    "2020-01-05",
    "2020-01-06",
    "2020-01-09",
    "2020-01-12",
]

start = "2020-01-04"
end = "2020-01-11"


def is_date_earlier(date1, date2, date_format="%Y-%m-%d"):
    """Compares two dates to check if first date is before second date.

    Args:
        date1 (str): Date to check if earlier than second date.
        date2 (str): Date to check if later than first date.
        date_format (str, optional): Format which the date string is in. Defaults to "%Y-%m-%d".

    Returns:
        bool: True if date1 is earlier than date2. If not it returns False.
    """
    # Converting dates to datetime objects
    date1 = datetime.strptime(date1, date_format)
    date2 = datetime.strptime(date2, date_format)

    # Check if date1 is earlier than date2
    if date1 < date2:
        return True
    else:
        return False


print(is_date_earlier(end, start))
