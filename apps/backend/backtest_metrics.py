import performance_metrics
from utils.dataframe import build_dataframe_from_tuples
from functools import partial


class BacktestMetrics:

    def __init__(self, algorithm, portfolio_data):
        self.benchmarks = algorithm["benchmarks"]
        self.portfolio_value_data = portfolio_data["portfolio_values"]

        self.traded_dates = list(self.portfolio_value_data.keys())
        self.first_traded_date = self.traded_dates[0]
        self.last_traded_date = self.traded_dates[-1]

        self.portfolio_dataframe = self.build_portfolio_dataframe()

        self.performance_metrics = {
            "annualized_return": performance_metrics.get_annualized_return,
            "calmar_ratio": performance_metrics.get_calmar_ratio,
            "downside_deviation": performance_metrics.get_downside_deviation,
            "historical_cumulative_returns": performance_metrics.get_historical_cumulative_returns,
            "maximum_drawdown": performance_metrics.get_maximum_drawdown,
            "sharp_ratio": performance_metrics.get_sharp_ratio,
            "sortino_ratio": performance_metrics.get_sortino_ratio,
            "standard_deviation": performance_metrics.get_standard_deviation,
            "total_cumulative_return": performance_metrics.get_total_cumulative_return,
            "trailing_return_30day": partial(
                performance_metrics.get_trailing_return, days=30
            ),
            "trailing_return_60day": partial(
                performance_metrics.get_trailing_return, days=60
            ),
            "trailing_return_90day": partial(
                performance_metrics.get_trailing_return, days=90
            ),
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
            dataframe (df): Pandas dataframe.

        Returns:
            dict: Dictionary with performance metric names as keys, and performance
            metric values as values.
        """
        metrics = {}

        for metric_name, metric_function in self.performance_metrics.items():
            metrics[metric_name] = metric_function(
                dataframe, self.first_traded_date, self.last_traded_date
            )

        return metrics
