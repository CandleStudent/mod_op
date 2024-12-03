import numpy as np

from transport_task.OptimalPlanFinder import OptimalPlanFinder


class HungarianMethod(OptimalPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

    def find_optimal_plan(self, basic_plan:np.array):
        pass