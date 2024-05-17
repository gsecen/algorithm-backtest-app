"""This module helps with all pandas df related functions"""

from math import isnan


def get_value_by_date(dataframe, date, column_name):
    """Gets value from the specified column corresponding to the given date.

    Args:
        dataframe (df): Pandas dataframe.
        date (str): The date to search for.
        column_name (str): Column name to get value from.

    Returns:
        int/None: Returns integer if value is found. If no match found returns None.
    """

    try:
        # Pandas boolean indexing
        value = dataframe[dataframe["Date"] == date][column_name].item()
    except ValueError as ve:
        print(f"Key error in function get_value_by_date: {ve}")
        value = None
    except KeyError as ke:
        print(f"Index error in function get_value_by_date: {ke}")
        value = None

    return value


def remove_non_numeric_rows(dataframe, column_name):
    """Removes entire row in dataframe if value in column is not a number.

    Args:
        dataframe (df): Dataframe to remove rows from.
        column_name (str): The name of column to check values from.

    Returns:
        df: Dataframe without rows that have non numeric values in column.
    """
    for i, value in enumerate(dataframe[column_name]):

        # If string value is not a number remove row from dataframe
        if not value.replace(".", "").isnumeric():
            dataframe.drop(i, inplace=True)

    dataframe.reset_index(drop=True, inplace=True)

    return dataframe


# get_date_of_first_non_nan_value()


# get_date_of_first_valid_value()


import pandas as pd

dates = ["2020-01", "2020-02", "2020-03", "2020-04"]
values = [float("nan"), float("nan"), 0.34, 0.34]

dictionary = {"Date": dates, "value": values}

# Converting dictionary of lists to df
df = pd.DataFrame(dictionary)


def test(dataframe, column_name):

    # Iterate through column name
    # for index, value in enumerate(dataframe[column_name]):

    # Get date for first value which is not float nan
    # if not isnan(value):
    #     return dataframe["Date"].iloc[index]

    value = dataframe[dataframe["value"] == 0.34]["Date"].items()

    return value


# value = dataframe[dataframe["Date"] == date][column_name].item()

print(test(df, "value"))
