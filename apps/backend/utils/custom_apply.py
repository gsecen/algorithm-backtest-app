"""This module helps with all pandas custom apply functions"""


def calculate_return(values):
    """Calculates the return as percentage from two values.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values.
    """
    return ((values[1] / values[0]) * 100) - 100


def calculate_negative_return(values):
    """Gets the negative return as percentage from two values. Will ignore positive returns.

    Args:
        values (list): Two values to calculate percentage from.

    Returns:
        float: Return as a percentage of the two values. Will only return negative values or nan.
    """
    return_percentage = ((values[1] / values[0]) * 100) - 100

    # If it is a positive return
    if return_percentage >= 0:
        return float("nan")
    else:
        return return_percentage
