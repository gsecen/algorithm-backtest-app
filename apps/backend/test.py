from backtest import Backtest
from dataset.dataset_builder import build_dataset
from utils.algorithm import sample_algo_requestv2

dataet = build_dataset(sample_algo_requestv2)

backtest = Backtest(sample_algo_requestv2, dataet)


print(backtest.backtest_algorithm())
