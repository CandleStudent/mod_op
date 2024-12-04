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
        self.is_balanced = True

    def find_optimal_plan(self, basic_plan:np.array):
        # self.balance()
        self.find_internal(basic_plan)

    # def balance(self):
    #     sum_supply = sum(self.supply)
    #     sum_demand = sum(self.demand)
    #     is_task_balanced = sum_demand == sum_supply
    #     self.is_balanced = is_task_balanced
    #     if is_task_balanced:
    #         print("Задача сбалансирована")
    #     else:
    #         print("Задача несбалансирована. Сбалансируем ее")
    #         if sum_supply > sum_demand:
    #             # Вводим фиктивного n+1 потребителя
    #             self.demand = np.append(self.demand, sum_supply - sum_demand)
    #             for row_i in range(len(self.cost)):
    #                 self.cost[row_i] = np.append(self.cost[row_i], 0)
    #         else:
    #             # Вводим фиктивного m+1 поставщика
    #             self.supply = np.append(self.supply, sum_demand - sum_supply)
    #             self.cost = np.append(self.cost, np.zeros(len(self.demand)))



    def find_internal(self, basic_plan:np.array):
        pass