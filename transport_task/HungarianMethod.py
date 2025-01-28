import numpy as np

from transport_task.BasicPlanFinder import BasicPlanFinder

def calculate_delta_k(demand:np.array, supply:np.array, plan:np.array): # суммарная невязка матрицы, которая характеризует близость решения к оптимальному
    # суммируем потребности и запасы и вычитываем из них сумму всех клеток плана
    supply_and_demands = np.sum(demand) + np.sum(supply)
    plan_cells_sum = np.sum(plan)
    return supply_and_demands - plan_cells_sum

cost = np.array([[4893, 4280, 6213], [5327, 4296, 6188], [6006, 5030, 7224]])

# Для замены элементов. используется для "вычёркивания" обработанных ячеек (замена на очень большое значение).
max_elem = np.max(cost) + 100000

# Матрица оптимального плана
optimal_plan = np.zeros((3, 3), dtype=int)

answer_matrix = np.zeros((3, 3), dtype=int)


# Запасы
supply = np.array([1000, 1700, 1600])  # индексация по i
# Потребности
demand = np.array([1600, 1000, 1700])  # индексация по j

# Балансируем задачу
balancer = BasicPlanFinder(cost=cost, demand=demand, supply=supply)
balancer.balance()
supply = balancer.supply
demand = balancer.demand
cost = balancer.cost

matrix_copy = np.copy(cost)

print(cost)

def check_zeros_rows(matrix):
    for row in matrix:
        min_elem = np.min(row)
        if min_elem != 0:
            # for i in range(0, len(row) - 1):
            for i in range(0, len(row)):
                row[i] = row[i] - min_elem


def check_zeros_columns(matrix):
    for j in range(0, len(matrix)):
        column = matrix[:, j]
        min_elem = np.min(column)
        if min_elem != 0:
            for i in range(0, len(column)):
                column[i] = column[i] - min_elem


def distr_of_supplies(matrix):
    # Делаем базисную матрицу из шага 1. Для этого, если у нас минимальный элемент не нуль, то мы вычитаем минимальный элемент из всех элементов столбца/строки
    check_zeros_rows(matrix)
    check_zeros_columns(matrix)
    print("Checked matrix:")
    print(matrix)

    stocks = np.copy(supply)
    reqs = np.copy(demand)
    temporary_matrix = np.copy(optimal_plan)



    # Копия нужна для того, чтобы потом вернуть нули в матрицу (поскольку нули при расчётах не считаются (например, при
    # нахождении минимального элемента), ниже в коде я заменяю нули заранее записанным в отдельную переменную
    # максимальным элементом в матрице + 1)
    matrix_copy = np.copy(matrix)

    # Проверяем, можем ли мы распределить поставки
    while np.min(matrix) == 0:
        amount_of_zeros_in_each_row = np.sum(matrix == 0, axis=1) # массив, содержащий количество нулей в каждой строке.
        min_count_of_zeros = np.min(amount_of_zeros_in_each_row[np.nonzero(amount_of_zeros_in_each_row)])

        # Находим строку с минимальным количеством нулей.
        i = np.where(amount_of_zeros_in_each_row == min_count_of_zeros)[0][0]
        row = matrix[i]
        j = np.where(row == 0)[0][0] # столбцы, где элемент найденной строки = 0

        min_stocks_reqs = min(stocks[i], reqs[j]) # нахожим минимум среди поставок и запросов
        print("min stock: ", min_stocks_reqs)
        temporary_matrix[i][j] = min_stocks_reqs
        # final_matrix[i][j] = min_stocks_reqs
        print("Промежуточный результат")
        print(temporary_matrix)
        stocks[i] = stocks[i] - min_stocks_reqs
        reqs[j] = reqs[j] - min_stocks_reqs


        matrix[i][j] = max_elem # отработали данный элемент
        print("Матрица после вычёркивания")
        print(matrix)
        print(f"Запасы после: {stocks}")
        print(f"Потребности после: {reqs}")
        print("\n=========\n")

        current_delta_k = calculate_delta_k(demand, supply, matrix)
        print("Текущая невязка матрицы: ", current_delta_k)



    # Если поставки распределить не получилось, ищем строку с максимальным запасом, затем вычитаем из каждого элемента
    # этой строки его минимальный элемент
    print("Temp1: ")
    global answer_matrix
    answer_matrix = np.copy(temporary_matrix)
    if np.count_nonzero(stocks) > 0:
        max_stock_index = np.where(stocks == np.max(stocks))[0][0]  # i Индекс максимального запаса
        min_elem_in_stock = np.min(matrix[max_stock_index])# Минимальный элемент в этой строке, не считая нули (они помечены огромными значениями)

        matrix = np.copy(matrix_copy)
        for elem_index in range(0, len(matrix[max_stock_index])):
            matrix[max_stock_index][elem_index] = matrix[max_stock_index][elem_index] - min_elem_in_stock

        # Если в полученной строке есть отрицательный элемент, то к элементам столбца, в котором он находится,
        # прибавляем абсолютное значение этого элемента
        print("Строка до прибавлений: ", matrix[max_stock_index])
        while np.min(matrix[max_stock_index]) < 0:
            min_elem_in_stock = np.min(matrix[max_stock_index])
            min_index = np.where(matrix[max_stock_index] == min_elem_in_stock)[0][0]
            print("Индекс отрицательного числа: ", min_index)
            for i in range(len(matrix)):
                print("Столбец до прибавлений: ", matrix[i][min_index])
                matrix[i][min_index] = matrix[i][min_index] + abs(min_elem_in_stock)
            print("Матрица после прибавлений")
            print(matrix)
        print("----------------")
        distr_of_supplies(matrix)
    print("Temp2: ")
    print(temporary_matrix)

    return temporary_matrix


def hungarian_method():
    print("Начало итераций")
    answer = np.copy(distr_of_supplies(cost))
    print("Конец итераций")


hungarian_method()
print(answer_matrix)
print()
Fmin = 0
while np.sum(answer_matrix)>0:
        indices = np.where(answer_matrix > 0)
        r_i, c_i = indices[0][0], indices[1][0]
        Fmin += answer_matrix[r_i][c_i] * matrix_copy[r_i][c_i]
        answer_matrix[r_i][c_i] = 0
print(f'Найдем значение целевой функции = {Fmin}')