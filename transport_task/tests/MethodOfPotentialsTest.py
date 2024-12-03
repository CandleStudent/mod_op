import unittest

import numpy as np

from transport_task.BasicPlanFinder import NorthWestCornerMethod, MinimalCostMethod
from transport_task.MethodOfPotentials import MethodOfPotentials


class MethodOfPotentialsTest(unittest.TestCase):
    def setUp(self):
        # тестовые данные со страниц 38-39 методички (примеры использования методов)
        self.supply = np.array([100, 300, 180, 320])
        self.demand = np.array([200, 250, 120, 130, 200])
        self.cost = np.array([
            [10, 7, 2, 5, 5],
            [4, 9, 8, 1, 3],
            [5, 12, 16, 8, 7],
            [7, 4, 6, 3, 11]
        ])
        self.methodOfPotentials = MethodOfPotentials(self.supply, self.demand, self.cost)

    def test_find_potentials(self):
        supply = np.array([100, 300, 180, 320])
        demand = np.array([200, 250, 120, 130, 200])
        cost = np.array([
            [10, 7, 2, 5, 5],
            [4, 9, 8, 1, 3],
            [5, 12, 16, 8, 7],
            [7, 4, 6, 3, 11]
        ])
        methodOfPotentials = MethodOfPotentials(supply, demand, cost)
        optimal_plan = np.array([
            [0, 0, 100, 0, 0],
            [0, 0, 0, 130, 170],
            [180, 0, 0, 0, 0],
            [20, 250, 20, 0, 30]
        ])
        methodOfPotentials.optimal_plan = optimal_plan
        methodOfPotentials.initial_find_occupied_cells()

        methodOfPotentials.find_potentials()

        expected_potentials = np.array([0, -4, 2, 4, 3, 0, 2, 5, 7]) # см. страницу 46 пособия
        np.testing.assert_allclose(methodOfPotentials.potentials, expected_potentials, atol=1e-5)

    def test_is_plan_optimal_negative_test(self):
        supply = np.array([100, 300, 180, 320])
        demand = np.array([200, 250, 120, 130, 200])
        cost = np.array([
            [10, 7, 2, 5, 5],
            [4, 9, 8, 1, 3],
            [5, 12, 16, 8, 7],
            [7, 4, 6, 3, 11]
        ])
        methodOfPotentials = MethodOfPotentials(supply, demand, cost)
        optimal_plan = np.array([
            [0, 0, 100, 0, 0],
            [0, 0, 0, 130, 170],
            [180, 0, 0, 0, 0],
            [20, 250, 20, 0, 30]
        ])
        methodOfPotentials.optimal_plan = optimal_plan
        methodOfPotentials.potentials = np.array([0, -4, 2, 4, 3, 0, 2, 5, 7])

        # данные со страницы 46
        self.assertFalse(methodOfPotentials.is_plan_optimal())
        self.assertEquals(methodOfPotentials.max_delta, 6)
        self.assertEquals(methodOfPotentials.max_delta_i_j, (3, 3))

    def test_create_new_plan(self):
        supply = np.array([100, 300, 180, 320])
        demand = np.array([200, 250, 120, 130, 200])
        cost = np.array([
            [10, 7, 2, 5, 5],
            [4, 9, 8, 1, 3],
            [5, 12, 16, 8, 7],
            [7, 4, 6, 3, 11]
        ])
        methodOfPotentials = MethodOfPotentials(supply, demand, cost)
        optimal_plan = np.array([
            [0, 0, 100, 0, 0],
            [0, 0, 0, 130, 170],
            [180, 0, 0, 0, 0],
            [20, 250, 20, 0, 30]
        ])
        methodOfPotentials.optimal_plan = optimal_plan
        methodOfPotentials.potentials = np.array([0, -4, 2, 4, 3, 0, 2, 5, 7])
        methodOfPotentials.max_delta = 6
        methodOfPotentials.max_delta_i_j = (3, 3)

        methodOfPotentials.create_new_plan()

        # стр. 47 с новым планом
        expected_optimal_plan = np.array([
            [0, 0, 100, 0, 0],
            [0, 0, 0, 100, 200],
            [180, 0, 0, 0, 0],
            [20, 250, 20, 30, 0]
        ])
        np.testing.assert_allclose(methodOfPotentials.optimal_plan, expected_optimal_plan, atol=1e-5)


if __name__ == "__main__":
    unittest.main()