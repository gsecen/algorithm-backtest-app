from utils.algorithm import sample_algo_request
from utils.time import get_trading_days, get_time_based_trading_dates
from utils.algorithm import calculate_task_weight, get_indicator_names
from utils.dataframe import get_value_by_date

from algorithm.dataset_builder import build_dataset

import pandas as pd
import operator


class Backtest:

    def __init__(self, algorithm, dataset):
        self.algorithm = algorithm
        self.dataset = dataset

        self.trading_frequency = algorithm["trading_frequency"]
        # self.trading_days = get_trading_days(
        #     algorithm["start_date"], algorithm["end_date"]
        # )
        self.starting_weight = algorithm["algorithm"]["weight"]

        self.balance = 100000

        self.operators = {
            ">": operator.gt,
            "<": operator.lt,
            "==": operator.eq,
            ">=": operator.ge,
            "<=": operator.le,
            "!=": operator.ne,
        }

    def calculate_holdings(
        self, date, tasks, weight, task_relative_weight, holdings=None
    ):

        # If first time recursive function has been called
        if holdings is None:
            holdings = {}

        for index, task in enumerate(tasks):

            # Getting the relative weight for task
            relative_weight = calculate_task_weight(
                len(tasks), index, weight, task_relative_weight
            )

            if task["type"] == "buy":
                asset = task["asset"]

                # Add the asset to holdings, if asset already exists add to existing asset weight
                if asset not in holdings:
                    holdings[asset] = relative_weight
                else:
                    holdings[asset] += relative_weight

            if task["type"] == "expression":
                self.handle_expression(date, task, weight, relative_weight, holdings)

            if task["type"] == "instructions":
                self.calculate_holdings(
                    date, task["tasks"], task["weight"], relative_weight, holdings
                )
        return holdings

    def handle_expression(self, date, task, weight, relative_weight, holdings):
        indicator1, indicator2 = get_indicator_names(task["conditions"])
        asset1 = task["conditions"]["condition1"]["asset"]
        asset2 = task["conditions"]["condition2"]["asset"]
        operator = task["conditions"]["operator"]
        asset1_dataset = self.dataset[asset1]
        asset2_dataset = self.dataset[asset2]

        if self.operators[operator](
            get_value_by_date(asset1_dataset, date, indicator1),
            get_value_by_date(asset2_dataset, date, indicator2),
        ):
            self.calculate_holdings(
                date, task["true"], weight, relative_weight, holdings
            )
        else:
            self.calculate_holdings(
                date, task["false"], weight, relative_weight, holdings
            )

    def ttt(self, date):
        print(
            self.calculate_holdings(
                date, gg.algorithm["algorithm"]["tasks"], gg.starting_weight, 1
            )
        )


dates = ["2020-01-01", "2020-01-02", "2020-01-03", "2020-01-04"]
values = ["12", "14", "20", "50"]

dictionary = {"Date": dates, "value": values}

# Converting dictionary of lists to df
df = pd.DataFrame(dictionary)

# print(df)

data = build_dataset(sample_algo_request)

gg = Backtest(sample_algo_request, data)

print(gg.ttt("2020-01-02"))
