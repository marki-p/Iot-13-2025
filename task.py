from heapq import heappush, heappop

def solve():
    try:
        with open('gamsrv.in', 'r') as f:
            line1 = f.readline().split()
            if not line1:
                return
            n, m = map(int, line1)
            
            clients = list(map(int, f.readline().split()))
            client_set = set(clients)
            
            adj = [[] for _ in range(n + 1)]
            for _ in range(m):
                u, v, w = map(int, f.readline().split())
                adj[u].append((v, w))
                adj[v].append((u, w))
    except (FileNotFoundError, ValueError):
        return

    def dijkstra(start_node):
        distances = [float('inf')] * (n + 1)
        distances[start_node] = 0
        pq = [(0, start_node)]
        
        while pq:
            d, u = heappop(pq)
            
            if d > distances[u]:
                continue
            
            for v, weight in adj[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    heappush(pq, (distances[v], v))
        return distances

    max_latency = [0] * (n + 1)
    
    for client in clients:
        distances = dijkstra(client)
        for i in range(1, n + 1):
            if distances[i] > max_latency[i]:
                max_latency[i] = distances[i]

    min_max_val = float('inf')
    for i in range(1, n + 1):
        if i not in client_set:
            if max_latency[i] < min_max_val:
                min_max_val = max_latency[i]

    with open('gamsrv.out', 'w') as f:
        f.write(str(int(min_max_val)))

if __name__ == "__main__":
    solve()
