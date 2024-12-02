import numpy as np
from scipy.optimize import linprog

class BasicPlanFinder:
    def __init__(self,
                 supply: np.array,
                 demand: np.array,
                 cost: np.array):
        self.supply = np.copy(supply)
        self.demand = np.copy(demand)
        self.cost = np.copy(cost)
        self.basic_plan = np.zeros(shape=[len(self.supply), len(self.demand)], dtype=int)
        self.cost_func = 0

    def find_path(self):
        pass


# Метод северо-западного угла. Предполагает заполнение изначального плана поставок
# от верхней левой клетки до правой, пока не будет исчерпан план поставки или принятие товара
class NorthWestCornerMethod(BasicPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

    def find_path(self):
        m = len(self.supply)
        n = len(self.demand)
        for i in range(m):
            for j in range(n):
                minimal_num = min(self.supply[i], self.demand[j])
                self.basic_plan[i, j] = minimal_num
                self.supply[i] -= minimal_num
                self.demand[j] -= minimal_num

        return self.cost


# план нахождения опорного плана "метод наименьшей стоимости"
# предполагает, в отличие от метода северо-западного угла, что на каждом шаге
# максимально возможным объемом заполняется не левая верхняя клетка, а та клетка
# незаполненной части таблицы, в которой содержится наименьшая стоимость перевозок c[i,j]

# в отличие от северо-западного угла дает более близкий к оптимальному опорный план
class MinimalCostMethod(BasicPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

    def __find_minimal_cost(self):
        min_cost = self.cost[0, 0]
        min_i = 0
        min_j = 0
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if self.cost[i, j] < min_cost and self.basic_plan == 0: # последнее условие для исключения уже обработанных клеток, ибо признак их обработки -- установление количества товаров
                    min_cost = self.cost[i, j]
        return (min_i, min_j)

    def __is_contains_only_zeros(self, arr:np.array):
        for el in arr:
            if el != 0:
                return False
        return True

    def find_path(self):
        # m = len(self.supply)
        # n = len(self.demand)
        while ( (not self.__is_contains_only_zeros(self.supply))
                and (not self.__is_contains_only_zeros(self.demand)) ):

            min_i, min_j = self.__find_minimal_cost()
            minimal_num = min(self.supply[min_i], self.demand[min_j])
            self.basic_plan[min_i, min_j] = minimal_num
            self.supply[min_i] -= minimal_num
            self.demand[min_j] -= minimal_num

        return self.basic_plan


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


class HungarianMethod(OptimalPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

    def find_optimal_plan(self, basic_plan:np.array):
        pass

class MethodOfPotentials(OptimalPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)
        self.potentials = []

    def find_optimal_plan(self, basic_plan:np.array):
        self.optimal_plan = basic_plan
        self.__find_potentials()
        while not self.__is_plan_optimal():
            self.__create_new_plan()
            self.__find_potentials()

        return self.optimal_plan

    def __find_potentials(self):
        non_null_cells = self.__find_non_null_cells()
        linear_equations_system_vars = []
        linear_equations_system_consts = []
        for indexes in non_null_cells:
            linear_equation = np.zeros(len(self.demand) + len(self.supply))
            linear_equation[indexes[0]] = 1
            linear_equation[len(self.supply) + indexes[1]] = 1
            linear_equations_system_vars.append(linear_equation)
            linear_equations_system_consts.append(self.cost[indexes[0], indexes[1]])
        # устанавливаем значение одной из переменных как нуль (убираем один столбец по сути, считая его известным)
        linear_equations_system_vars = linear_equations_system_vars[:-1]
        self.potentials = np.linalg.solve(linear_equations_system_vars, linear_equations_system_consts)
        self.potentials = np.append(self.potentials, 0) # добавляем зануленный потенциал

    def __find_non_null_cells(self):
        non_null_cells = []
        for i in range(self.supply):
            for j in range(self.demand):
                if self.optimal_plan[i, j] != 0:
                    non_null_cells.append((i, j))
        return non_null_cells

    def __is_plan_optimal(self):
        for i in range(self.supply):
            for j in range(self.demand):
                if self.optimal_plan[i, j] == 0:
                    delta = self.__get_supply_potential(i) - self.__get_demand_potential(j) - self.cost[i, j]
                    if delta > 0:
                        return False
        return True

    def __get_demand_potential(self, index:int):
        return self.potentials[len(self.supply) + index]

    def __get_supply_potential(self, index:int):
        return self.potentials[index]

    def __create_new_plan(self):
        pass

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


supply = np.array([1300, 1200, 1100])
demand = np.array([1000, 1500, 1100])
cost = np.array([
    [4893, 4280, 6213],
    [5327, 4296, 6188],
    [6006, 5030, 7224]])

task = Task(supply,
            demand,
            cost,
            MinimalCostMethod(supply, demand, cost),
            MethodOfPotentials(supply, demand, cost))

task.solve()
