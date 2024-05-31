"""This module gets all the backtesting metrics"""

from functools import partial
import performance_metrics as pm
import comparative_metrics as cm
from utils.dataframe import build_dataframe_from_tuples


class BacktestMetrics:
    """This class gets the algorithms metric data. Performance metrics of algorithm and benchmarks.
    Comparative metrics of algorithm compared to benchmarks.
    """

    def __init__(self, algorithm, portfolio_data, dataset):
        self.dataset = dataset

        self.benchmarks = algorithm["benchmarks"]
        self.algorithm_name = algorithm["name"]
        self.portfolio_value_data = portfolio_data["portfolio_values"]

        self.portfolio_dataframe = self.build_portfolio_dataframe()

        traded_dates = list(self.portfolio_value_data.keys())
        self.first_traded_date = traded_dates[0]
        self.last_traded_date = traded_dates[-1]

        self.performance_metrics = {
            "annualized_return": pm.get_annualized_return,
            "calmar_ratio": pm.get_calmar_ratio,
            "downside_deviation": pm.get_downside_deviation,
            "annualized_downside_deviation": pm.get_annualized_downside_deviation,
            "historical_cumulative_returns": pm.get_historical_cumulative_returns,
            "maximum_drawdown": pm.get_maximum_drawdown,
            "sharp_ratio": pm.get_sharp_ratio,
            "sortino_ratio": pm.get_sortino_ratio,
            "standard_deviation": pm.get_standard_deviation,
            "annualized_standard_deviation": pm.get_annualized_standard_deviation,
            "total_cumulative_return": pm.get_total_cumulative_return,
            "trailing_return_30day": partial(pm.get_trailing_return, days=30),
            "trailing_return_60day": partial(pm.get_trailing_return, days=60),
            "trailing_return_90day": partial(pm.get_trailing_return, days=90),
        }

        self.comparative_metrics = {
            "beta": cm.get_beta,
            "coefficient_determination": cm.get_coefficient_determination,
            # "jenses_alpha": cm.get_jensens_alpha,
            "pearson_correlation": cm.get_pearson_correlation,
            "treynor_ratio": cm.get_treynor_ratio,
        }

    def build_portfolio_dataframe(self):
        """Builds the historical portfolio values data into pandas dataframe from dictionary so that it can be used
        in calculations.

        Returns:
            df: Pandas dataframe with dates and portfolio values data.
        """

        # The portfolio value data is dict of dates as keys and portfolio values as value
        portfolio_dates = self.portfolio_value_data.keys()
        portfolio_values = self.portfolio_value_data.values()

        # Building the dataframe
        dataframe = build_dataframe_from_tuples(
            (portfolio_dates, "Date"), (portfolio_values, "Open")
        )

        return dataframe

    def get_performance_metrics(self, dataframe):
        """Gets all the performance metrics of an asset or portfolio.

        Args:
            dataframe (df): Pandas dataframe containing assets or portfolios data.

        Returns:
            dict: Dictionary with performance metric names as keys, and performance
            metric values as values.
        """
        if dataframe is None:
            return None

        metrics = {}

        for metric_name, metric_function in self.performance_metrics.items():
            metrics[metric_name] = metric_function(
                dataframe, self.first_traded_date, self.last_traded_date
            )

        return metrics

    def get_comparative_metrics(self, dataframe1, dataframe2):
        """Gets all the comparative metrics of an asset or portfolio compared to another asset or portfolio.

        Args:
            dataframe1 (df): Pandas dataframe containing first assets or portfolios data.
            dataframe2 (df): Pandas dataframe containing second assets or portfolios data.

        Returns:
            dict: Dictionary of performance metric names as keys and their values as values.
        """
        if dataframe1 is None or dataframe2 is None:
            return None

        metrics = {}

        for metric_name, metric_function in self.comparative_metrics.items():
            metrics[metric_name] = metric_function(
                dataframe1, dataframe2, self.first_traded_date, self.last_traded_date
            )

        return metrics

    def get_all_metrics(self):
        """Gets all the comparative and performance metrics of all benchmarks and portfolio.

        Returns:
            dict: Dictionary of performance metric names as keys and their values as values, dictionary
            of comparative metric names as keys and their values as values.
        """
        metrics = {}
        metrics["performance_metrics"] = {}
        metrics["comparative_metrics"] = {}

        # Getting and adding algorithm performance metrics
        algorithm_performance_metrics = self.get_performance_metrics(
            self.portfolio_dataframe
        )
        metrics["performance_metrics"][
            self.algorithm_name
        ] = algorithm_performance_metrics

        # Adding initial investment and final value to algorithm performance metrics
        intial_investment = self.portfolio_value_data[self.first_traded_date]
        final_value = self.portfolio_value_data[self.last_traded_date]
        metrics["performance_metrics"][self.algorithm_name][
            "initial_investment"
        ] = intial_investment
        metrics["performance_metrics"][self.algorithm_name]["final_value"] = final_value

        # Getting all the benchmark metrics
        for asset in self.benchmarks:
            asset_df = self.dataset[asset]

            # Getting and adding performance metrics
            asset_performance_metrics = self.get_performance_metrics(asset_df)
            metrics["performance_metrics"][asset] = asset_performance_metrics

            # Getting and adding comparative metrics
            asset_comparative_metrics = self.get_comparative_metrics(
                self.portfolio_dataframe, asset_df
            )
            metrics["comparative_metrics"][asset] = asset_comparative_metrics

        return metrics
