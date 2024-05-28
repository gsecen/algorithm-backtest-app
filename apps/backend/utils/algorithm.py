"""This module helps with all algorithm related functions"""

# Will all make more sense once UI is done then you can visually see the structure of algoirithm


# Things to note:
# Type buy is the purchase of an asset
# Type expression is an if else statement
# Type instructions is anytime you want a new weight or want to branch off (will make more sense soon)
sample_algo_request = {
    "start_date": "2010-01-01",
    "end_date": "2021-01-01",
    "name": "test algo",
    "benchmarks": ["NVDA", "SPY"],
    "trading_frequency": "annually",  # Can be daily, weekly, monthly, quarterly, annually.
    "algorithm": {
        "type": "instructions",
        "weight": 1,
        "tasks": [
            {"type": "buy", "asset": "MSFT"},
            {
                "type": "instructions",
                "weight": [0.75, 0.25],
                "tasks": [
                    {"type": "buy", "asset": "AAPL"},
                    {"type": "buy", "asset": "MMM"},
                ],
            },
            {
                "type": "instructions",
                "weight": 1,
                "tasks": [
                    {
                        "type": "expression",
                        "conditions": {
                            "operator": "<",
                            "condition1": {
                                "function": "sma",
                                "period": 2,
                                "asset": "AAPL",
                            },
                            "condition2": {
                                "function": "sma",
                                "asset": "MSFT",
                                "period": 2,
                            },
                        },
                        "true": [
                            {"type": "buy", "asset": "MA"},
                            {
                                "type": "instructions",
                                "weight": 1,
                                "tasks": [
                                    {
                                        "type": "expression",
                                        "conditions": {
                                            "operator": "<",
                                            "condition1": {
                                                "function": "sma",
                                                "asset": "AAPL",
                                                "period": 2,
                                            },
                                            "condition2": {
                                                "function": "sma",
                                                "asset": "NVDA",
                                                "period": 2,
                                            },
                                        },
                                        "true": [
                                            {"type": "buy", "asset": "COST"},
                                            {"type": "buy", "asset": "NVDA"},
                                        ],
                                        "false": [
                                            {"type": "buy", "asset": "ADBE"},
                                            {"type": "buy", "asset": "AMZN"},
                                        ],
                                    }
                                ],
                            },
                        ],
                        "false": [
                            {"type": "buy", "asset": "V"},
                        ],
                    }
                ],
            },
        ],
    },
}


# The absolute weight is the weight of the following tasks.
# Example is weight:1 or weight:[0.5, 0.25, 0.25]
# Even though the weight is weight:1 or weight:[0.5, 0.25, 0.25], the actual weight
# of the task may not be 0.5. This is because weights can be nested inside each other.
# The actual value/weight of the task is its relative weight.
sample_algo_requestv2 = {
    "start_date": "2010-01-01",
    "end_date": "2021-01-01",
    "name": "test algo",
    "benchmarks": ["NVDA", "SPY"],
    "trading_frequency": "annually",  # Can be daily, weekly, monthly, quarterly, annually.
    "algorithm": {
        "type": "instructions",
        "weight": 1,
        "tasks": [
            {"type": "buy", "asset": "AAPL"},
            {"type": "buy", "asset": "MSFT"},
        ],
    },
}


def calculate_task_weight(tasks_length, task_index, weight, relative_weight):
    """Calculates the relative task weight.

    Args:
        tasks_length (int): Number of tasks.
        task_index (int): Task index you want want relative weight for.
        weight (list/int): Absolute weight for tasks.
        relative_weight (float): Current relative weight for tasks.

    Returns:
        float: Relative weight for task.
    """
    # Equal weight amongst tasks
    if weight == 1:
        return relative_weight / tasks_length
    # Specified weights
    else:
        return weight[task_index] * relative_weight


def get_buy_and_condition_data(algorithm):
    """Gets all the type buy and condition objects in algorithm.

    Args:
        algorithm (dict): Entire algorithm.

    Returns:
        list: List of type buy and condition objects.
    """

    data = []

    def iterate_tasks_add_data(tasks):
        """Iterates through all tasks(and nested tasks) and adds the type buy and condition objects to data list.

        Args:
            tasks (list): List of task objects.
        """
        for task in tasks:
            if task["type"] == "buy":
                data.append(task)

            if task["type"] == "expression":
                data.append(task["conditions"]["condition1"])
                data.append(task["conditions"]["condition2"])
                iterate_tasks_add_data(task["true"])
                iterate_tasks_add_data(task["false"])

            if task["type"] == "instructions":
                iterate_tasks_add_data(task["tasks"])

    iterate_tasks_add_data(algorithm["algorithm"]["tasks"])

    return data


def get_benchmark_data(algorithm):
    """Gets the benchmarks in algorithm and puts them into {asset:benchmark} objects
    to be used in building dataset.

    Args:
        algorithm (dict): Entire algorithm.

    Returns:
        list: List of benchmark objects.
    """
    data = []

    benchmarks = algorithm["benchmarks"]

    for asset in benchmarks:
        data.append({"asset": asset})

    return data


# Rough function which will iterate through all tasks in algorithm and keep track of weights
def iterate_tasks(tasks, weight, relative_weight):

    for index, task in enumerate(tasks):
        # Getting the relative weight for task
        task_relative_weight = calculate_task_weight(
            len(tasks), index, weight, relative_weight
        )

        if task["type"] == "buy":
            print(task)
            print(task_relative_weight)

        if task["type"] == "expression":
            iterate_tasks(task["true"], weight, task_relative_weight)
            iterate_tasks(task["false"], weight, task_relative_weight)

        if task["type"] == "instructions":
            iterate_tasks(task["tasks"], task["weight"], task_relative_weight)


