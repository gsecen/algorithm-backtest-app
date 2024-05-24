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
        self.trading_days = get_trading_days(
            algorithm["start_date"], algorithm["end_date"]
        )
        self.backtest_trading_dates = get_time_based_trading_dates(
            self.trading_days, self.trading_frequency
        )

        # self.trading_days = [
        #     "1995-01-03",
        #     "1998-01-02",
        #     "2008-01-03",
        #     "2018-01-02",
        #     "2021-01-04",
        # ]
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

    def calculate_holdings(self, date, tasks, weight, task_relative_weight, holdings):
        """Calculates the portfolio holdings for given date.

        Args:
            date (str): Date to get holdings for.
            tasks (dict): Tasks to iterate through.
            weight (int): Absolute weight of task
            task_relative_weight (float): Relative weight of task.
            holdings (dict): Current holdings.

        Returns:
            dict: Dictionary of assets as keys, and holdings for assets as values.
        """

        for index, task in enumerate(tasks):

            # Getting the relative weight for task
            relative_weight = calculate_task_weight(
                len(tasks), index, weight, task_relative_weight
            )

            if task["type"] == "buy":
                if self.handle_buy(date, task, relative_weight, holdings):
                    return None

            if task["type"] == "expression":

                if (
                    self.handle_expression(
                        date, task, weight, relative_weight, holdings
                    )
                    is None
                ):
                    return None

            if task["type"] == "instructions":

                if (
                    self.calculate_holdings(
                        date,
                        task["tasks"],
                        task["weight"],
                        relative_weight,
                        holdings,
                    )
                    is None
                ):
                    return None

        return holdings

    def handle_buy(self, date, task, relative_weight, holdings):
        """Handle type buys in calculate holdings. Will add assets to holdings dictionary.

        Args:
            date (str): Date to calculate holdings for.
            task (dict): Type buy task.
            holdings (dict): Current holdings.
            relative_weight (float): Relative weight of task.

        Returns:
            bool: True if error and algorithm cannot continue. False if no error.
        """
        asset = task["asset"]

        # If asset data is not available at date
        if not does_value_exist(self.dataset[asset], date):
            holdings.clear()
            return True

        # If there is no asset data
        if self.dataset[asset] is None:
            holdings.clear()
            return True

        # Add the asset to holdings, if asset already exists add to existing asset weight
        if asset not in holdings:
            holdings[asset] = relative_weight
        else:
            holdings[asset] += relative_weight

        return False

    def handle_expression(self, date, task, weight, relative_weight, holdings):

        indicator1, indicator2 = get_indicator_names(task["conditions"])
        asset1_data, asset2_data = get_asset_datasets(self.dataset, task["conditions"])
        operator = task["conditions"]["operator"]
        value1 = get_value_by_date(asset1_data, date, indicator1)
        value2 = get_value_by_date(asset2_data, date, indicator2)

        # If the assets indicators data does not exist at all
        if asset1_data is None or asset2_data is None:
            holdings.clear()
            return None

        # If the assets indicators data does not exist on date
        if not does_value_exist(asset1_data, date) or not does_value_exist(
            asset2_data, date
        ):
            holdings.clear()
            return None

        # If the assets indicators data exists but value is nan
        if isnan(value1) or isnan(value2):
            holdings.clear()
            return None

        # If indicator values for assets exist and are not nan
        # Actually calculate the type expression (if/else)
        if self.operators[operator](
            get_value_by_date(asset1_data, date, indicator1),
            get_value_by_date(asset2_data, date, indicator2),
        ):
            return self.calculate_holdings(
                date, task["true"], weight, relative_weight, holdings
            )
        else:
            return self.calculate_holdings(
                date, task["false"], weight, relative_weight, holdings
            )

    def get_historical_holdings(self):
        """Runs the algorithm through backtesting trading dates and keeps track of the holdings
        for each backtesting day.

        Returns:
            dict: Dictionary with dates as keys and holdings for that date as values.
        """
        historical_holdings = {}

        for date in self.backtest_trading_dates:

            # First relative weight will always be 1 because it is not nested in anything else
            holdings = self.calculate_holdings(
                date, self.algorithm["algorithm"]["tasks"], self.starting_weight, 1, {}
            )

            # If holdings is none there was an error in the algorithm
            if holdings is None:
                historical_holdings.clear()
            else:
                historical_holdings[date] = holdings

        return historical_holdings

    def get_backtest_errors(self):
        """Runs the algorithm and checks for issues"""
        buy_and_condition_data = get_buy_and_condition_data(self.algorithm)

        # Date which the algorithm will try to run on first
        starting_date = self.backtest_trading_dates[0]

        for data in buy_and_condition_data:

            # Type buys
            if "type" in data:
                if data["type"] == "buy":
                    asset = data["asset"]

                    self.handle_buy_errors(asset, starting_date)

            # Indicators for assets and series
            if "function" in data:
                if "asset" in data:
                    asset = data["asset"]

                    # Getting indicator name
                    indicator = f"{data['function']} {data['period']}"

                    self.handle_indicator_errors(
                        asset, indicator, starting_date, "asset"
                    )

                if "series" in data:
                    series = data["series"]

                    # Getting indicator name
                    indicator = f"{data['function']} {data['period']}"

                    self.handle_indicator_errors(
                        series, indicator, starting_date, "series"
                    )

    def handle_buy_errors(self, asset, date):
        """Handle the errors for type buy objects.

        Args:
            asset (str): Asset in type buy object.
            date (str): Date to check for issues with asset.
        """
        # If assets data does not exist
        if self.dataset[asset] is None:
            self.error_tracker.add_asset_error(asset)

        # If assets data exists on current date
        if does_value_exist(self.dataset[asset], date):
            pass
        else:
            asset_available = get_first_value(self.dataset[asset])
            self.error_tracker.add_asset_error(asset, asset_available)

    def handle_indicator_errors(self, asset, indicator, date, type):
        """Handle the errors for indicators. (Condition objects)

        Args:
            asset (str): Asset or series in condition object. (Asset or series the indicator is for)
            indicator (str): Indicator name.
            date (str): Date to check for issues with indicator data.
            type (str): Indicator is for asset or series. ("asset" or "series")
        """
        # If assets data does not exist neither does indicators
        if self.dataset[asset] is None:
            if type == "asset":
                self.error_tracker.add_asset_error(asset)
            if type == "series":
                self.error_tracker.add_series_error(asset)
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


# gg.get_backtest_errors("2010-06-29")
# print(gg.error_tracker.asset_errors)
# print(gg.error_tracker.indicator_errors)

gg.get_backtest_errors()
print(gg.error_tracker.asset_errors)
print(gg.error_tracker.indicator_errors)
print(gg.get_historical_holdings())
# print(
#     gg.calculate_holdings(
#         "2005-01-03",
#         gg.algorithm["algorithm"]["tasks"],
#         gg.algorithm["algorithm"]["weight"],
#         1,
#         {},
#     )
# )
