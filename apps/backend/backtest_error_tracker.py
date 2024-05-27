from utils.algorithm import get_buy_and_condition_data
from utils.dataframe import (
    does_value_exist,
    get_first_value,
    get_value_by_date,
    get_date_of_first_non_nan_value,
)
from math import isnan


class BacktestErrorTracker:

    def __init__(self, algorithm, dataset, first_backtest_trading_date):

        self.algorithm = algorithm
        self.dataset = dataset
        self.first_backtest_trading_date = first_backtest_trading_date

        # Indicator data errors
        self.indicator_errors = []

        # Stock and asset price data errors
        self.asset_errors = []

        # Fred series data errors
        self.series_errors = []

    def add_asset_error(self, asset, date=None):
        """Adds asset issues from algorithm to asset errors list.

        Args:
            asset (str): Name of asset.
            date (str, optional): Date of when issue will be resolved. Defaults to None.
        """
        if date is None:
            error = f"{asset} not available."
        else:
            error = f"{asset} not available until {date}."

        if error in self.asset_errors:
            return

        self.asset_errors.append(error)

    def add_series_error(self, series, date=None):
        """Adds series issues from algorithm to series errors list.

        Args:
            series (str): Name of series.
            date (str, optional): Date of when issue will be resolved. Defaults to None.
        """
        if date is None:
            error = f"{series} not available."
        else:
            error = f"{series} not available until {date}."

        if error in self.series_errors:
            return

        self.series_errors.append(error)

    def add_indicator_error(self, asset, indicator, date=None):
        """Adds indicator issues from algorithm to indicator errors list.

        Args:
            asset (str): Name of asset or series.
            indicator (str): Name of indicator.
            date (str, optional): Date of when issue will be resolved. Defaults to None.
        """
        if date is None:
            error = f"{asset} {indicator} not available."
        else:
            error = f"{asset} {indicator} not available until {date}."

        if error in self.indicator_errors:
            return

        self.indicator_errors.append(error)

    def get_backtest_errors(self):
        """Runs the algorithm and checks for issues"""
        buy_and_condition_data = get_buy_and_condition_data(self.algorithm)

        # Date which the algorithm will try to run on first
        starting_date = self.first_backtest_trading_date

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
            self.add_asset_error(asset)

        # If assets data exists on current date
        if does_value_exist(self.dataset[asset], date):
            pass
        else:
            asset_available = get_first_value(self.dataset[asset])
            self.add_asset_error(asset, asset_available)

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
                self.add_asset_error(asset)
            if type == "series":
                self.add_series_error(asset)
            self.add_indicator_error(asset, indicator)
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
                    self.add_indicator_error(asset, indicator)
                else:
                    self.add_indicator_error(asset, indicator, first_date)

        else:
            first_date = get_date_of_first_non_nan_value(self.dataset[asset], indicator)

            # If there is no first date (all indicator values are nan)
            if first_date is None:
                self.add_indicator_error(asset, indicator)
            else:
                self.add_indicator_error(asset, indicator, first_date)
