from utils.algorithm import compare_holdings

current_holdings = {
    "AAPL": 0.5,
    "NVDA": 0.1,
    # "TSLA": 0.1,
    # "MSFT": 0.3,
}

new_holdings = {
    "AAPL": 0.5,
    "NVDA": 0.5,
    # "FORD": 0.1,
    # "MSFT": 0.2,
}

print(compare_holdings(current_holdings, new_holdings))

prices = {
    "AAPL": {
        "2020-01-01": 10,
        "2020-01-02": 20,
        "2020-01-03": 30,
        "2020-01-04": 40,
        "2020-01-05": 50,
        "2020-01-06": 60,
    },
    "NVDA": {
        "2020-01-01": 10,
        "2020-01-02": 20,
        "2020-01-03": 30,
        "2020-01-04": 40,
        "2020-01-05": 50,
        "2020-01-06": 60,
    },
}


balance = 100000
example = {
    "2020-01-01": current_holdings,
    "2020-01-02": current_holdings,
    "2020-01-03": current_holdings,
    "2020-01-04": new_holdings,
    "2020-01-05": new_holdings,
    "2020-01-06": new_holdings,
}


def calculate_stock_quantities():
    something = {}

    for date, value in example.items():
        # print(key)
        something[date] = {}
        for asset, weight in value.items():
            shares = (balance * weight) / prices[asset][date]
            # print(f"{asset} Shares: {shares}")
            something[date][asset] = shares

    return something


stock_quantites = {
    "2020-01-01": {"AAPL": 5000.0, "NVDA": 1000.0},
    "2020-01-02": {"AAPL": 2500.0, "NVDA": 500.0},
    "2020-01-03": {"AAPL": 1666.6666666666667, "NVDA": 333.3333333333333},
    "2020-01-04": {"AAPL": 1250.0, "NVDA": 1250.0},
    "2020-01-05": {"AAPL": 1000.0, "NVDA": 1000.0},
    "2020-01-06": {"AAPL": 833.3333333333334, "NVDA": 833.3333333333334},
}


def calculate_portfolio_asset_weights():
    gg = {}

    for date, value in stock_quantites.items():
        gg[date] = {}
        for asset, quantity in value.items():
            total_stock_value = quantity * prices[asset][date]
            stock_weight = total_stock_value / balance
            gg[date][asset] = stock_weight

    return gg


def calculate_portfolio_value():
    gg = {}

    for date, value in stock_quantites.items():
        # gg[date] = {}
        portfolio_value = 0
        for asset, quantity in value.items():
            total_stock_value = quantity * prices[asset][date]
            portfolio_value += total_stock_value
            # stock_weight = total_stock_value / balance
            # gg[date][asset] = stock_weight

        # print(portfolio_value)
        gg[date] = portfolio_value

    return gg


print(calculate_portfolio_asset_weights())


print(calculate_stock_quantities())

print(calculate_portfolio_value())
