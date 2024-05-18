"""This module helps with all pandas df related functions"""


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


def get_date_of_first_non_nan_value(dataframe, column_name):
    """Gets the date of the first non nan value from dataframe.

    Args:
        dataframe (df): Pandas dataframe.
        column_name (str): Column name to check values from.

    Returns:
        str/None: Returns first date which column name value is not nan. If there is no
        value which is not nan returns None.
    """

    # Pandas boolean indexing
    value = dataframe[dataframe[column_name].notna()]["Date"]

    if value.empty:
        return None
    else:
        # Return first value
        return value.iloc[0]


import pandas as pd

dates = ["1", "2", "3"]
values = [1, 2, 3]

dictionary = {"Date": dates, "value": values}

# Converting dictionary of lists to df
df = pd.DataFrame(dictionary)

if 3 in df["Date"].values:
    print("sdfio")


def does_value_exist(dataframe, value, column_name="Date"):
    """Checks if value exists in dataframe column.

    Args:
        dataframe (df): Pandas dataframe.
        value (int/str): Value to search for.
        column_name (str, optional): Column name to check if value exists. Defaults to "Date".

    Returns:
        bool: True if value exists in dataframe column. False if it does not exist.
    """

    # Check if value is in dataframe column
    if value in dataframe[column_name]:
        return True
    return False
