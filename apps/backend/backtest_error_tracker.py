class BacktestErrorTracker:

    def __init__(self):

        # Indicator data errors
        self.indicator_errors = []

        # Stock and asset price data errors
        self.asset_errors = []

        # Fred series data errors
        self.series_errors = []

    def add_asset_error(self, asset, date=None):
        if date is None:
            pass
        else:
            error = f"{asset} close price data not available until {date}"

            self.asset_errors.append(error)
