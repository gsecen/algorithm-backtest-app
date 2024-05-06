"""This module helps with all algorithm related functions"""

# Will all make more sense once UI is done then you can visually see the structure of algoirithm


# Things to note:
# Type buy is the purchase of an asset
# Type expression is an if else statement
# Type instructions is anytime you want a new weight or want to branch off (will make more sense soon)
sample_algo_request = {
    "start_date": "2020-01-01",
    "end_date": "2021-01-01",
    "name": "test algo",
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
                    {"type": "buy", "asset": "TSLA"},
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
                                "function": "price",
                                "asset": "AAPL",
                            },
                            "condition2": {
                                "function": "fixed_value",
                                "value": 10,
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
                                                "function": "price",
                                                "asset": "AAPL",
                                            },
                                            "condition2": {
                                                "function": "fixed_value",
                                                "value": 10,
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

    def get_tasks_buy_and_condition_data(tasks):
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
                get_tasks_buy_and_condition_data(task["true"])
                get_tasks_buy_and_condition_data(task["false"])

            if task["type"] == "instructions":
                get_tasks_buy_and_condition_data(task["tasks"])

    get_tasks_buy_and_condition_data(algorithm["algorithm"]["tasks"])

    return data


# print(get_buy_and_condition_data(sample_algo_request))


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
    iterate_tasks(sample_algo_request["algorithm"]["tasks"], starting_weight, 1)


# test()
