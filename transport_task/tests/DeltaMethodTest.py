import unittest

import numpy as np

from transport_task.BasicPlanFinder import NorthWestCornerMethod, MinimalCostMethod
from transport_task.Delta import DeltaMethod
class DeltaMethodTest(unittest.TestCase):

    def test_build_column_increment_table(self):
        matrix = np.array([
            [10, 5, 34],
            [20, 1, 4],
            [19, 2, 2]])
        expected_matrix = np.array([
            [0, 4, 32],
            [10, 0, 2],
            [9, 1, 0]])
        deltaMethod = DeltaMethod(
            np.array([1]),
            np.array([1]),
            matrix)

        result = deltaMethod.build_column_increment_table()

        np.testing.assert_allclose(result, expected_matrix, atol=1e-5)

    def test_build_row_increment_table(self):
        matrix = np.array([
            [0, 4, 32],
            [10, 0, 2],
            [9, 2, 4]])
        expected_matrix = np.array([
            [0, 4, 32],
            [10, 0, 2],
            [7, 0, 2]])
        deltaMethod = DeltaMethod(
            np.array([1]),
            np.array([1]),
            matrix)

        result = deltaMethod.build_row_increment_table(matrix)

        np.testing.assert_allclose(result, expected_matrix, atol=1e-5)

    def test_assign_customer_to_supplier(self):
        pass

    def test_find_optimal_plan(self):
        supply = np.array([1000, 1700, 1600])
        demand = np.array([1600,1000,	1700])
        cost = np.array([
            [4893, 4280, 6213],
            [5327, 4296, 6188],
            [6006, 5030, 7224]])
        methodOfPotentials = MethodOfPotentials(supply, demand, cost)
        basic_plan = np.array([
            [1000, 0, 0],
            [600, 1000, 100],
            [0, 0, 1600]
        ])

        optimal_plan = methodOfPotentials.find_optimal_plan(basic_plan)

        expected_optimal_plan = np.array([
            [1000, 0, 0],
            [0, 0, 1700],
            [600, 1000, 0]
        ])
        np.testing.assert_allclose(optimal_plan, expected_optimal_plan, atol=1e-5)



if __name__ == "__main__":
    unittest.main()