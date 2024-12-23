import numpy as np

from transport_task.OptimalPlanFinder import OptimalPlanFinder
from transport_task.Utility import print_matrix

class DeltaMethod(OptimalPlanFinder):

    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)
        self.supply_diff = None
        self.occupied_cells = np.array([np.zeros(len(self.demand)) for _ in range(len(self.supply))])

    # here assignment_matrix equals to optimal_plan
    def find_optimal_plan(self, basic_plan:np.array):
        print("Начало работы дельта-метода")
        print("Исходная таблица стоимости")
        print_matrix(self.cost)
        column_increment_table = self.build_column_increment_table() # постр. таблицу приращений
        print("Таблица приращений по столбцам")
        print_matrix(column_increment_table)
        row_increment_table = self.build_row_increment_table(column_increment_table)
        print("Таблица приращений по строкам")
        print_matrix(row_increment_table)
        assignment_matrix = self.assign_customer_to_supplier(row_increment_table)
        print("матрица прикреплений поставщиков и потребителей")
        print_matrix(assignment_matrix)

        self.get_virtual_and_real_supply_diff(assignment_matrix) # self.supply_diff

        while not self.is_plan_after_diff_optimal():
            print("Найден неоптимальный план. Продолжаем алгоритм")
            columns_with_cells_in_zero_or_excessive_rows = self.get_columns_indexes_with_cells_in_excessive_rows(assignment_matrix) # п. 5 столбцы, имеющие занятые клетки в избыточных строках
            lowest_diffs_in_marked_row_column_pairs = self.get_lowest_diffs_in_marked_row_column_pairs(columns_with_cells_in_zero_or_excessive_rows, row_increment_table) #п. 6
            # п. 7
            deficient_rows_indexes = [i for i in range(len(self.supply)) if self.supply_diff[i] > 0]
            minimal_lowest_diff_for_deficient_rows = min([lowest_diffs_in_marked_row_column_pairs[i] for i in deficient_rows_indexes])
            # два случая: минимум меньше всех минимумов для нулевых строк и минимум некоторых нулевых строк меньше найденного минимума
            zero_rows_indexes = [i for i in range(len(self.supply)) if self.supply_diff[i] == 0]
            zero_rows_minimal = min([lowest_diffs_in_marked_row_column_pairs[i] for i in zero_rows_indexes])
            zero_rows_index_minimal = self.__get_minimal_index_in_dict_from_list(lowest_diffs_in_marked_row_column_pairs, zero_rows_indexes)
            zero_rows_column_index_minimal = [j for j in range(len(self.demand)) if lowest_diffs_in_marked_row_column_pairs[zero_rows_index_minimal] == zero_rows_minimal][0]
            if minimal_lowest_diff_for_deficient_rows <= zero_rows_minimal:
                #TODO
                # случай 1. Просто производим перераспределение из избыточной строки в недостаточную в клетку отмеченного столбца. кот соответствует min delta
                redistribution_value = min()

            else:
                # случай 2 (п. 9)
                # проверяем перераспределение по цепочкам
                # в нулевой строке в отмеченном столбце находим клетку, где у нас мин меньше мина для недостаточных строк
                

            self.get_virtual_and_real_supply_diff(assignment_matrix)  # self.supply_diff

        #TODO проверить план методом потенциалов на корректность
        print("Найден оптимальный план")
        print_matrix(assignment_matrix)
        return assignment_matrix

            
    def __get_minimal_index_in_dict_from_list(self, dict, list):
        min_value = float("inf")
        min_index = -1
        for el in list:
            if dict[el] < min_value:
                min_value = dict[el]
                min_index = el
        return min_index


    def build_column_increment_table(self):
        print("1. Создание таблицы приращений по столбцам")
        column_increment_table = self.cost.copy()
        # проходим по столбцам, выбираем наим. стоимость и вычитаем ее из всех стоимостей столбца
        for col_index in range(len(column_increment_table[0])):
            # поиск наименьшего значения в столбце
            min_column_cost = min([row[col_index] for row in column_increment_table])
            # вычитаем ее
            for row_index in range(len(column_increment_table)):
                column_increment_table[row_index, col_index] -= min_column_cost

        return column_increment_table


    def build_row_increment_table(self, column_increment_table:np.array):
        print("2. Создание таблицы приращений по строкам")
        row_increment_table = column_increment_table.copy()
        for row_index in range(len(row_increment_table)):
            curr_row = row_increment_table[row_index]
            min_row_cost = min(curr_row)
            if min_row_cost > 0:
                # вычитаем из ненулевых значений
                for col_index in range(len(row_increment_table[row_index])):
                    row_increment_table[row_index, col_index] -= 0 if row_increment_table[row_index, col_index] <= 0 else min_row_cost

        return row_increment_table


    def assign_customer_to_supplier(self, row_increment_table:np.array):
        print("3. Назначение потребителей поставщикам")
        supply = self.supply.copy()
        demand = self.demand.copy()
        x = np.zeros_like(row_increment_table)
        for num_zeros in range(1, row_increment_table.shape[0] + row_increment_table.shape[1]):
            for j in range(row_increment_table.shape[1]):
                zero_indices = np.where(row_increment_table[:, j] == 0)[0]
                if len(zero_indices) == num_zeros:
                    if num_zeros == 1:
                        for i in zero_indices:
                            # print(supply[i], demand[j])
                            x[i, j] = demand[j]
                            # bfs.append(((i, j), demand[j]))
                            supply[i] -= demand[j]
                            demand[j] -= demand[j]
                    else:
                        for i in zero_indices:
                            min_sup_demand = min(supply[i], demand[j])
                            x[i, j] = min_sup_demand
                            supply[i] -= min_sup_demand
                            demand[j] -= min_sup_demand
        return x

    def get_virtual_and_real_supply_diff(self, assignment_matrix):
        print("4. Подсчитываем для строк разницы между фактическими запасами и полученными для опорного фиктивного плана")
        self.supply_diff = np.zeros_like(self.supply)
        for i in range(len(self.supply)):
            self.supply_diff[i] = self.supply[i] - sum(assignment_matrix[i])

    def get_columns_indexes_with_cells_in_excessive_rows(self, assignment_matrix):
        # print("Получение столбцов, у которых есть занятые клетки в избыточных строках")
        columns_indexes = set()
        for col_index in range(len(self.cost[0])):
            for row_index in range(len(self.cost)):
                if self.supply_diff[row_index] < 0 and assignment_matrix[row_index, col_index] > 0:
                    columns_indexes.add(col_index)
        return np.array(list(columns_indexes))

    def is_plan_after_diff_optimal(self):
        return len(self.supply_diff) == np.where(self.supply_diff[:] == 0)[0]  # см. п. 4 все дельты = 0. Все грузы перевозятся с наименьшими приращениями стоимости


    # п. 6 Возвращает key-value -- row_index : min_diff
    def get_lowest_diffs_in_marked_row_column_pairs(self, columns_with_cells_in_zero_or_excessive_rows,
                                                    row_increment_table):
        lowest_diffs = {} # float(inf, если нет подходящих элементов. В остальном повторяет длину массива супплая
        for row_index in range(len(self.cost)):
            if self.supply_diff[row_index] >= 0:
                lowest_diff = float("inf")
                for col_index in columns_with_cells_in_zero_or_excessive_rows:
                    if row_increment_table[row_index, col_index] < lowest_diff:
                        lowest_diff = row_increment_table[row_index, col_index]
                lowest_diffs[row_index] = lowest_diff
        return lowest_diffs

