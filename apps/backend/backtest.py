from utils.algorithm import (
    sample_algo_request,
    sample_algo_requestv2,
    is_holdings_above_threshold,
)
from utils.time import (
    get_trading_days,
    get_time_based_trading_dates,
    copy_date_data_to_new_dates,
    get_dates_after_date,
)
from utils.algorithm import (
    calculate_task_weight,
    get_indicator_names,
    get_asset_datasets,
)
from utils.dataframe import (
    get_value_by_date,
    does_value_exist,
)

from algorithm.dataset_builder import build_dataset

import pandas as pd
import operator
from math import isnan


class Backtest:

    def __init__(self, algorithm, dataset):
        self.algorithm = algorithm
        self.dataset = dataset

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

        self.initial_investment = 100000

        self.threshold = 0.03

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
            weight (int/float): Absolute weight of task
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
            holdings (dict): Current holdings.

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
        """Handle type expression in calculate holdings.

        Args:
            date (str): Date to calculate holdings for.
            task (dict): Type expression task.
            weight (int/float): Absolute weight of task
            relative_weight (float): Relative weight of task.
            holdings (dict): Current holdings.

        Returns:
            None: None if error and algorithm cannot continue.
        """

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

    def get_time_based_historical_portfolio_data(self):
        """Gets the historical traded dates, portfolio values, and asset weights for every trading day in
        time based algorithm.

        Returns:
            dict: Dictionary of list of traded dates, dictionary with dates as keys and portfolio values as values,
            dictionary of dates as keys and asset weights as values.
        """
        historical_trading_dates = []
        historical_portfolio_values = {}
        historical_asset_weights = {}
        portfolio_value_tracker = self.initial_investment

        # Tracks the very latest asset quantities and holdings used for calculations
        lastest_asset_quantities = {}
        latest_holdings = {}

        for date in self.trading_days:

            # If it is a date to trade
            if date in self.backtest_trading_dates:

                # If there are currently holdings calculate the portfolio value
                if latest_holdings:
                    portfolio_value = self.calculate_portfolio_value(
                        date, lastest_asset_quantities
                    )
                    portfolio_value_tracker = portfolio_value
                    historical_portfolio_values[date] = portfolio_value

                holdings = self.calculate_holdings(
                    date,
                    self.algorithm["algorithm"]["tasks"],
                    self.starting_weight,
                    1,
                    {},
                )

                # If holdings returned none there was an error in algorithm so reset everything
                if holdings is None:
                    latest_holdings.clear()
                    lastest_asset_quantities.clear()
                    historical_portfolio_values.clear()
                    historical_asset_weights.clear()
                    historical_trading_dates.clear()
                    portfolio_value_tracker = self.initial_investment
                else:

                    # Calculating and adding historical values
                    latest_holdings = holdings
                    asset_quantities = self.calculate_portfolio_asset_quantities(
                        date, holdings, portfolio_value_tracker
                    )
                    lastest_asset_quantities = asset_quantities
                    asset_weights = self.calculate_portfolio_weights(
                        date, asset_quantities, portfolio_value_tracker
                    )
                    historical_asset_weights[date] = asset_weights
                    historical_trading_dates.append(date)

            else:

                # If there are holdings calculate and add historical values
                if latest_holdings:
                    portfolio_value = self.calculate_portfolio_value(
                        date, lastest_asset_quantities
                    )
                    portfolio_value_tracker = portfolio_value
                    asset_weights = self.calculate_portfolio_weights(
                        date, lastest_asset_quantities, portfolio_value
                    )
                    historical_portfolio_values[date] = portfolio_value
                    historical_asset_weights[date] = asset_weights

        return {
            "trading_dates": historical_trading_dates,
            "portfolio_values": historical_portfolio_values,
            "asset_weights": historical_asset_weights,
        }

    def get_threshold_based_historical_portfolio_data(self):
        """Gets the historical traded dates, portfolio values, and asset weights for every trading day in
        threshold based algorithm.

        Returns:
            dict: Dictionary of list of traded dates, dictionary with dates as keys and portfolio values as values,
            dictionary of dates as keys and asset weights as values.
        """
        historical_trading_dates = []
        historical_portfolio_values = {}
        historical_asset_weights = {}
        portfolio_value_tracker = self.initial_investment

        # Tracks the very latest asset quantities and holdings used for calculations
        lastest_asset_quantities = {}
        latest_holdings = {}

        for date in self.trading_days:

            # For threshold based trading will have to calculate holdings for every trading day
            holdings = self.calculate_holdings(
                date,
                self.algorithm["algorithm"]["tasks"],
                self.starting_weight,
                1,
                {},
            )

            # If holdings returned none there was an error in algorithm so reset everything
            # and skip the rest of the logic for the trading day
            if holdings is None:
                latest_holdings.clear()
                lastest_asset_quantities.clear()
                historical_portfolio_values.clear()
                historical_asset_weights.clear()
                historical_trading_dates.clear()
                portfolio_value_tracker = self.initial_investment
                continue

            # If there are currently holdings
            if latest_holdings:

                # Calculate and adding the portfolio value and weights
                portfolio_value = self.calculate_portfolio_value(
                    date, lastest_asset_quantities
                )
                portfolio_value_tracker = portfolio_value
                historical_portfolio_values[date] = portfolio_value
                portfolio_weights = self.calculate_portfolio_weights(
                    date, lastest_asset_quantities, portfolio_value
                )
                historical_asset_weights[date] = portfolio_weights

                # If the latest holdings compared to the current weights exceed the threshold
                if is_holdings_above_threshold(
                    latest_holdings,
                    portfolio_weights,
                    self.threshold,
                ):

                    # Calculating and adding historical values
                    latest_holdings = holdings
                    asset_quantities = self.calculate_portfolio_asset_quantities(
                        date, holdings, portfolio_value_tracker
                    )
                    lastest_asset_quantities = asset_quantities
                    portfolio_weights = self.calculate_portfolio_weights(
                        date, asset_quantities, portfolio_value_tracker
                    )
                    historical_asset_weights[date] = portfolio_weights
                    historical_trading_dates.append(date)

            # There are no holdings so this is first traded day
            else:

                # Calculating and adding historical values
                latest_holdings = holdings
                asset_quantities = self.calculate_portfolio_asset_quantities(
                    date, holdings, portfolio_value_tracker
                )
                lastest_asset_quantities = asset_quantities
                asset_weights = self.calculate_portfolio_weights(
                    date, asset_quantities, portfolio_value_tracker
                )
                historical_asset_weights[date] = asset_weights
                historical_trading_dates.append(date)

        return {
            "trading_dates": historical_trading_dates,
            "portfolio_values": historical_portfolio_values,
            "asset_weights": historical_asset_weights,
        }

    def get_threshold_based_holdings(self):
        historical_holdings = {}

        # Must keep track of latest asset quantities and portfolio value
        lastest_quantities = {}
        portfolio_value_tracker = self.initial_investment

        for date in self.trading_days:

            # If there are holdings
            if historical_holdings:

                # Updating the portfolios current value
                portfolio_value = self.calculate_portfolio_value(
                    date, lastest_quantities
                )
                portfolio_value_tracker = portfolio_value

                # Get portfolio weights
                portfolio_weights = self.calculate_portfolio_weights(
                    date, lastest_quantities, portfolio_value_tracker
                )

                # If the current weights compared to latest holdings exceed the threshold
                if is_holdings_above_threshold(
                    historical_holdings[list(historical_holdings)[-1]],
                    portfolio_weights,
                    self.threshold,
                ):

                    # First relative weight will always be 1 because it is not nested in anything else
                    holdings = self.calculate_holdings(
                        date,
                        self.algorithm["algorithm"]["tasks"],
                        self.starting_weight,
                        1,
                        {},
                    )

                    # If holdings is none there was an error in the algorithm
                    if holdings is None:
                        historical_holdings.clear()
                        lastest_quantities.clear()
                        portfolio_value_tracker = self.initial_investment
                    else:
                        historical_holdings[date] = holdings
                        asset_quantities = self.calculate_portfolio_asset_quantities(
                            date, holdings, portfolio_value_tracker
                        )
                        lastest_quantities = asset_quantities

            else:

                # First relative weight will always be 1 because it is not nested in anything else
                holdings = self.calculate_holdings(
                    date,
                    self.algorithm["algorithm"]["tasks"],
                    self.starting_weight,
                    1,
                    {},
                )

                # If holdings is none there was an error in the algorithm
                if holdings is None:
                    historical_holdings.clear()
                    lastest_quantities.clear()
                    portfolio_value_tracker = self.initial_investment
                else:
                    historical_holdings[date] = holdings
                    asset_quantities = self.calculate_portfolio_asset_quantities(
                        date, holdings, portfolio_value_tracker
                    )
                    lastest_quantities = asset_quantities

        return historical_holdings

    def calculate_portfolio_asset_quantities(self, date, holdings, portfolio_value):
        """Calculates the portfolio asset quantities on specified date based off balance and what the
        holdings (asset weights) are.

        Args:
            date (str): Date to calculate portfolio assets quantities for.
            holdings (dict): Holdings (asset weights).

        Returns:
            dict: Dictionary with assets as keys and asset quantities as values.
        """
        quantities = {}
        for asset, weight in holdings.items():

            # Calculating shares based on balance and weight
            asset_price = get_value_by_date(self.dataset[asset], date, "Open")
            shares = (portfolio_value * weight) / asset_price

            if asset in quantities:
                quantities[asset] += shares
            else:
                quantities[asset] = shares

        return quantities

    def calculate_portfolio_value(self, date, asset_quantities):
        """Calculates the portfolio value on specified date based off of asset quantities.

        Args:
            date (str): Date to calculate portfolio for.
            asset_quantities (dict): Assets and their quantities.

        Returns:
            float/int: Portfolio value.
        """
        portfolio_value = 0
        for asset, quantity in asset_quantities.items():

            # Calculating the total asset value and adding it to portfolio value
            asset_price = get_value_by_date(self.dataset[asset], date, "Open")
            total_asset_value = quantity * asset_price
            portfolio_value += total_asset_value

        return portfolio_value

    def calculate_portfolio_weights(self, date, asset_quantities, portfolio_value):
        """Calculates the portfolio asset weights on a specified date based off of
        asset quantities and portfolio value.

        Args:
            date (str): Date to calculate asset weights for.
            asset_quantities (dict): Asset quantities.
            portfolio_value (float): Portfolio value.

        Returns:
            dict: Dictionary with dates as keys and asset weights as values.
        """
        asset_weights = {}

        for asset, quantity in asset_quantities.items():

            # Calculating asset weight based on asset value and portfolio value
            asset_price = get_value_by_date(self.dataset[asset], date, "Open")
            total_asset_value = quantity * asset_price
            asset_weight = total_asset_value / portfolio_value

            # Adding asset weight as a decimal
            asset_weights[asset] = asset_weight

        return asset_weights

    def get_historical_portfolio_asset_quantities(self, historical_holdings):
        """Gets the historical asset quantities for each backtesting trading day.
        (same days as historical holdings)

        Args:
            historical_holdings (dict): Historical holdings.

        Returns:
            dict: Dicionary with dates as keys and asset quantities for that date as values.
        """
        asset_quantities = {}

        portfolio_value = self.initial_investment
        for index, date in enumerate(historical_holdings):
            holdings = historical_holdings[date]

            # If very first trading day
            if index == 0:
                asset_quantities[date] = self.calculate_portfolio_asset_quantities(
                    date, holdings, portfolio_value
                )
            else:

                # Getting date of previous asset quantities
                stock_quantities_list = list(asset_quantities)
                last_date = stock_quantities_list[index - 1]

                # Getting the previous asset quantities
                previous_quantities = asset_quantities[last_date]

                # Calculating and updating the new portfolio value
                new_portfolio_value = self.calculate_portfolio_value(
                    date, previous_quantities
                )
                previous_quantities = new_portfolio_value

                asset_quantities[date] = self.calculate_portfolio_asset_quantities(
                    date, holdings, new_portfolio_value
                )

        return asset_quantities

    def get_historical_portfolio_values(self, historical_asset_quantities):
        """Gets the historical portfolio values for each trading day no matter the timeframe.

        Args:
            historical_asset_quantities (dict): Historical asset quantities.

        Returns:
            dict: Dictionary with dates as keys and portfolio value on that date as values.
        """

        # Getting all trading days which there are holdings for no matter timeframe
        first_traded_date = list(historical_asset_quantities)[0]
        days_with_holdings = get_dates_after_date(self.trading_days, first_traded_date)

        # Get asset quantities for every trading day no matter timeframe
        # Example: Timeframe is quarterly, only 4 days traded of year, get what the asset quantities are
        # for every single trading day
        historical_asset_quantities = copy_date_data_to_new_dates(
            historical_asset_quantities, days_with_holdings
        )

        historical_portforlio_values = {}

        for date, quantities in historical_asset_quantities.items():

            # Calculating and adding the portfolio value for date
            portfolio_value = self.calculate_portfolio_value(date, quantities)
            historical_portforlio_values[date] = portfolio_value

        return historical_portforlio_values

    def get_historical_portfolio_weights(
        self, historical_asset_quantities, historical_portfolio_values
    ):
        """Gets the historical portfolio weights for each trading day no matter the timeframe.

        Args:
            historical_asset_quantities (dict): Historical asset quantities.
            historical_portfolio_values (dict): Historical portfolio values.

        Returns:
            dict: Dictionary with dates as keys and portfolio weights on that date as values.
        """
        # Getting all trading days which there are holdings for no matter timeframe
        first_traded_date = list(historical_asset_quantities)[0]
        days_with_holdings = get_dates_after_date(self.trading_days, first_traded_date)

        # Get asset quantities for every trading day no matter timeframe
        # Example: Timeframe is quarterly, only 4 days traded of year, get what the asset quantities are
        # for every single trading day
        historical_asset_quantities = copy_date_data_to_new_dates(
            historical_asset_quantities, days_with_holdings
        )

        historical_portforlio_weights = {}

        for date, quantities in historical_asset_quantities.items():

            # Calculating and adding the portfolio asset weights for date
            portfolio_value = historical_portfolio_values[date]
            asset_weights = self.calculate_portfolio_weights(
                date, quantities, portfolio_value
            )
            historical_portforlio_weights[date] = asset_weights

        return historical_portforlio_weights

    def get_hisorical_portfolio_values_weights(self, historical_asset_quantities):
        """Gets the historical portfolio values and weights for each trading day no matter the timeframe.

        Args:
            historical_asset_quantities (dict): Historical asset quantities.

        Returns:
            tuple: Dictionary with dates as keys and portfolio value on that date as values, dictionary with
            dates as keys and portfolio weights on that date as values.
        """
        # Getting all trading days which there are holdings for no matter timeframe
        first_traded_date = list(historical_asset_quantities)[0]
        days_with_holdings = get_dates_after_date(self.trading_days, first_traded_date)

        # Get asset quantities for every trading day no matter timeframe
        # Example: Timeframe is quarterly, only 4 days traded of year, get what the asset quantities are
        # for every single trading day
        historical_asset_quantities = copy_date_data_to_new_dates(
            historical_asset_quantities, days_with_holdings
        )

        historical_portforlio_values = {}
        historical_portfolio_weights = {}

        for date, quantities in historical_asset_quantities.items():

            # Calculating the portfolio value for date
            portfolio_value = self.calculate_portfolio_value(date, quantities)

            # Calculating the portfolio weights for date
            portfolio_weights = self.calculate_portfolio_weights(
                date, quantities, portfolio_value
            )

            historical_portforlio_values[date] = portfolio_value
            historical_portfolio_weights[date] = portfolio_weights

        return historical_portforlio_values, historical_portfolio_weights

    def update_portfolio_value(self, new_value):
        """Update class portfolio value.

        Args:
            new_value (int/float): Value you want class portfolio value to be
        """
        self.initial_investment = new_value


