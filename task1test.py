from task1 import map_cal

import unittest

class test_map_cal(unittest.TestCase):

    def test_example1(self):
        self.assertEqual(map_cal([(0, 1), (3, 5), (4, 8), (10, 12), (9, 10)]), [(0, 1), (3, 8), (9, 12)])

    def test_example2(self):
        self.assertEqual(map_cal([(2, 4), (3, 6), (8, 10), (6, 7)]), [(2, 7), (8, 10)])

if __name__ == '__main__':
    unittest.main()


 
