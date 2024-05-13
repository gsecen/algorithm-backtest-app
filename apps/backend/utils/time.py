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


# dates = [
#     "2020-01-01",
#     "2020-01-02",
#     "2020-01-05",
#     "2020-01-06",
#     "2020-01-09",
#     "2020-01-12",
# ]

start = "2020-01-04"
end = "2020-01-11"


# test = []
# for i in dates:
#     if i == start or is_date_earlier(start, i):
#         test.append(i)


# print(test)


def get_trading_days(start_date, end_date):
    """Gets all the trading days between two dates.

    Args:
        start_date (str): Date to start looking for trading days.
        end_date (str): Date to stop looking for trading days.

    Returns:
        list: List of trading days.
    """

    trading_days = []

    # Gets all SPX data from 1928 until now (Dates are trading days)
    query_string = f"https://query1.finance.yahoo.com/v7/finance/download/^SPX?period1=-999999999999999&period2=9999999999999999&interval=1d&events=history&includeAdjustedClose=true"
    df = pd.read_csv(query_string)

    for date in df["Date"]:

        # If date is after start date
        if date == start_date or is_date_earlier(start_date, date):

            # If date is before end date
            if date == end_date or not is_date_earlier(end_date, date):
                trading_days.append(date)

    return trading_days


# print(get_trading_days("1919-01-01", "1930-01-01"))


def is_date_between(check_date, start_date, end_date, date_format="%Y-%m-%d"):
    """Checks if check date is in between start date and end date.

    Args:
        check_date (str): Date to check if in between.
        start_date (_type_): Sart date.
        end_date (_type_): End date.
        date_format (str, optional): Format which the date string is in. Defaults to "%Y-%m-%d".

    Returns:
        bool: True if check date is in between start date and end date. If not it returns False.
    """

    # If date is after start date
    if is_date_earlier(start_date, check_date, date_format):

        # If date is before end date
        if is_date_earlier(check_date, end_date, date_format):
            return True

    return False


dates = [
    "2019-12-31",
    "2020-01-02",
    "2020-03-05",
    "2020-04-06",
    "2020-05-09",
    "2020-06-12",
]

gg = "1999-01-01"

date = datetime.strptime(gg, "%Y-%m-%d")

# print(is_date_earlier("01-05", "01-02", "%m-%d"))

# print(date.strftime("%m-%d"))

quarterly = ["01-01", "04-01", "07-01", "10-01"]


for index, date in enumerate(dates):

    # Turn date string into datetime object and remove year from date just look at month and day
    date = datetime.strptime(date, "%Y-%m-%d")
    print(date)
    date = date.strftime("%m-%d")

    # print(date)

    # for month_day in quarterly:
    #     month_day = datetime.strptime(month_day, "%m-%d")
    #     if is_date_between(month_day, dates[index - 1], date, "%m-%d"):
    #         print(date)
