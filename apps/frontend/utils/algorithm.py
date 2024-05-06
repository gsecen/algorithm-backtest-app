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
            {"type": "buy", "assets": "MSFT"},
            {
                "type": "instructions",
                "weight": [0.75, 0.25],
                "tasks": [
                    {"type": "buy", "assets": "AAPL"},
                    {"type": "buy", "assets": "TSLA"},
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
                            {"type": "buy", "assets": "MA"},
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
                                            {"type": "buy", "assets": "COST"},
                                            {"type": "buy", "assets": "NVDA"},
                                        ],
                                        "false": [
                                            {"type": "buy", "assets": "ADBE"},
                                            {"type": "buy", "assets": "AMZN"},
                                        ],
                                    }
                                ],
                            },
                        ],
                        "false": [
                            {"type": "buy", "assets": "V"},
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
        weight (list/int): Absolute weight for task/tasks.
        relative_weight (float): Current relative weight for task/tasks.

    Returns:
        float: Relative weight for task.
    """
    # Equal weight amongst tasks
    if weight == 1:
        return relative_weight / tasks_length
    # Specified weights
    else:
        return weight[task_index] * relative_weight


# Rough function which will iterate through all tasks in algorithm and keep track of weights
def iterate_tasks(tasks, weight, relative_weight):

    for index, task in enumerate(tasks):
        # Getting the new current relative weight for task
        current_relative_weight = calculate_task_weight(
            len(tasks), index, weight, relative_weight
        )

        if task["type"] == "buy":
            print(task)
            print(current_relative_weight)

        if task["type"] == "expression":
            iterate_tasks(task["true"], weight, current_relative_weight)
            iterate_tasks(task["false"], weight, current_relative_weight)

        if task["type"] == "instructions":
            iterate_tasks(task["tasks"], task["weight"], current_relative_weight)


def test():
    starting_weight = sample_algo_request["algorithm"]["weight"]
    # Relative weight argument will always be 1 at the start
    iterate_tasks(sample_algo_request["algorithm"]["tasks"], starting_weight, 1)


test()