# osio
data = build_dataset(sample_algo_requestv2)

gg = Backtest(sample_algo_requestv2, data)
# gg.ttt("2020-01-02")


# gg.get_backtest_errors("2010-06-29")
# print(gg.error_tracker.asset_errors)
# print(gg.error_tracker.indicator_errors)

# gg.get_backtest_errors()
# print(gg.error_tracker.asset_errors)
# print(gg.error_tracker.indicator_errors)

# ss = gg.get_historical_holdings()
# zz = gg.get_historical_portfolio_asset_quantities(ss)

# print(gg.get_threshold_based_holdings())

# print(zz)
# from backtest_error_tracker import BacktestErrorTracker

# fff = BacktestErrorTracker(sample_algo_request, data, gg.backtest_trading_dates[0])
# fff.get_backtest_errors()
# print(fff.indicator_errors)
# print(fff.asset_errors)

# print(gg.get_historical_portfolio_values(zz))
# print(gg.get_time_based_historical_portfolio_data())
# print(gg.get_threshold_based_historical_portfolio_data()["asset_weights"])

# print(
#     gg.calculate_holdings(
#         "2005-01-03",
#         gg.algorithm["algorithm"]["tasks"],
#         gg.algorithm["algorithm"]["weight"],
#         1,
#         {},
#     )
# )
