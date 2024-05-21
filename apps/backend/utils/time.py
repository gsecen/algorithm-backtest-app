"""This module helps with all time related functions"""

from datetime import datetime, timedelta
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

            # Append date as string not datetime object
            trading_days.append(datetime.strftime(current_date, "%Y-%m-%d"))

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

                # Append date as string not datetime object
                trading_days.append(datetime.strftime(next_date, "%Y-%m-%d"))
                break

    return trading_days


def get_time_based_trading_dates(dates, frequency):
    """Gets the time based trading dates based on the frequency specified.

    Args:
        dates (list): List of trading days to filter.
        frequency (str): Time based trading frequency which you want to filter data for. Can be
        annully, qaurterly, monthly, weekly, or daily.

    Returns:
        list: List of trading days which you want to trade on based on frequency.
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


def get_date_range_bounds(df, start_date, end_date):
    """Gets the start and end dates of the dataframe where the date column is between the start and end date.

    Args:
        df (df): Pandas dataframe to get range bounds for.
        start_date (str): Starting date for the date range.
        end_date (str): Ending date for the date range.

    Returns:
        tuple/None: Start date in dataframe which is between start and end date range, end date in dataframe
        which is between start and end date range. None for no valid start or end date in dataframe which is
        between date range.
    """

    if df is None:
        return None

    # Getting the assets start and end dates
    asset_start_date = df["Date"].iloc[0]
    asset_end_date = df["Date"].iloc[-1]

    # If the end date to make calculations is before the asset start date the asset does not exist in timeframe
    if is_date_earlier(end_date, asset_start_date):
        return None

    # If the assets end date is before the start date to make calculations the asset does not exist in timeframe
    if is_date_earlier(asset_end_date, start_date):
        return None

    # If start date is before the assets starting date
    if is_date_earlier(start_date, asset_start_date):
        valid_start_date = asset_start_date
    else:
        valid_start_date = start_date

    # If end date is before assets ending date
    if is_date_earlier(end_date, asset_end_date):
        valid_end_date = end_date
    else:
        valid_end_date = asset_end_date

    # The very rare occasion when the start date or end date are the same as when the asset starts or ends
    if asset_start_date == start_date:
        valid_start_date = start_date
    if asset_end_date == end_date:
        valid_end_date = end_date

    return valid_start_date, valid_end_date


def get_rows_between_dates(asset_df, start_date, end_date):
    """Gets the rows of dataframe which are between two dates. (Within date range)

    Args:
        asset_df (df): Pandas dataframe you want rows for.
        start_date (str): Start date of range.
        end_date (str): End date of range.

    Returns:
        df: Pandas dataframe with rows that are in between start and end date.
    """
    if asset_df is None:
        return

    date_range = get_date_range_bounds(asset_df, start_date, end_date)

    # If asset does not have data within start and end date
    if date_range is None:
        return
    else:

        # Gettting the asset dates available within the range
        valid_start_date, valid_end_date = date_range

        # Getting the indexes of the start and end dates in dataframe
        start_index = asset_df.loc[asset_df["Date"] == valid_start_date].index[0]
        end_index = asset_df.loc[asset_df["Date"] == valid_end_date].index[0]

        # Getting the dataframe rows which are between the start and end indexes
        rows_between = asset_df.iloc[start_index : end_index + 1]

        return rows_between


def calculate_years_passed(start_date, end_date):
    """Calculates how many years have past between two dates.

    Args:
        start_date (str): Start date.
        end_date (str): End date.

    Returns:
        float: Years passed.
    """

    # Turning dates into datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    years_passed = (end - start).days / 365

    return years_passed


def calculate_days_passed(start_date, end_date):
    """Calculates how many days have past between two dates.

    Args:
        start_date (str): Start date.
        end_date (str): End date.

    Returns:
        int: Days passed.
    """
    # Turning dates into datetime objects
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    return (end - start).days


def subtract_days_from_date(start_date, days):
    """Subtracts however many days from the start date.

    Args:
        start_date (str): Date to subtract days from.
        days (int): Number of days to subtract from start date.

    Returns:
        str: String date which is however many days prior from the start date.
    """

    # Turning date into datetime object
    date = datetime.strptime(start_date, "%Y-%m-%d")

    # Subtracting days from date
    new_date = date - timedelta(days=days)

    # Convert new date to string
    new_date = datetime.strftime(new_date, "%Y-%m-%d")

    return new_date
