import numpy as np

class OptimalPlanFinder:
    def __init__(self,
                 supply: np.array,
                 demand: np.array,
                 cost: np.array):
        self.supply = np.copy(supply)
        self.demand = np.copy(demand)
        self.cost = np.copy(cost)
        self.cost_func = 0
        self.optimal_plan = np.zeros([len(self.supply), len(self.demand)])

    def find_optimal_plan(self, basic_plan:np.array):
        pass

    def update_cost_func(self):
        cost = 0
        for i in range(len(self.cost)):
            for j in range(len(self.cost[0])):
                cost += self.cost[i, j] * self.optimal_plan[i, j]
        self.cost_func = cost