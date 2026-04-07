class BinaryTree:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right

def build_tree(text):
    values = text.replace("\n", " ").split()
    
    if not values: return None
    nodes = [BinaryTree(v) if v != 'N' else None for v in values]
    for i in range(len(nodes)):
        if nodes[i] is not None:
            left_i, right_i = 2 * i + 1, 2 * i + 2
            if left_i < len(nodes): nodes[i].left = nodes[left_i]
            if right_i < len(nodes): nodes[i].right = nodes[right_i]
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

def print_tree(root):
    if not root: return
    
    def get_height(node):
        if not node: return 0
        return 1 + max(get_height(node.left), get_height(node.right))

    height = get_height(root)
    width = (2 ** height - 1) * 2  # Приблизна ширина для відступів
    
    levels = []
    queue = [(root, 0, 0, width)] # node, level, left_boundary, right_boundary
    
    current_level = -1
    while queue:
        node, level, l, r = queue.pop(0)
        if level != current_level:
            levels.append([])
            current_level = level
        
        mid = (l + r) // 2
        levels[level].append((node, mid))
        
        if node:
            queue.append((node.left, level + 1, l, mid))
            queue.append((node.right, level + 1, mid, r))

    for i, level in enumerate(levels):
        # Друкуємо самі вузли
        line = [" "] * (width + 1)
        for node, pos in level:
            if node:
                val = node.value
                line[pos:pos+len(val)] = list(val)
        print("".join(line))
        
        # Друкуємо гілки (якщо це не останній рівень)
        if i < len(levels) - 1:
            branch_line = [" "] * (width + 1)
            for node, pos in level:
                if node:
                    if node.left:
                        branch_line[pos - 1] = "/"
                    if node.right:
                        branch_line[pos + 1] = "\\"
            print("".join(branch_line))

tre = """1
2 3
3 4 N 6
7 N N N N N N N"""

root = build_tree(tre)
print(postorder(root))

print("Твоє дерево:")
print_tree(root)
