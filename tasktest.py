from task import BinaryTree, postorder 

import unittest

class TestPostOrderTraversal(unittest.TestCase):

    def test_ex1(self):
        root = BinaryTree(1)
        root.left = BinaryTree(2)
        root.right = BinaryTree(3)
        
        root.left.right = BinaryTree(5)
        
        root.right.left = BinaryTree(6)
        root.right.right = BinaryTree(7)

        self.assertEqual(postorder(root), [5, 2, 6, 7, 3, 1])

if __name__ == "__main__":
    unittest.main()
