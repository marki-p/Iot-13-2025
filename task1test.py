from task1 import find_paris

import unittest

class test_find_pairs(unittest.TestCase):

    def test_ex1(self):
        self.assertEqual(find_paris([2,7,11,15], 9), [0,1])

    def test_ex2(self):
        self.assertEqual(find_paris([3,2,4], 6), [1,2])

    def test_ex3(self):
        self.assertEqual(find_paris([3,3], 6), [0,1])

    def test_ex4(self):
        self.assertEqual(find_paris([3,5], 6), -1)

if __name__ == '__main__':
    unittest.main()
