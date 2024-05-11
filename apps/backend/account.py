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

something = {}


def calculate_stock_quantities():
    for date, value in example.items():
        # print(key)
        something[date] = {}
        for asset, weight in value.items():
            shares = (balance * weight) / prices[asset][date]
            # print(f"{asset} Shares: {shares}")
            something[date][asset] = shares


print(something)
