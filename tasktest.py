import unittest
from task import breadth_first_search

class TestLabyrinth(unittest.TestCase):
    def test1(self):
        matrix = [
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 1, 0, 0, 1, 1, 0, 0, 1]
        ]
        start = (0, 0)
        end = (7, 5)
        self.assertEqual(breadth_first_search(matrix, start, end), 12)

    def test2(self):
        matrix = [
            [1, 0],
            [0, 1]
        ]
        self.assertEqual(breadth_first_search(matrix, (0, 0), (1, 1)), -1)

    def test3(self):
        matrix = [
            [1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1]
        ]
        start = (0, 0)
        end = (4, 4)
        self.assertEqual(breadth_first_search(matrix, start, end), 8)

if __name__ == "__main__":
    unittest.main()
