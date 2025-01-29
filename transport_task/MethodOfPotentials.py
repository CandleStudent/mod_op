import numpy as np

from transport_task.OptimalPlanFinder import OptimalPlanFinder

#TODO добавить вычисление целевой функции и проверку того, что она действительно уменьшается с каждой итерацией
class MethodOfPotentials(OptimalPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)
        self.potentials = []
        # таблица из 0 и 1. Отражает занятые и свободные клетки. Изначально 1 ставим туда, где не нуль. Потом по ситуации (стр. 45 -- когда у нас могут быть 0, но при этом занятые клетки)
        self.occupied_cells = np.array([np.zeros(len(self.demand)) for _ in range(len(self.supply))])
        self.max_delta = None
        self.max_delta_i_j = None

    def print_matr(self):
        for i in range(len(self.supply)):
            print(self.optimal_plan[i])

    def find_optimal_plan(self, basic_plan:np.array):
        print("Начало поиска оптимального плана")
        self.optimal_plan = basic_plan
        self.update_cost_func()
        print("Целевая функция: ", self.cost_func)
        print("Исходный план")
        self.print_matr()
        self.initial_find_occupied_cells()
        self.handle_degeneracy()
        self.find_potentials()
        while not self.is_plan_optimal():
            self.create_new_plan()
            # self.handle_degeneracy() #кажется, не нужно, ибо всегда одна клетка убирается и одна прибавляется
            print("Новый план")
            self.print_matr()
            self.find_potentials()
            self.update_cost_func()
            print("Целевая функция: ", self.cost_func)
            print("\n========\n")

        return self.optimal_plan

    def handle_degeneracy(self):
        # если базисных клеток меньше, чем m + n - 1
        is_degenerated = len(self.__get_occupied_cells()) < len(self.supply) + len(self.demand) - 1
        if is_degenerated:
            print("План вырожденный")
            print("Вводим фиктивную клетку")
            for i in range(len(self.supply) - 1):
                for j in range(len(self.demand)):
                    if (self.occupied_cells[i, j] == 0): #and self.occupied_cells[i + 1, j] != 0:
                        self.occupied_cells[i, j] = 1
                        if (self.find_loop((i, j))): # создает цикл, сл-но не подходит
                            self.occupied_cells[i, j] = 1
                        if not (len(self.__get_occupied_cells()) < len(self.supply) + len(self.demand) - 1):
                            print('Клетка: (', i, ',', j, ') = 0')
                            print('\n* * * * * * * * * * * * * * * * *\n')
                            return
        else:
            print("План невырожденный")

    def print_arr(self, arr):
        for el in arr:
            print(el, " ", end="")
        print()

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
        self.print_potential_system(linear_equations_system_vars, linear_equations_system_consts, non_null_cells)
        # устанавливаем значение одной из переменных как нуль (убираем один столбец по сути, считая его известным)
        linear_equations_system_vars = linear_equations_system_vars[:, 1:]

        self.potentials = np.linalg.solve(linear_equations_system_vars, linear_equations_system_consts)
        self.potentials = np.append(0, self.potentials) # добавляем зануленный потенциал
        print("\nПотенциалы")
        print("u1,   u2,   u3,      v1,      v2,      v3")
        self.print_arr(self.potentials)
        # print("Потенциалы:", self.potentials)

    def print_potential_system(self, coefs, consts, non_null_cells):
        print()
        print("Матрица системы для поиска потенциалов")
        # вывод названий
        print("матрица составляется только для занятых клеток")
        print("u1,  u2,   u3,  v1,  v2,  v3,cost_i_j,  i , j")

        for i in range(len(coefs)):
            self.print_arr(np.append(np.append(coefs[i], consts[i]),non_null_cells[i]))
            # print(coefs[i], "   ", consts[i], non_null_cells[i])

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
        print("план оптимальный? ", is_plan_optimal)
        return is_plan_optimal

    def __get_demand_potential(self, index:int):
        return self.potentials[len(self.supply) + index]

    def __get_supply_potential(self, index:int):
        return self.potentials[index]

    def create_new_plan(self):
        print("Создаем новый план")
        print("Цикл начинается в клетке ", self.max_delta_i_j)
        # find cycle and put + and - in cycle_matrix
        loop = self.find_loop(self.max_delta_i_j)
        print("Найденный цикл: ", loop)
        even_cells = loop[0::2]  # четные позиции в цикле <==> +
        odd_cells = loop[1::2]  # нечетные позиции в цикле <==> -
        lower_transfer_i, lower_transfer_j = self.__get_lower_transfer_index(odd_cells) # из всех объемов перевозок с - -- наименьший
        lower_tranfer = self.optimal_plan[lower_transfer_i, lower_transfer_j]
        print("Наименьший объем перевозок ", lower_tranfer, "В клетке ", lower_transfer_i, lower_transfer_j)
        # меняем матрицу занятости
        self.occupied_cells[lower_transfer_i, lower_transfer_j] = 0
        self.occupied_cells[self.max_delta_i_j[0], self.max_delta_i_j[1]] = 1
        # вычитаем и прибавляем lower_tranfer из - и + соотв
        self.__update_optimal_plan_after_find_lower_tranfer(even_cells, odd_cells, lower_tranfer)

    def __update_optimal_plan_after_find_lower_tranfer(self, even_cells, odd_cells, lower_transfer):
        count_null_cells = 0
        for even_cell in even_cells:
            self.optimal_plan[even_cell[0], even_cell[1]] += lower_transfer
        for odd_cell in odd_cells:
            self.optimal_plan[odd_cell[0], odd_cell[1]] -= lower_transfer
            # кажется, не нужно, ибо там и так будет 1, ибо мы зануляем только одну клетку в методе выше
            # count_null_cells += 1
            # if count_null_cells > 1:
            #     self.occupied_cells[odd_cell[0], odd_cell[1]] = 1

    def __get_lower_transfer_index(self, odd_cells: list[tuple[int, int]]):
        lower_transfer = self.optimal_plan[odd_cells[0]]
        min_i = 0
        min_j = 0
        for i, j in odd_cells:
            if self.optimal_plan[i, j] <= lower_transfer:
                lower_transfer = self.optimal_plan[i, j]
                min_i = i
                min_j = j
        return (min_i, min_j)


    def __get_occupied_cells(self):
        occupied_cells_list = []
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if self.occupied_cells[i, j] == 1:
                    occupied_cells_list.append((i, j))
        return occupied_cells_list

    def find_loop(self, loop_start):
        def recursion(loop):
            if len(loop) > 3:
                can_be_closed = len(self.get_possible_next_nodes(loop, [loop_start])) == 1
                if can_be_closed: return loop
            not_visited = list(set(self.__get_occupied_cells()) - set(loop))
            possible_next_nodes = self.get_possible_next_nodes(loop, not_visited)
            for next_node in possible_next_nodes:
                new_loop = recursion(loop + [next_node])
                if new_loop: return new_loop # если не пустой

        return recursion([loop_start])


    def get_possible_next_nodes(self, loop, not_visited):
        last_node = loop[-1]
        nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
        nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
        # Если цикл < 2 узлов, остаемся том же ряду и столбце.
        if len(loop) < 2:
            return nodes_in_row + nodes_in_column
        # Иначе чередуем строка-столбец
        else:
            prev_node = loop[-2]
            row_move = prev_node[0] == last_node[0]
            if row_move: return nodes_in_column
            return nodes_in_row