def delta_method(costs, supply, demand):
    print("\n----------- Дельта мтеод -----------")

    # Шаг 1: Создаем таблицу приращений по столбцам
    costs = np.array(costs, dtype=float)
    supply = np.array(supply, dtype=float)
    demand = np.array(demand, dtype=float)

    supply_copy = supply.copy()

    delta_costs = costs.copy()


    bfs = []


    for j in range(delta_costs.shape[1]):
        min_cost = np.min(delta_costs[:, j])
        delta_costs[:, j] -= min_cost
    print("\nТаблица приращений по столбцам:\n")
    print_matrix(delta_costs)
    # Шаг 2: Создаем таблицу приращений по строкам
    for i in range(delta_costs.shape[0]):
        if np.min(delta_costs[i, :]) > 0:
            min_delta = np.min(delta_costs[i, :])
            delta_costs[i, :] -= min_delta


    print("\nТаблица приращений по строкам:\n")
    print_matrix(delta_costs)
    # Шаг 3: Закрепляем потребности bj, начиная с столбцов с минимальным числом нулевых приращений
    x = np.zeros_like(delta_costs)


    for num_zeros in range(1, delta_costs.shape[0] + delta_costs.shape[1]):
        # print("num_zeros= ", num_zeros)
        for j in range(delta_costs.shape[1]):
            zero_indices = np.where(delta_costs[:, j] == 0)[0]
            # print("zero_indices", zero_indices)
            if len(zero_indices) == num_zeros:
                for i in zero_indices:
                    if supply[i] > 0 and demand[j] > 0:

                        # print(supply[i], demand[j])
                        x[i, j] =  demand[j]
                        # bfs.append(((i, j), demand[j]))
                        supply[i] -=  demand[j]
                        demand[j] -=  demand[j]
                        if supply[i] == 0 or demand[j] == 0:
                            break
    print("\nТаблица после закрепления потребностей:\n")
    print_matrix(x)

    # Шаг 4: Подсчитываем ∆a_i для строк и определяем их статус

    delta_supply = supply_copy - x.sum(axis=1)
    print("\n∆a_i = ", delta_supply)
    surplus_rows = np.where(delta_supply < 0)[0]
    deficit_rows = np.where(delta_supply > 0)[0]
    zero_rows = np.where(delta_supply == 0)[0]

    # Шаги 5–12: Перераспределение по цепочкам для устранения избытков и дефицитов
    while len(deficit_rows) > 0 or len(surplus_rows) > 0:
        marked_columns = set(j for i in surplus_rows for j in range(x.shape[1]) if x[i, j] > 0)

        # Находим наименьшее значение среди отмеченных столбцов для дефицитных строк
        min_cost_chain = None
        min_chain_value = float('inf')
        for i in deficit_rows:
            for j in marked_columns:
                if delta_costs[i, j] < min_chain_value:
                    min_cost_chain = (i, j)
                    min_chain_value = delta_costs[i, j]
        print('\nНаименьшее значение среди столбцов имющих значения в +строках: \n', min_cost_chain,' = ', min_chain_value)
        # Если есть перераспределение
        if min_cost_chain:
            i, j = min_cost_chain
            transfer_amount = min(delta_supply[i], -delta_supply[surplus_rows[0]])

            print("\nВеличина перераспределения = ", transfer_amount)
            x[surplus_rows[0], j] -= transfer_amount
            print("\nx",surplus_rows[0],j, " - ", transfer_amount, " = ", x[surplus_rows[0], j])

            # bfs.append(((surplus_rows[0], j), x[surplus_rows[0], j]))
            x[i, j] += transfer_amount
            print("\n x",i,j, " + ", transfer_amount, " = ", x[i, j])



            # bfs.append(((i, j), x[i, j]))

            delta_supply[surplus_rows[0]] += transfer_amount

            delta_supply[i] -= transfer_amount

            print("\n∆a_i = ", delta_supply)


            # Обновление строковых состояний
            surplus_rows = np.where(delta_supply < 0)[0]
            deficit_rows = np.where(delta_supply > 0)[0]
            zero_rows = np.where(delta_supply == 0)[0]
        else:
            break
    for i in range(x.shape[0]):
      for j in range(x.shape[1]):
        if(x[i, j] != 0):
          bfs.append(((i, j), x[i, j]))



    print("\nПолученный план: ")
    print_matrix(x)


    x, bfs = handle_degeneracy(x.copy(), bfs.copy())
    print("\nОптимальный план:")
    print_matrix(x)

    print("\nМинимальная сумма: ", get_total_cost(costs, x), "\n")


    return x, bfs
