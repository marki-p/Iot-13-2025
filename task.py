class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}
        self.count = len(nodes)

    def find(self, node):
        if self.parent[node] == node:
            return node
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            self.count -= 1
            return True
        return False

def calculate_min_cable_length(file_path):
    edges = []
    nodes = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(',')]
                if len(parts) < 3:
                    continue
                
                u, v, weight = parts[0], parts[1], int(parts[2])
                edges.append((weight, u, v))
                nodes.add(u)
                nodes.add(v)
    except (FileNotFoundError, ValueError, IndexError):
        return -1

    if not nodes:
        return 0

    edges.sort()
    
    uf = UnionFind(nodes)
    mst_weight = 0

    for weight, u, v in edges:
        if uf.union(u, v):
            mst_weight += weight

    if uf.count > 1:
        return -1

    return mst_weight

if __name__ == "__main__":
    import sys
    filename = 'communication_wells.csv'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    print(calculate_min_cable_length(filename))
