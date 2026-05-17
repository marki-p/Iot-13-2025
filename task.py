def calculate_max_wire_length(w, heights):
    n = len(heights)
    if n < 2:
        return 0.0
    dp = [[0.0, 0.0] for _ in range(n)]

    for i in range(1, n):
        dist_1_1 = (w**2 + (1 - 1)**2)**0.5
        dist_h_1 = (w**2 + (heights[i-1] - 1)**2)**0.5
        
        dp[i][0] = max(dp[i-1][0] + dist_1_1, dp[i-1][1] + dist_h_1)
        dist_1_h = (w**2 + (1 - heights[i])**2)**0.5
        dist_h_h = (w**2 + (heights[i-1] - heights[i])**2)**0.5
        
        dp[i][1] = max(dp[i-1][0] + dist_1_h, dp[i-1][1] + dist_h_h)

    return max(dp[n-1][0], dp[n-1][1])

def main():
    try:
        with open('data.in', 'r') as f_in:
            data = f_in.read().split()
        
        if not data:
            return
        
        w = int(data[0])
        heights = [int(x) for x in data[1:]]
        
        if not heights:
            return
            
        max_length = calculate_max_wire_length(w, heights)
        
        with open('data.out', 'w') as f_out:
            f_out.write("{:.2f}".format(max_length))
            
    except (ValueError, FileNotFoundError):
        pass

if __name__ == "__main__":
    main()
