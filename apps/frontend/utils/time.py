"""This module helps with all time related functions"""

import datetime


def date_to_epoch(date, date_format="%Y-%m-%d"):
    """Converts date to seconds since epoch (January 1, 1970).

    Args:
        date (str): Date which you want converted.
        date_format (str, optional): Format which the date string is in. Defaults to "%Y-%m-%d".

    Returns:
        int: Seconds since epoch.
    """
    epoch = datetime.datetime(1970, 1, 1)

    # Converting date string to datetime object
    datetime_object = datetime.datetime.strptime(date, date_format)

    # Calculating how many seconds have past since epoch
    diff = datetime_object - epoch

    return int(diff.total_seconds())
