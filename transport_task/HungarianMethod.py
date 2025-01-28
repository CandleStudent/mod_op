import numpy as np

cost = np.array([[4893, 4280, 6213], [5327, 4296, 6188], [6006, 5030, 7224]])

# Для замены элементов
max_elem = np.max(cost) + 10000

# Матрица оптимального плана
final_matrix = np.zeros((3, 3), dtype=int)

otvet = np.zeros((3, 3), dtype=int)


# Запасы
supply = np.array([1000, 1700, 1600])  # индексация по i
# Потребности
demand = np.array([1600, 1000, 1700])  # индексация по j


if np.sum(supply) == np.sum(demand):
    print("Транспортная задача является закрытая")
else:
    print("Транспортная задача является открытая")
    cost = np.copy(np.append(cost, np.array([
        [0],
        [0],
        [0]
    ]), axis=1))
    demand = np.copy(np.append(demand, [abs(np.sum(demand) - np.sum(supply))]))
    final_matrix = np.zeros((3, 4), dtype=int)
    otvet = np.copy(final_matrix)

matrix_copy = np.copy(cost)


print(cost)

def check_zeros_rows(matrix):
    for row in matrix:
        min_elem = np.min(row)
        if min_elem != 0:
            for i in range(0, len(row) - 1):
                row[i] = row[i] - min_elem


def check_zeros_columns(matrix):
    for j in range(0, len(matrix)):
        column = matrix[:, j]
        min_elem = np.min(column)
        if min_elem != 0:
            for i in range(0, len(column)):
                column[i] = column[i] - min_elem


def distr_of_supplies(matrix):
    check_zeros_rows(matrix)
    check_zeros_columns(matrix)
    print("Checked matrix:")
    print(matrix)

    stocks = np.copy(supply)
    reqs = np.copy(demand)
    temporary_matrix = np.copy(final_matrix)



    # Копия нужна для того, чтобы потом вернуть нули в матрицу (поскольку нули при расчётах не считаются (например, при
    # нахождении минимального элемента), ниже в коде я заменяю нули заранее записанным в отдельную переменную
    # максимальным элементом в матрице + 1)
    matrix_copy = np.copy(matrix)

    # Проверяем, можем ли мы распределить поставки
    while np.min(matrix) == 0:
        mass = np.sum(matrix == 0, axis=1)
        min_count_of_zeros = np.min(mass[np.nonzero(mass)])


        i = np.where(mass == min_count_of_zeros)[0][0]
        row = matrix[i]
        j = np.where(row == 0)[0][0]

        min_stocks_reqs = min(stocks[i], reqs[j])
        print("min stock: ", min_stocks_reqs)
        temporary_matrix[i][j] = min_stocks_reqs
        # final_matrix[i][j] = min_stocks_reqs
        print("Промежуточный результат")
        print(temporary_matrix)
        stocks[i] = stocks[i] - min_stocks_reqs
        reqs[j] = reqs[j] - min_stocks_reqs


        matrix[i][j] = max_elem
        print("Матрица после вычёркивания")
        print(matrix)
        print(f"Запасы после: {stocks}")
        print(f"Потребности после: {reqs}")
        print("\n=========\n")



    # Если поставки распределить не получилось, ищем строку с максимальным запасом, затем вычитаем из каждого элемента
    # этой строки его минимальный элемент
    print("Temp1: ")
    global otvet
    otvet = np.copy(temporary_matrix)
    if np.count_nonzero(stocks) > 0:
        max_stock_index = np.where(stocks == np.max(stocks))[0][0]  # i Индекс максимального запаса
        min_elem_in_stock = np.min(matrix[max_stock_index])# Минимальный элемент в этой строке

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
print(otvet)
print()
Fmin = 0
while np.sum(otvet)>0:
        indices = np.where(otvet>0)
        r_i, c_i = indices[0][0], indices[1][0]
        Fmin += otvet[r_i][c_i]*matrix_copy[r_i][c_i]
        otvet[r_i][c_i] = 0
print(f'Найдем значение целевой функции = {Fmin}')