import unittest
import os
from task import solve

class TestGamSrv(unittest.TestCase):
    def run_test_case(self, input_data, expected_output):
        with open('gamsrv.in', 'w') as f:
            f.write(input_data)
        
        solve()
        
        with open('gamsrv.out', 'r') as f:
            result = f.read().strip()
            
        self.assertEqual(result, str(expected_output))

    def test_example_1(self):
        input_data = "6 6\n1 2 6\n1 3 10\n3 4 80\n4 5 50\n5 6 20\n2 3 40\n2 4 100\n"
        self.run_test_case(input_data, 100)

    def test_example_2(self):
        input_data = "9 12\n2 4 6\n1 2 20\n2 3 20\n3 6 20\n6 9 20\n9 8 20\n8 7 20\n7 4 20\n4 1 20\n5 2 10\n5 4 10\n5 6 10\n5 8 10\n"
        self.run_test_case(input_data, 10)

    def test_example_3(self):
        input_data = "3 2\n1 3\n1 2 50\n2 3 1000000000\n"
        self.run_test_case(input_data, 1000000000)

    def tearDown(self):
        if os.path.exists('gamsrv.in'):
            os.remove('gamsrv.in')
        if os.path.exists('gamsrv.out'):
            os.remove('gamsrv.out')

if __name__ == '__main__':
    unittest.main()
