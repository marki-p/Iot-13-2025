import unittest
from task import kmp_search

class TestKMPSearch(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(kmp_search("hello world", "world"), [6])

    def test_ex2(self):
        self.assertEqual(kmp_search("abcabcabc", "abc"), [0, 3, 6])

    def test_ex3(self):
        self.assertEqual(kmp_search("hello world", "python"), [])

    def test_ex4(self):
        self.assertEqual(kmp_search("abababa", "aba"), [0, 2, 4])

    def test_ex5(self):
        self.assertEqual(kmp_search("hello", ""), [])

    def test_ex6(self):
        self.assertEqual(kmp_search("", "needle"), [])

    def test_ex7(self):
        self.assertEqual(kmp_search("", ""), [])

    def test_ex8(self):
        self.assertEqual(kmp_search("abc", "abcdef"), [])

    def test_ex9(self):
        self.assertEqual(kmp_search("aaaaa", "aa"), [0, 1, 2, 3])

if __name__ == '__main__':
    unittest.main()
