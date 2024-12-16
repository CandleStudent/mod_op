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
        supply = np.array([450, 400, 150, 150, 250])
        demand = np.array([200, 300, 400, 250, 150, 100])
        cost = np.array([
            [10, 19, 17, 18, 16, 21],
            [13, 14, 11, 17, 18, 19],
            [15, 11, 7, 19, 19, 22],
            [14, 13, 12, 18, 21, 23],
            [21, 23, 10, 20, 15, 16]
            ])
        row_increment_table = np.array([
            [0, 8, 10, 1, 1, 5],
            [3, 3, 4, 0, 3, 3],
            [5, 0, 0, 2, 4, 6],
            [3, 1, 4, 0, 5, 6],
            [11, 12, 3, 3, 0, 0]
            ])
        expected_assignment_table = np.array([
            [200, 0, 0, 0, 0, 0],
            [0, 0, 0, 250, 0, 0],
            [0, 300, 400, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 150, 100]
            ])
        deltaMethod = DeltaMethod(
            supply,
            demand,
            cost)

        result = deltaMethod.assign_customer_to_supplier(row_increment_table)

        np.testing.assert_allclose(result, expected_assignment_table, atol=1e-5)

    def test_get_virtual_and_real_supply_diff(self):
        supply = np.array([450, 400, 150, 150, 250])
        demand = np.array([200, 300, 400, 250, 150, 100])
        cost = np.array([
            [10, 19, 17, 18, 16, 21],
            [13, 14, 11, 17, 18, 19],
            [15, 11, 7, 19, 19, 22],
            [14, 13, 12, 18, 21, 23],
            [21, 23, 10, 20, 15, 16]
            ])
        assignment_table = np.array([
            [200, 0, 0, 0, 0, 0],
            [0, 0, 0, 100, 0, 0],
            [0, 300, 400, 0, 0, 0],
            [0, 0, 0, 150, 0, 0],
            [0, 0, 0, 0, 150, 100]
            ])
        expected_diff = np.array([
            250, 300, -550, 0, 0
            ])
        deltaMethod = DeltaMethod(
            supply,
            demand,
            cost)

        deltaMethod.get_virtual_and_real_supply_diff(assignment_table)

        np.testing.assert_allclose(deltaMethod.supply_diff, expected_diff, atol=1e-5)


    def test_get_columns_indexes_with_cells_in_redundant_rows(self):
        supply = np.array([450, 400, 150, 150, 250])
        demand = np.array([200, 300, 400, 250, 150, 100])
        cost = np.array([
            [10, 19, 17, 18, 16, 21],
            [13, 14, 11, 17, 18, 19],
            [15, 11, 7, 19, 19, 22],
            [14, 13, 12, 18, 21, 23],
            [21, 23, 10, 20, 15, 16]
        ])
        assignment_table = np.array([
            [200, 0, 0, 0, 0, 0],
            [0, 0, 0, 100, 0, 0],
            [0, 300, 400, 0, 0, 0],
            [0, 0, 0, 150, 0, 0],
            [0, 0, 0, 0, 150, 100]
        ])
        expected_columns = np.array([
            1, 2
        ])
        deltaMethod = DeltaMethod(
            supply,
            demand,
            cost)
        deltaMethod.supply_diff = np.array([
            250, 300, -550, 0, 0
            ])

        result = deltaMethod.get_columns_indexes_with_cells_in_excessive_rows(assignment_table)

        np.testing.assert_allclose(result, expected_columns, atol=1e-5)

    def test_get_lowest_diffs_in_marked_row_column_pairs(self):
        supply = np.array([450, 400, 150, 150, 250])
        demand = np.array([200, 300, 400, 250, 150, 100])
        cost = np.array([
            [10, 19, 17, 18, 16, 21],
            [13, 14, 11, 17, 18, 19],
            [15, 11, 7, 19, 19, 22],
            [14, 13, 12, 18, 21, 23],
            [21, 23, 10, 20, 15, 16]
        ])
        assignment_table = np.array([
            [200, 0, 0, 0, 0, 0],
            [0, 0, 0, 100, 0, 0],
            [0, 300, 400, 0, 0, 0],
            [0, 0, 0, 150, 0, 0],
            [0, 0, 0, 0, 150, 100]
        ])
        row_increment_table = np.array([
            [0, 8, 10, 1, 1, 5],
            [3, 3, 4, 0, 3, 3],
            [5, 0, 0, 2, 4, 6],
            [3, 1, 4, 0, 5, 6],
            [11, 12, 3, 3, 0, 0]
        ])
        columns_with_cells_in_zero_or_excessive_rows = np.array([1, 2])
        expected_diffs = {0: 8, 1: 3, 3: 1, 4: 3}
        deltaMethod = DeltaMethod(
            supply,
            demand,
            cost)
        deltaMethod.supply_diff = np.array([
            250, 300, -550, 0, 0
            ])

        result = deltaMethod.get_lowest_diffs_in_marked_row_column_pairs(
            columns_with_cells_in_zero_or_excessive_rows, row_increment_table)

        self.assertEqual(result, expected_diffs)


    def test_find_optimal_plan(self):
        supply = np.array([450, 400, 150, 150, 250])
        demand = np.array([200, 300, 400, 250, 150, 100])
        cost = np.array([
            [10, 19, 17, 18, 16, 21],
            [13, 14, 11, 17, 18, 19],
            [15, 11, 7, 19, 19, 22],
            [14, 13, 12, 18, 21, 23],
            [21, 23, 10, 20, 15, 16]
        ])
        deltaMethod = DeltaMethod(
            supply,
            demand,
            cost)

        optimal_plan = deltaMethod.find_optimal_plan(np.array([]))

        expected_optimal_plan = np.array([
            [200, 0, 0, 100, 150, 0],
            [0, 150, 100, 150, 0, 0],
            [0, 0, 150, 0, 0, 0],
            [0, 150, 0, 0, 0, 0],
            [0, 0, 150, 0, 0, 100]
        ])

        np.testing.assert_allclose(optimal_plan, expected_optimal_plan, atol=1e-5)



if __name__ == "__main__":
    unittest.main()