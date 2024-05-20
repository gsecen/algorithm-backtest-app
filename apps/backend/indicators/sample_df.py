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
]

values = [float("nan"), float("nan"), float("nan"), 1, 2, 3, 4, 5]

dictionary = {"Date": dates, "value": values}

# Converting dictionary of lists to df
sample_df = pd.DataFrame(dictionary)
