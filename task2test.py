from task2 import find_donors

import unittest

class test_find_pairs(unittest.TestCase):

    def test_ex1(self):
        self.assertEqual(find_donors([200,700,1100,1500], 900), [0,1])

    def test_ex2(self):
        self.assertEqual(find_donors([300,200,400], 600), [1,2])

    def test_ex3(self):
        self.assertEqual(find_donors([300,300], 600), [0,1])

    def test_ex4(self):
        self.assertEqual(find_donors([300,5], 600), -1)

if __name__ == '__main__':
    unittest.main()
