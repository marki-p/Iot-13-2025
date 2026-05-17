import unittest
from task import calculate_max_wire_length

class TestWireLength(unittest.TestCase):
    def test_ex1(self):
        w = 2
        heights = [3, 3, 3]
        result = calculate_max_wire_length(w, heights)
        self.assertAlmostEqual(result, 5.656854, places=4)
        self.assertEqual("{:.2f}".format(result), "5.66")

    def test_ex2(self):
        w = 4
        heights = [100, 2, 100, 2, 100]
        result = calculate_max_wire_length(w, heights)
        self.assertAlmostEqual(result, 396.3231, places=4)
        self.assertEqual("{:.2f}".format(result), "396.32")

    def test_ex3(self):
        w = 4
        heights = [56, 18, 17, 94, 23, 7, 21, 94, 29, 54, 44, 26, 86, 79, 4, 15, 5, 91, 25, 17, 88, 66, 28, 2, 95, 97, 60, 93, 40, 70, 75, 48, 38, 51, 34, 52, 87, 8, 62, 77, 35, 52, 3, 93, 34, 57, 51, 11, 39, 72]
        result = calculate_max_wire_length(w, heights)
        self.assertAlmostEqual(result, 2738.1785, places=3)
        self.assertEqual("{:.2f}".format(result), "2738.18")

    def test_ex4(self):
        w = 10
        heights = [100]
        result = calculate_max_wire_length(w, heights)
        self.assertEqual(result, 0.0)

    def test_ex5(self):
        w = 3
        heights = [1, 5]
        result = calculate_max_wire_length(w, heights)
        self.assertEqual(result, 5.0)

if __name__ == '__main__':
    unittest.main()
