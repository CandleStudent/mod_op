import numpy as np

from transport_task import BasicPlanFinder, OptimalPlanFinder
from transport_task.BasicPlanFinder import MinimalCostMethod, NorthWestCornerMethod
from transport_task.MethodOfPotentials import MethodOfPotentials

#TODO выделить в отдельный класс балансировку задачи
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


# ДРУГОЙ ВАРИАНТ
costs1 = np.array([[4893, 4280, 6213], [5327, 4296, 6188], [6006, 5030, 7224]])
supply1 = np.array([1000, 1700, 1600])  # запасы
demand1 = np.array([1600,1000,1700])  # спрос
print(MinimalCostMethod(supply1, demand1, costs1).find_path())
task = Task(supply1,
            demand1,
            costs1,
            MinimalCostMethod(supply1, demand1, costs1),
            MethodOfPotentials(supply1, demand1, costs1))

task.solve()
print(task.plan)

# ИЗ ПОСОБИЯ
# supply2 = np.array([100, 300, 180, 320])
# demand2 = np.array([200, 250, 120, 130, 200])
# cost2 = np.array([
#     [10, 7, 2, 5, 5],
#     [4, 9, 8, 1, 3],
#     [5, 12, 16, 8, 7],
#     [7, 4, 6, 3, 11]
# ])
# task = Task(supply2,
#             demand2,
#             cost2,
#             MinimalCostMethod(supply2, demand2, cost2),
#             MethodOfPotentials(supply2, demand2, cost2))
#
# task.solve()
# print(task.plan)

supply = np.array([1300, 1200, 1100])
demand = np.array([1000, 1500, 1100])
cost = np.array([
    [4893, 4280, 6213],
    [5327, 4296, 6188],
    [6006, 5030, 7224]])
# print(MinimalCostMethod(supply, demand, cost).find_path())
# minimal_cost_method = MinimalCostMethod(supply, demand, cost)
# basic_plan = minimal_cost_method.find_path()
# potentials_method = MethodOfPotentials(minimal_cost_method.supply, minimal_cost_method.demand, minimal_cost_method.cost)
# optimal_plan = potentials_method.find_optimal_plan(basic_plan)
# task = Task(supply,
#             demand,
#             cost,
#             MinimalCostMethod(supply, demand, cost),
#             MethodOfPotentials(supply, demand, cost))
#
# task.solve()
# print(task.plan)


# north_west_corner_method = NorthWestCornerMethod(supply, demand, cost)
# basic_plan = north_west_corner_method.find_path()
# potentials_method = MethodOfPotentials(north_west_corner_method.supply, north_west_corner_method.demand, north_west_corner_method.cost)
# optimal_plan = potentials_method.find_optimal_plan(basic_plan)
# task = Task(supply,
#             demand,
#             cost,
#             NorthWestCornerMethod(supply, demand, cost),
#             MethodOfPotentials(supply, demand, cost))
#
# task.solve()
# print(task.plan)
