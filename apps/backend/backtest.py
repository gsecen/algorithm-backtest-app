"""This module backtests the algorithm"""

import operator
from math import isnan

from utils.algorithm import (
    is_holdings_above_threshold,
)
from utils.time import (
    get_trading_days,
    get_time_based_trading_dates,
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

from backtest_error_tracker import BacktestErrorTracker
from backtest_metrics import BacktestMetrics


class Backtest:
    """This class backtests the algorithm and gets the historical data. Data such as
    portfolio historical values and weights.
    """

    def __init__(self, algorithm, dataset):
        self.dataset = dataset
        self.algorithm = algorithm

        self.trading_frequency = algorithm["trading_frequency"]
        self.trading_threshold = algorithm["trading_threshold"]
        self.starting_task = algorithm["algorithm"]["tasks"]
        self.starting_weight = algorithm["algorithm"]["weight"]

        self.trading_days = get_trading_days(
            algorithm["start_date"], algorithm["end_date"]
        )

        self.initial_investment = 100000

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

        # If there is no asset data
        if self.dataset[asset] is None:
            holdings.clear()
            return True

        # If asset data is not available at date
        if not does_value_exist(self.dataset[asset], date):
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

        # Getting the backtesting trading days
        time_based_trading_dates = get_time_based_trading_dates(
            self.trading_days, self.trading_frequency
        )

        for date in self.trading_days:

            # If it is a date to trade
            if date in time_based_trading_dates:

                # If there are currently holdings calculate the portfolio value
                if latest_holdings:
                    portfolio_value = self.calculate_portfolio_value(
                        date, lastest_asset_quantities
                    )
                    portfolio_value_tracker = portfolio_value
                    historical_portfolio_values[date] = portfolio_value
                else:
                    historical_portfolio_values[date] = (
                        portfolio_value_tracker  # Adding the inital investment on first traded day
                    )

                holdings = self.calculate_holdings(
                    date,
                    self.starting_task,
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
            "traded_dates": historical_trading_dates,
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
                self.starting_task,
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
                    self.trading_threshold,
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
                historical_portfolio_values[date] = (
                    portfolio_value_tracker  # Adding the inital investment on first traded day
                )

        return {
            "traded_dates": historical_trading_dates,
            "portfolio_values": historical_portfolio_values,
            "asset_weights": historical_asset_weights,
        }

    def get_historical_portfolio_data(self):
        """Gets the historical traded dates, portfolio values, and asset weights for every trading day in
        time based or threshold based algorithm.

        Returns:
            dict: Dictionary of list of traded dates, dictionary with dates as keys and portfolio values as values,
            dictionary of dates as keys and asset weights as values.
        """

        # If threshold is 0 algorithm uses time based trading
        if self.trading_threshold == 0:
            return self.get_time_based_historical_portfolio_data()

        return self.get_threshold_based_historical_portfolio_data()

    def backtest_algorithm(self):
        """Backtests the algorithm and gets all the historical performance metrics, comparative metrics,
        and algorithm issues.

        Returns:
            dict: Dictionary of metrics and dictionary of issues.
        """

        # Getting algorithm traded dates, values, weights, and errors
        algorithm_dates_values_weights = self.get_historical_portfolio_data()
        errors = BacktestErrorTracker(
            self.algorithm,
            self.dataset,
            self.trading_days[0],  # first day algorithm trys to run on
        )

        # If there is any portfolio data (algorithm ran successfully at least once)
        if algorithm_dates_values_weights["traded_dates"]:

            # Get the metrics
            metrics = BacktestMetrics(
                self.algorithm, algorithm_dates_values_weights, self.dataset
            )

            return {
                "metrics": metrics.get_all_metrics(),
                "issues": errors.get_backtest_errors(),
            }
        else:

            # Cannot get metrics if there is no algorithm portfolio data
            return {"metrics": None, "issues": errors.get_backtest_errors()}
