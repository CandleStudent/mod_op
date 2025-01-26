# Магазин прессует и складывает в поддоны пустые картонные упаковочные
# коробки для их последующей переработки. За день штабелируется пять поддонов.
# Стоимость хранения одного поддона на заднем дворе магазина составляет 0,10 долл. в
# день. Компания, которая перевозит поддоны в перерабатывающий центр, устанавливает
# оплату в 100 долл. за аренду своего погрузочного оборудования плюс 3 долл. за перевозку
# каждого поддона. Разработайте оптимальную стратегию доставки поддонов в
# перерабатывающий центр.

class InventoryManagement:
    def __init__(self, v, s, k, cost_per_product):
        # input
        self.v = v # скорость потребление запаса
        self.s = s # траты на хранение запаса
        self.k = k # траты на осуществление запаса. Не зависят от размера заказа
        self.pallet_fright = cost_per_product # стоимость перевозки одного поддона

        # output
        self.q = None # размер заказа
        self.l = None # траты на управление запасами
        self.theta = None # период поставки (время между поставками)

    def solve_task(self):
        q_func = lambda k, v, s: (2 * k * v / s)**0.5
        l_func = lambda k, v, s, q: k * v / q + s * q / 2
        theta_func = lambda q, v: q / v

        self.q = q_func(self.k, self.v, self.s)
        self.l = l_func(self.k, self.v, self.s, self.q)
        self.theta = theta_func(self.q, self.v)


if __name__ == "__main__":
    inventory_management = InventoryManagement(v = 5, s  =0.1, k = 100, cost_per_product=3)
    inventory_management.solve_task()
    print("Решение задачи управления запасами со следующими входными данными:")
    print("Скорость потребление запаса: {} ед.товара на ед. времени".format(inventory_management.v))
    print("Траты на хранение запаса: {} ед.денег на ед. времени * ед. товара".format(inventory_management.s))
    print("Траты на осуществление зааказа: {} ед.денег".format(inventory_management.k))
    print("=========ОТВЕТ=========")
    print("Оптимальный размер поставки паллетов: ", inventory_management.q)
    print("Траты на управление запасами: ", inventory_management.l)
    print("Период поставки (время между поставками)", inventory_management.theta)