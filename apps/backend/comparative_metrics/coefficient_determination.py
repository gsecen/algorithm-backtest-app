"""This module calculates the coefficient of determination"""

from pearson_correlation import get_pearson_correlation


def get_coefficient_determination(
    asset1_df, asset2_df, start_date, end_date, column_name="Open"
):
    """Gets the coefficient of determination between the returns of two assets within date range.

    Args:
        asset1_df (df): Pandas dataframe containing first assets data.
        asset2_df (df): Pandas dataframe containing second assets data.
        start_date (str): Start date for calculation.
        end_date (str): End date for calculation.
        column_name (str): Column name to calculate value from.

    Returns:
        float: Coefficient of determination between the returns of assets within date range.
    """
    # Calculating the coefficient of determination
    pearsons_correlation = get_pearson_correlation(
        asset1_df, asset2_df, start_date, end_date, column_name
    )
    coefficient_of_determination = pearsons_correlation**2

    return coefficient_of_determination
