import numpy as np

from transport_task import BasicPlanFinder, OptimalPlanFinder
from transport_task.BasicPlanFinder import MinimalCostMethod, NorthWestCornerMethod
from transport_task.MethodOfPotentials import MethodOfPotentials


class Task:
    def __init__(self,
                 supply: np.array,
                 demand: np.array,
                 cost: np.array,
                 basicPlanFinder:BasicPlanFinder,
                 optimalPlanFinder:OptimalPlanFinder):

        self.supply = supply
        self.demand = demand
        self.cost = cost
        self.plan = np.zeros(shape=[len(self.supply), len(self.demand)], dtype=int)
        self.basicPlanFinder = basicPlanFinder
        self.optimalPlanFinder = optimalPlanFinder

    def solve(self):
        self.plan = self.optimalPlanFinder.find_optimal_plan(self.basicPlanFinder.find_path())


# costs1 = np.array([[4893, 4280, 6213], [5327, 4296, 6188], [6006, 5030, 7224]])
# supply1 = np.array([1000, 1700, 1600])  # запасы
# demand1 = np.array([1600,1000,1700])  # спрос
# print(MinimalCostMethod(supply1, demand1, costs1).find_path())
# task = Task(supply1,
#             demand1,
#             costs1,
#             MinimalCostMethod(supply1, demand1, costs1),
#             MethodOfPotentials(supply1, demand1, costs1))
#
# task.solve()
# print(task.plan)


supply = np.array([1300, 1200, 1100])
demand = np.array([1000, 1500, 1100])
cost = np.array([
    [4893, 4280, 6213],
    [5327, 4296, 6188],
    [6006, 5030, 7224]])
print(MinimalCostMethod(supply, demand, cost).find_path())

task = Task(supply,
            demand,
            cost,
            NorthWestCornerMethod(supply, demand, cost),
            MethodOfPotentials(supply, demand, cost))

task.solve()
print(task.plan)
