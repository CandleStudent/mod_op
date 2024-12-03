import numpy as np

from transport_task.OptimalPlanFinder import OptimalPlanFinder


class MethodOfPotentials(OptimalPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)
        self.potentials = []
        # таблица из 0 и 1. Отражает занятые и свободные клетки. Изначально 1 ставим туда, где не нуль. Потом по ситуации (стр. 45 -- когда у нас могут быть 0, но при этом занятые клетки)
        self.occupied_cells = np.array([np.zeros(len(self.demand)) for _ in range(len(self.supply))])
        self.max_delta = None
        self.max_delta_i_j = None

    def find_optimal_plan(self, basic_plan:np.array):
        self.optimal_plan = basic_plan
        self.initial_find_occupied_cells()
        self.find_potentials()
        while not self.is_plan_optimal():
            self.create_new_plan()
            self.find_potentials()

        return self.optimal_plan

    def initial_find_occupied_cells(self):
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if self.optimal_plan[i, j] != 0:
                    self.occupied_cells[i, j] = 1

    def find_potentials(self):
        non_null_cells = self.__find_non_null_cells()
        linear_equations_system_vars = []
        linear_equations_system_consts = []
        for indexes in non_null_cells:
            linear_equation = np.zeros(len(self.demand) + len(self.supply))
            linear_equation[indexes[0]] = 1
            linear_equation[len(self.supply) + indexes[1]] = 1
            linear_equations_system_vars.append(linear_equation)
            linear_equations_system_consts.append(self.cost[indexes[0], indexes[1]])
        linear_equations_system_vars = np.array(linear_equations_system_vars)
        # устанавливаем значение одной из переменных как нуль (убираем один столбец по сути, считая его известным)
        linear_equations_system_vars = linear_equations_system_vars[:, 1:]

        self.potentials = np.linalg.solve(linear_equations_system_vars, linear_equations_system_consts)
        self.potentials = np.append(0, self.potentials) # добавляем зануленный потенциал

    def __find_non_null_cells(self):
        non_null_cells = []
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if self.occupied_cells[i, j] != 0:
                    non_null_cells.append((i, j))
        return non_null_cells

    def is_plan_optimal(self):
        is_plan_optimal = True
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if self.occupied_cells[i, j] == 0:
                    delta = self.__get_supply_potential(i) + self.__get_demand_potential(j) - self.cost[i, j]
                    if delta > 0:
                        if is_plan_optimal:
                            is_plan_optimal = False
                            self.max_delta = delta
                            self.max_delta_i_j = (i, j)
                        else:
                            if delta > self.max_delta:
                                self.max_delta = delta
                                self.max_delta_i_j = (i, j)

        return is_plan_optimal

    def __get_demand_potential(self, index:int):
        return self.potentials[len(self.supply) + index]

    def __get_supply_potential(self, index:int):
        return self.potentials[index]

    def create_new_plan(self):
        cycle_matrix = [['' for _ in range(len(self.demand))] for _ in range(len(self.supply))]
        i_start, j_start = self.max_delta_i_j
        cycle_matrix[i_start, j_start] = '+'
        # find cycle and put + and - in cycle_matrix