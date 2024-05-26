class BacktestErrorTracker:

    def __init__(self):

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
