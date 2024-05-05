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


# Rough function to get the actual weight of task
# Must keep in mind there are weights of grandparent and parent tasks
# which will effect the actual weight of task
def get_task_weight(tasks, previous_weight, weight, task_index=0):
    # If equal weight split weight amongst all tasks
    if weight == 1:
        current_weight = weight / len(tasks)
        return current_weight / previous_weight
    # If specified weight return weight for that task
    else:
        current_weight = weight[task_index]
        return current_weight / previous_weight


def calculate_weight(tasks_length, task_index, tasks_weights, actual_parent_weight):
    if tasks_weights == 1:  # Equal weight amongst tasks
        return actual_parent_weight / tasks_length
    else:  # Specified weights
        return tasks_weights[task_index] * actual_parent_weight


# Rough function which will iterate through all tasks and keep track of weights
def iterate_through_tasks(tasks):
    print(len(tasks))
    for index, task in enumerate(tasks):
        if task["type"] == "buy":
            print(index)
            print(task)
        # if task["type"] == "expression":
        #     iterate_through_tasks(task["true"])
        #     iterate_through_tasks(task["false"])
        # if task["type"] == "instructions":
        #     iterate_through_tasks(task["tasks"])


# Rough function to handle type buys
# def handle_buy(task):


def test():
    starting_weight = sample_algo_request["algorithm"]["weight"]
    iterate_through_tasks(sample_algo_request["algorithm"]["tasks"])


# test()
