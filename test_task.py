import unittest
import os
from task import calculate_min_cable_length

class TestMST(unittest.TestCase):
    def create_test_file(self, content):
        path = "test_data.csv"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def tearDown(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_basic_mst(self):
        path = self.create_test_file("K1, K2, 100\nK2, K3, 150\nK1, K3, 200")
        self.assertEqual(calculate_min_cable_length(path), 250)

    def test_disconnected_graph(self):
        path = self.create_test_file("K1, K2, 100\nK3, K4, 150")
        self.assertEqual(calculate_min_cable_length(path), -1)

    def test_single_edge(self):
        path = self.create_test_file("K1, K2, 100")
        self.assertEqual(calculate_min_cable_length(path), 100)

    def test_empty_file(self):
        path = self.create_test_file("")
        self.assertEqual(calculate_min_cable_length(path), 0)

    def test_redundant_edges(self):
        path = self.create_test_file("K1, K2, 100\nK1, K2, 50")
        self.assertEqual(calculate_min_cable_length(path), 50)

    def test_malformed_data(self):
        path = self.create_test_file("K1, K2, text\nK2, K3, 100")
        self.assertEqual(calculate_min_cable_length(path), -1)

if __name__ == "__main__":
    unittest.main()
