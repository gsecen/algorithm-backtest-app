import pandas as pd


dates = [
    "2020-01-01",
    "2020-01-02",
    "2020-01-03",
    "2020-01-04",
    "2020-01-05",
]

values = [1, 2, 3, 4, 5]

dictionary = {"Date": dates, "value": values}

# Converting dictionary of lists to df
sample_df = pd.DataFrame(dictionary)

print(sample_df)
