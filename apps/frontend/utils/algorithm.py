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
            {"type": "buy", "assets": "MA"},
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
