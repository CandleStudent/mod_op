import unittest

import numpy as np

from transport_task.BasicPlanFinder import NorthWestCornerMethod, MinimalCostMethod


class BasicPlanFinderTest(unittest.TestCase):
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
        self.northWestCornerMethod = NorthWestCornerMethod(self.supply, self.demand, self.cost)
        self.minimalCostMethod = MinimalCostMethod(self.supply, self.demand, self.cost)

    def test_north_west_corner_method(self):
        basic_plan = self.northWestCornerMethod.find_path()
        expected_basic_plan = np.array([
            [100, 0, 0, 0, 0],
            [100, 200, 0, 0, 0],
            [0, 50, 120, 10, 0],
            [0, 0, 0, 120, 200]
        ])
        np.testing.assert_allclose(basic_plan, expected_basic_plan, atol=1e-5)

    def test_minimal_cost_method(self):
        basic_plan = self.minimalCostMethod.find_path()
        expected_basic_plan = np.array([
            [0, 0, 100, 0, 0],
            [0, 0, 0, 130, 170],
            [180, 0, 0, 0, 0],
            [20, 250, 20, 0, 30]
        ])
        np.testing.assert_allclose(basic_plan, expected_basic_plan, atol=1e-5)


if __name__ == "__main__":
    unittest.main()