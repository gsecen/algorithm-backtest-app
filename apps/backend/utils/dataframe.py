"""This module helps with all pandas df related functions"""

import pandas as pd


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

    except ValueError as e:
        print(f"Key error in function get_value_by_date: {e}")
        value = None

    except KeyError as e:
        print(f"Index error in function get_value_by_date: {e}")
        value = None

    except Exception as e:
        print(f"Error in function get_value_by_date: {e}")
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
    if value in dataframe[column_name].values:
        return True
    return False


def get_first_value(dataframe, column_name="Date"):
    """Gets the first value from column name.

    Args:
        dataframe (df): Pandas dataframe.
        column_name (str, optional): Column name to get first value from. Defaults to "Date".

    Returns:
        str/int/float: First value in column name.
    """
    return dataframe[column_name].iloc[0]


def get_shared_rows(dataframe1, dataframe2, column_name):
    """Gets the rows of both dataframes which share the same values in column name.

    Args:
        dataframe1 (df): First pandas dataframe.
        dataframe2 (df): Second pandas dataframe.
        column_name (str): Column name.

    Returns:
        tuple/None: Pandas dataframe of shared rows of first dataframe, pandas dataframe of
        shared rows of second dataframe. Returns None if no shared rows.
    """
    # Pandas boolean indexing
    df1_shared_rows = dataframe1[dataframe1[column_name].isin(dataframe2[column_name])]

    # If there are no shared rows
    if len(df1_shared_rows.values) == 0:
        return None

    # Pandas boolean indexing
    df2_shared_rows = dataframe2[dataframe2[column_name].isin(dataframe1[column_name])]

    # Resetting the indexes, inplace true modifies the dataframe rather than creating a new one.
    df1_shared_rows.reset_index(inplace=True)
    df2_shared_rows.reset_index(inplace=True)

    return df1_shared_rows, df2_shared_rows


def build_dataframe_from_tuples(*values_column_names):
    """Builds a pandas dataframe with specified values and column names in tuple(s).
    The iterables in tuple will be the values for column name in tuple.

    Args:
        values_column_names (tuple): Tuple(s). (iterable, "column name")

    Returns:
        df: Pandas dataframe with specified values(iterables) and column names from tuple(s).
    """

    # Creating an empty dataframe
    dataframe = pd.DataFrame()

    for value, column_name in values_column_names:

        # Adding the values with the column name to dataframe
        dataframe[column_name] = value

    return dataframe
