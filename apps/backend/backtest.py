from utils.algorithm import sample_algo_request
from utils.time import get_trading_days, get_time_based_trading_dates
from utils.algorithm import (
    calculate_task_weight,
    get_indicator_names,
    get_asset_datasets,
    get_buy_and_condition_data,
)
from utils.dataframe import (
    get_value_by_date,
    get_date_of_first_non_nan_value,
    does_value_exist,
    get_first_value,
)

from algorithm.dataset_builder import build_dataset
from backtest_error_tracker import BacktestErrorTracker

import pandas as pd
import operator
from math import isnan


class Backtest:

    def __init__(self, algorithm, dataset):
        self.algorithm = algorithm
        self.dataset = dataset
        self.error_tracker = BacktestErrorTracker()

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

        # Recursion base case
        # If holding is False there was an error so stop recursion
        if holdings is False:
            return

        # If first time recursive function has been called
        if holdings is None:
            holdings = {}

        for index, task in enumerate(tasks):

            # Getting the relative weight for task
            relative_weight = calculate_task_weight(
                len(tasks), index, weight, task_relative_weight
            )

            if task["type"] == "buy":
                if self.handle_buy(task, holdings, relative_weight):
                    holdings = False

            if task["type"] == "expression":
                self.handle_expression(date, task, weight, relative_weight, holdings)

            if task["type"] == "instructions":

                self.calculate_holdings(
                    date,
                    task["tasks"],
                    task["weight"],
                    relative_weight,
                    holdings,
                )

        return holdings

    def handle_buy(self, task, holdings, relative_weight):
        asset = task["asset"]

        if holdings is False:
            return

        if asset == "COST":
            print("msft ya")
            holdings.clear()
            return True

        # Add the asset to holdings, if asset already exists add to existing asset weight
        if asset not in holdings:
            holdings[asset] = relative_weight
        else:
            holdings[asset] += relative_weight

    def handle_expression(self, date, task, weight, relative_weight, holdings):
        indicator1, indicator2 = get_indicator_names(task["conditions"])
        asset1_data, asset2_data = get_asset_datasets(self.dataset, task["conditions"])
        operator = task["conditions"]["operator"]
        value1 = get_value_by_date(asset1_data, date, indicator1)
        value2 = get_value_by_date(asset2_data, date, indicator2)

        if isnan(value1) or isnan(value2):
            holdings.clear()
            holdings = False

        if self.operators[operator](
            get_value_by_date(asset1_data, date, indicator1),
            get_value_by_date(asset2_data, date, indicator2),
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

    def get_backtest_errors(self, date):
        buy_condition_data = get_buy_and_condition_data(self.algorithm)

        # Dont forget to remove duplicates in buy condition data

        for data in buy_condition_data:

            # Type buys
            if "type" in data:
                if data["type"] == "buy":
                    asset = data["asset"]

                    self.handle_buy_errors(asset, date)

            # Indicators
            if "function" in data:
                asset = data["asset"]

                # Getting indicator name
                indicator = f"{data['function']} {data['period']}"

                self.handle_indicator_errors(asset, indicator, date)

    def handle_buy_errors(self, asset, date):
        # If assets data does not exist
        if self.dataset[asset] is None:
            self.error_tracker.add_asset_error(asset)

        # If assets data exists on current date
        if does_value_exist(self.dataset[asset], date):
            pass
        else:
            asset_available = get_first_value(self.dataset[asset])
            self.error_tracker.add_asset_error(asset, asset_available)

    def handle_indicator_errors(self, asset, indicator, date):
        # If assets data does not exist neither does indicators
        if self.dataset[asset] is None:
            self.error_tracker.add_asset_error(asset)
            self.error_tracker.add_indicator_error(asset, indicator)
            return

        # If assets data exists on current date indicators data exists aswell (could be nan)
        if does_value_exist(self.dataset[asset], date):

            # If indicator value is nan
            if isnan(get_value_by_date(self.dataset[asset], date, indicator)):
                first_date = get_date_of_first_non_nan_value(
                    self.dataset[asset], indicator
                )

                # If there is no first date (all indicator values are nan)
                if first_date is None:
                    self.error_tracker.add_indicator_error(asset, indicator)
                else:
                    self.error_tracker.add_indicator_error(asset, indicator, first_date)

        else:
            first_date = get_date_of_first_non_nan_value(self.dataset[asset], indicator)

            # If there is no first date (all indicator values are nan)
            if first_date is None:
                self.error_tracker.add_indicator_error(asset, indicator)
            else:
                self.error_tracker.add_indicator_error(asset, indicator, first_date)


data = build_dataset(sample_algo_request)

gg = Backtest(sample_algo_request, data)
# gg.ttt("2020-01-02")


gg.get_algorithm_errors("1992-01-02")
# print(gg.error_tracker.asset_errors)

print(gg.error_tracker.indicator_errors)
print(gg.error_tracker.asset_errors)
