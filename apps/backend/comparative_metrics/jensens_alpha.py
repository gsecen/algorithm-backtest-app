from beta import get_beta
from performance_metrics.annualized_return import get_annualized_return
from math import sqrt


def get_jensens_alpha(asset1_df, asset2_df, start_date, end_date, column_name="Open"):

    # Calculating jensens alpha
    asset1_annualized_return = get_annualized_return(
        asset1_df, start_date, end_date, column_name
    )
    asset2_annualized_return = get_annualized_return(
        asset2_df, start_date, end_date, column_name
    )
    beta = get_beta(asset1_df, asset2_df, start_date, end_date, column_name)
    alpha = asset1_annualized_return - (beta * asset2_annualized_return)

    print(beta)

    return alpha


# from indicators.sample_df import sample_df_aaple, sample_df_spy

# print(
#     get_jensens_alpha(
#         sample_df_aaple, sample_df_spy, "2000-01-01", "2050-01-01", "value"
#     )
# )
