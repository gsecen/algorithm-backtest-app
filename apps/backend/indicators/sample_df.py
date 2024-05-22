import pandas as pd


dates = [
    "2019-12-29",
    "2019-12-30",
    "2019-12-31",
    "2020-01-01",
    "2020-01-02",
    "2020-01-03",
    "2020-01-04",
    "2020-01-05",
    "2020-02-01",
    "2020-02-02",
    "2020-02-03",
    "2020-02-04",
    "2020-02-05",
]

dates2 = [
    "2019-12-29",
    "2019-12-30",
    "2019-12-31",
    "2020-01-01",
    "2020-01-02",
    "2020-01-03",
    "2020-01-04",
    "2020-01-05",
    "2020-02-01",
    "2020-02-02",
]

dates4 = [
    "2020-01-01",
    "2020-01-02",
    "2020-01-03",
    "2020-01-04",
    "2020-01-05",
    "2020-01-06",
    "2020-01-07",
    "2020-01-08",
    "2020-01-09",
    "2020-01-10",
]

dates5 = [
    "2020-01-01",
    "2020-01-02",
    "2020-01-03",
    "2020-01-04",
]

values1 = [float("nan"), float("nan"), float("nan"), 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
values2 = [2, 3, 4, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
values3 = [53.73, 53.87, 53.85, 53.88, 54.08, 54.14, 54.50, 54.30, 54.40, 54.16]
values4 = [182.40, 182.74, 184.57, 183.05]
values5 = [100, 120, 105, 110, 125, 130, 140, 135, 125, 130]

dictionary = {"Date": dates, "value": values1}
dictionary2 = {"Date": dates, "value": values2}
dictionary3 = {"Date": dates2, "value": values3}
dictionary4 = {"Date": dates5, "value": values4}
dictionary5 = {"Date": dates4, "value": values5}

# Converting dictionary of lists to df
sample_df = pd.DataFrame(dictionary)

sample_df_no_nans = pd.DataFrame(dictionary2)
sample_df_v3 = pd.DataFrame(dictionary3)
sample_df_v4 = pd.DataFrame(dictionary4)
sample_df_v5 = pd.DataFrame(dictionary5)
