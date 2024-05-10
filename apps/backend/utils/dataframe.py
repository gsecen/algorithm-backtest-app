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
        value = dataframe[dataframe["Date"] == date][column_name].item()
    except ValueError as ve:
        print(f"Key error in function get_value_by_date: {ve}")
        value = None
    except KeyError as ke:
        print(f"Index error in function get_value_by_date: {ke}")
        value = None

    return value