def test():
    starting_weight = sample_algo_request["algorithm"]["weight"]
    # Relative weight argument will always be 1 at the start
    iterate_tasks(sample_algo_request["algorithm"], starting_weight, 1)


# test()


current_holdings = {"AAPL": 0.3, "MSFT": 0.25, "TSLA": 0.1, "NVDA": 0.2, "gg": 23}

new_holdings2 = {
    "AAPL": 0.5,
    "AMZN": 0.10,
    "TSLA": 0.10,
    "NVDA": 0.10,
    "FORD": 0.2,
    "gg": 20,
    "ff": 0.5,
}


def compare_holdings(old_holdings, new_holdings):
    """Gets the difference of asset weights and new assets between old and new holdings.

    Args:
        old_holdings (dict): Old holdings.
        new_holdings (dict): New holdings.

    Returns:
        dict: Dictionary of differences of asset weights and new assets.
    """
    differences = {}
    for key in old_holdings.keys():
        if key in new_holdings.keys():

            # If the same asset is in old and new holdings calcualte difference in weights
            difference = new_holdings[key] - old_holdings[key]
            # If difference in weights in 0 the asset has the same weight in old and new holdings
            if difference != 0:
                differences[key] = new_holdings[key] - old_holdings[key]

        else:

            # If asset in old holdings is no longer in the new holdings make it negative because the entire holding was removed
            differences[key] = -old_holdings[key]

    for key in new_holdings.keys():
        if key not in old_holdings.keys():

            # If an asset is in new holdings which was not in old holdings
            differences[key] = new_holdings[key]

    return differences


def is_holdings_above_threshold(old_holdings, new_holdings, threshold):
    """Checks if the total differences in holdings differ by the threshold.

    Args:
        old_holdings (dict): Old holdings.
        new_holdings (dict): New holdings.
        threshold (float/int): The value to check if any of the holdings differences are above.

    Returns:
        bool: True if the total differences in holdings differ by the threshold. False if the total differencs
        in holdings do not differ by the threshold.
    """

    # Getting the total difference between assets in holdings
    holdings_differences = compare_holdings(old_holdings, new_holdings)
    total_difference = sum((abs(value) for value in holdings_differences.values()))

    if total_difference > threshold:
        return True
    return False


# print(is_holdings_above_threshold(new_holdings2, current_holdings, 0.1))

old_holdings = {"AAPL": 500, "NVDA": 1000, "AMZN": 200, "TSLA": 25.34, "FORD": 300}
new_holdings = {
    "AAPL": 250,
    "NVDA": 1500,
    "AMZN": 200,
    "TSLA": 20.348,
    "1": 923,
    "2": 2384,
    "2343": 1,
    "1212": 120.129,
}


def calculate_buy_sell_quantities(old_holdings, new_holdings):
    """Compares old and new stock holdings. Calculates how much quantity of each asset was bought or sold.

    Args:
        old_holdings (dict): Old holdings.
        new_holdings (dict): New holdings.

    Returns:
        dict: Dictionary of assets as keys and how much was bought or sold as values.
    """
    quantities = {}
    for asset, quantity in old_holdings.items():
        if asset in new_holdings:

            # If the same asset is in old and new holdings calcualte difference in quantities
            difference = new_holdings[asset] - quantity

            # If difference in quantities is 0 the asset has the same quantity in old and new holdings
            if difference != 0:
                quantities[asset] = new_holdings[asset] - quantity

        else:

            # If asset in old holdings is no longer in the new holdings make it negative because the entire holding was sold
            quantities[asset] = -quantity

    for asset, quantity in new_holdings.items():

        # If an asset is in new holdings which was not in old holdings
        if asset not in old_holdings:
            quantities[asset] = quantity

    return quantities


# print(calculate_buy_sell_quantities(old_holdings, new_holdings))


example_condtions = {
    "conditions": {
        "operator": "<",
        "condition1": {
            "function": "sma",
            "period": 8,
            "asset": "AAPL",
        },
        "condition2": {
            "function": "sma",
            "asset": "MSFT",
            "period": 2,
        },
    },
}


def get_indicator_names(conditions):
    """Gets the names of indicators in algorithm condition.

    Args:
        conditions (dict): Condition object in algoirthm.

    Returns:
        tuple: Name of first condition indicator, name of second condition indicator.
    """
    indicator1_function = conditions["condition1"]["function"]
    indicator1_period = conditions["condition1"]["period"]
    indicator2_function = conditions["condition2"]["function"]
    indicator2_period = conditions["condition2"]["period"]

    indicator1_name = f"{indicator1_function} {indicator1_period}"
    indicator2_name = f"{indicator2_function} {indicator2_period}"

    return indicator1_name, indicator2_name


def get_asset_names(conditions):
    """Gets the names of assets in algorithm condition.

    Args:
        conditions (dict): Condition object in algoirthm.

    Returns:
        tuple: Name of first condition asset, name of second condition asset.
    """
    asset1 = conditions["condition1"]["asset"]
    asset2 = conditions["condition2"]["asset"]

    return asset1, asset2


def get_asset_datasets(dataset, conditions):
    """Gets the data for each of the assets in condition from dataset.

    Args:
        dataset (dict): Dataset containing all assets, series', and indicator data to run algorithm.
        conditions (dict): Condition object in algoirthm.

    Returns:
        tuple: Pandas dataframe for first asset, pandas dataframe for second asset
    """
    asset1, asset2 = get_asset_names(conditions)
    return dataset[asset1], dataset[asset2]
