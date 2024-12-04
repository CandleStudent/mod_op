import numpy as np

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
        self.balance()
        return self.find_path_internal()

    def find_path_internal(self):
        pass

    def balance(self):
        sum_supply = sum(self.supply)
        sum_demand = sum(self.demand)
        is_task_balanced = sum_demand == sum_supply
        self.is_balanced = is_task_balanced
        if is_task_balanced:
            print("Задача сбалансирована")
        else:
            print("Задача несбалансирована. Сбалансируем ее")
            if sum_supply > sum_demand:
                # Вводим фиктивного n+1 потребителя
                self.demand = np.append(self.demand, sum_supply - sum_demand)
                for row_i in range(len(self.cost)):
                    self.cost[row_i] = np.append(self.cost[row_i], 0)
            else:
                # Вводим фиктивного m+1 поставщика
                self.supply = np.append(self.supply, sum_demand - sum_supply)
                self.cost = np.append(self.cost, np.zeros(len(self.demand)))

    def print_matr(self):
        for i in range(len(self.supply)):
            print(self.basic_plan[i])


# Метод северо-западного угла. Предполагает заполнение изначального плана поставок
# от верхней левой клетки до правой, пока не будет исчерпан план поставки или принятие товара
class NorthWestCornerMethod(BasicPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

    def find_path_internal(self):
        print("Поиск опорного плана северо-западным методом")
        m = len(self.supply)
        n = len(self.demand)
        for i in range(m):
            for j in range(n):
                minimal_num = min(self.supply[i], self.demand[j])
                self.basic_plan[i, j] = minimal_num
                self.supply[i] -= minimal_num
                self.demand[j] -= minimal_num
            print("Новая строка в опорном плане")
            self.print_matr()
            print("Из", self.supply)
            print("В", self.demand)

        return self.basic_plan


# план нахождения опорного плана "метод наименьшей стоимости"
# предполагает, в отличие от метода северо-западного угла, что на каждом шаге
# максимально возможным объемом заполняется не левая верхняя клетка, а та клетка
# незаполненной части таблицы, в которой содержится наименьшая стоимость перевозок c[i,j]

# в отличие от северо-западного угла дает более близкий к оптимальному опорный план
class MinimalCostMethod(BasicPlanFinder):
    def __init__(self, supply: np.array, demand: np.array, cost: np.array):
        super().__init__(supply, demand, cost)

    def __find_minimal_cost(self):
        min_cost = float("inf")
        min_i = 0
        min_j = 0
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if (self.cost[i, j] < min_cost
                        and self.supply[i] != 0 # для исключения обработнных потребностей
                        and self.demand[j] != 0): # для исключения обработнных поставок
                        # and self.basic_plan[i, j] == 0): # последнее условие для исключения уже обработанных клеток, ибо признак их обработки -- установление количества товаров
                    min_cost = self.cost[i, j]
                    min_i = i
                    min_j = j
        return (min_i, min_j)

    def __is_contains_only_zeros(self, arr:np.array):
        for el in arr:
            if el != 0:
                return False
        return True

    def find_path_internal(self):
        print("Поиск опорного плана методом наименьшей стоимости")
        while ( (not self.__is_contains_only_zeros(self.supply))
                and (not self.__is_contains_only_zeros(self.demand)) ):

            min_i, min_j = self.__find_minimal_cost()
            minimal_num = min(self.supply[min_i], self.demand[min_j])
            self.basic_plan[min_i, min_j] = minimal_num
            self.supply[min_i] -= minimal_num
            self.demand[min_j] -= minimal_num

            print("Обновление опорного плана")
            self.print_matr()
            print("Из", self.supply)
            print("В", self.demand)

        return self.basic_plan