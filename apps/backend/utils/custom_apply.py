"""This module helps with all pandas custom apply functions"""


def calculate_return(values):
    """Calculates the return as percentage from two values.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values.
    """
    return ((values[1] - values[0]) / values[0]) * 100


def calculate_negative_return(values):
    """Gets the negative return as percentage from two values. Will ignore positive returns.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values. Will only return negative values or nan.
    """
    return_percentage = ((values[1] - values[0]) / values[0]) * 100

    # If it is a positive return
    if return_percentage >= 0:
        return float("nan")
    else:
        return return_percentage


def calculate_cumulative_return(current_value, starting_value):
    """Calculates the cumulative return between current value and starting value.

    Args:
        current_value (list): List of 1 value.
        (List of 1 value because values from .rolling.apply are in list form)
        starting_value (float): Starting value.

    Returns:
        float: Cumulative return as a percentage between current and starting value.
    """
    return ((current_value[0] - starting_value) / starting_value) * 100
