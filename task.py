def breadth_first_search(matrix, start, end):
    rows = len(matrix)
    if rows == 0:
        return -1
    cols = len(matrix[0])
    
    start_x, start_y = start
    end_x, end_y = end
    
    if start_x < 0 or start_x >= rows or start_y < 0 or start_y >= cols:
        return -1
    if end_x < 0 or end_x >= rows or end_y < 0 or end_y >= cols:
        return -1
        
    if matrix[start_x][start_y] == 0 or matrix[end_x][end_y] == 0:
        return -1
        
    queue = [(start_x, start_y, 0)]
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    visited[start_x][start_y] = True
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    head = 0
    while head < len(queue):
        r, c, dist = queue[head]
        head += 1
        
        if (r, c) == (end_x, end_y):
            return dist
            
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < rows and 0 <= nc < cols and \
               matrix[nr][nc] == 1 and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc, dist + 1))
                
    return -1

def main():
    input_file = "input.txt"
    output_file = "output.txt"
    
    try:
        f = open(input_file, "r")
        content = f.readlines()
        f.close()
            
        lines = []
        for line in content:
            clean_line = line.split('#')[0].strip()
            if clean_line:
                lines.append(clean_line)
            
        if len(lines) < 3:
            return
            
        start_parts = lines[0].replace(',', ' ').split()
        start = (int(start_parts[0]), int(start_parts[1]))
        
        end_parts = lines[1].replace(',', ' ').split()
        end = (int(end_parts[0]), int(end_parts[1]))
        
        matrix = []
        for i in range(3, len(lines)):
            row = [int(x) for x in lines[i].replace(',', ' ').split()]
            if row:
                matrix.append(row)
        
        if not matrix:
             return

        result = breadth_first_search(matrix, start, end)
        
        out = open(output_file, "w")
        if result != -1:
            out.write(str(result) + "\n")
        else:
            out.write("Path not found\n")
        out.close()
                
    except:
        pass

if __name__ == "__main__":
    main()
