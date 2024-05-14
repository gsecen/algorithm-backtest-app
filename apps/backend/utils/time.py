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
    query_string = f"https://query1.finance.yahoo.com/v7/finance/download/ED?period1=-999999999999999&period2=9999999999999999&interval=1d&events=history&includeAdjustedClose=true"
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


# dates = [
#     "2019-12-31",
#     "2020-01-02",
#     "2020-03-05",
#     "2020-04-06",
#     "2020-05-09",
#     "2020-05-09",
#     "2020-05-10",
#     "2020-05-15",
#     "2020-05-17",
#     "2020-05-18",
#     "2020-05-19",
#     "2020-05-20",
#     "2020-06-12",
# ]

# dates = get_trading_days("2019-12-01", "2022-07-13")

# gg = "1999-01-01"

# date = datetime.strptime(gg, "%Y-%m-%d")

# print(date.weekday())


def get_weekly_trading_dates(dates):
    """Gets all the trading days for weekly time based frequency.

    Args:
        dates (list): List of trading days to filter.

    Returns:
        list: List of trading days which are the start of each trading week.
    """
    trading_days = []

    for index, date in enumerate(dates[1:], 1):

        # Turning dates into datetime objects to be compared
        current_date = datetime.strptime(date, "%Y-%m-%d")
        previous_date = datetime.strptime(dates[index - 1], "%Y-%m-%d")

        # If the current day is Monday or later and previous day was earlier than Monday
        # In other words checks if trading day is the start of the week
        if current_date.weekday() < previous_date.weekday():
            trading_days.append(current_date)

    return trading_days


# print(is_date_earlier("01-05", "01-02", "%m-%d"))

# print(date.strftime("%m-%d"))


def get_annual_quarterly_or_monthly_trading_dates(dates, frequency):
    """Gets all the trading days for quarterly, monthly, or annuall time based frequencies.

    Args:
        dates (list): List of trading days to filter.
        frequency (str): Time based trading frequency which you want to filter data for. Can be
        annully, qaurterly, or monthly.

    Returns:
        list: List of trading days which are the start of each year(annual), qaurter, or month.
    """

    # Dictionary of time based trading frequencies
    # The values are the target month-day which the algorithm should run on
    frequencies = {
        "annually": ["01-01"],
        "quarterly": ["01-01", "04-01", "07-01", "10-01"],
        "monthly": [
            "01-01",
            "02-01",
            "03-01",
            "04-01",
            "05-01",
            "06-01",
            "07-01",
            "08-01",
            "09-01",
            "10-01",
            "11-01",
            "12-01",
        ],
    }

    trading_days = []

    for index, date in enumerate(dates[:-1]):

        # Turning dates into datetime objects to be compared
        current_date = datetime.strptime(date, "%Y-%m-%d")
        next_date = datetime.strptime(dates[index + 1], "%Y-%m-%d")

        for month_day in frequencies[frequency]:

            # The target trading day which the algorithm is supposed to run on
            target = datetime.strptime(month_day, "%m-%d").replace(next_date.year)

            # If the exact target trading date is not available it is in between two dates
            if current_date == target or current_date < target and next_date > target:
                trading_days.append(next_date)
                break

    return trading_days


def get_time_based_trading_dates(dates, frequency):
    """Gets the time based trading dates based on the frequency specified.

    Args:
        dates (list): List of trading days to filter.
        frequency (str): Time based trading frequency which you want to filter data for. Can be
        annully, qaurterly, monthly, or daily.

    Returns:
        list: List of trading days which are the start of each year(annual), quarter, month, or day.
    """
    match frequency:
        case "annually":
            return get_annual_quarterly_or_monthly_trading_dates(dates, frequency)
        case "quarterly":
            return get_annual_quarterly_or_monthly_trading_dates(dates, frequency)
        case "monthly":
            return get_annual_quarterly_or_monthly_trading_dates(dates, frequency)
        case "weekly":
            return get_weekly_trading_dates(dates)
        case "daily":
            return dates
