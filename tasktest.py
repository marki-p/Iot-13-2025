from list_based_priority_queue import PriorityQueue

import unittest

class TestPriorityQueue(unittest.TestCase):

    def test_ex1(self):
        test_pq = PriorityQueue()
        test_pq.enqueue("low", 1)
        test_pq.enqueue("high", 5)
        test_pq.enqueue("medium", 3)
        test_pq.enqueue("urgent", 10)
        test_pq.enqueue("high_2", 5)
        
        test_pq.view()
        
        self.assertEqual(test_pq.dequeue(), ("urgent", 10))
        self.assertEqual(test_pq.dequeue(), ("high", 5))
        self.assertEqual(test_pq.dequeue(), ("high_2", 5))
        self.assertEqual(test_pq.dequeue(), ("medium", 3))
        self.assertEqual(test_pq.dequeue(), ("low", 1))


if __name__ == "__main__":
    unittest.main()
