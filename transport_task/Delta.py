import numpy as np

from transport_task.OptimalPlanFinder import OptimalPlanFinder
from transport_task.Utility import print_matrix

class DeltaMethod(OptimalPlanFinder):

    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

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



    def build_column_increment_table(self):
        print("1. Создание таблицы приращений по столбцам")
        column_increment_table = self.cost.copy()
        # проходим по столбцам, выбираем наим. стоимость и вычитываем ее из всех стоимостей столбца
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
    printMatrix(delta_costs)
    # Шаг 2: Создаем таблицу приращений по строкам
    for i in range(delta_costs.shape[0]):
        if np.min(delta_costs[i, :]) > 0:
            min_delta = np.min(delta_costs[i, :])
            delta_costs[i, :] -= min_delta


    print("\nТаблица приращений по строкам:\n")
    printMatrix(delta_costs)
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
    printMatrix(x)

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
    printMatrix(x)


    x, bfs = handle_degeneracy(x.copy(), bfs.copy())
    print("\nОптимальный план:")
    printMatrix(x)

    print("\nМинимальная сумма: ", get_total_cost(costs, x), "\n")


    return x, bfs
