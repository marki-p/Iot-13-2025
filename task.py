
class BinaryTree:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree(text):
    values = text.replace("\n", " ").split()
    
    if not values:
        return None

    nodes = []
    for i in values:
        try:
            nodes.append(BinaryTree(int(i)))
        except:
            nodes.append(None)

    for i in range(len(values)):
        if nodes[i] is not None:
            left_i = 2 * i + 1
            right_i = 2 * i + 2

            if left_i < len(values):
                nodes[i].left = nodes[left_i]

            if right_i < len(values):
                nodes[i].right = nodes[right_i]

    return nodes[0]


def postorder(root):
    result = []

    def dfs(node):
        if node is None:
            return
        dfs(node.left)
        dfs(node.right)
        result.append(node.value)

    dfs(root)
    return result

with open('tre.txt') as i:
    tre = i.read()

root = build_tree(tre)

print(postorder(root))
