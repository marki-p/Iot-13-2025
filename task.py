def compute_prefix_function(p):
    m = len(p)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and p[k] != p[q]:
            k = pi[k-1]
        if p[k] == p[q]:
            k += 1
        pi[q] = k
    return pi

def kmp_search(haystack, needle):
    if not needle:
        return []
    n = len(haystack)
    m = len(needle)
    pi = compute_prefix_function(needle)
    q = 0
    indices = []
    for i in range(n):
        while q > 0 and needle[q] != haystack[i]:
            q = pi[q-1]
        if needle[q] == haystack[i]:
            q += 1
        if q == m:
            indices.append(i - m + 1)
            q = pi[q-1]
    return indices

def main():
    try:
        with open('data.in', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) < 2:
                return
            haystack = lines[0].strip('\n\r')
            needle = lines[1].strip('\n\r')
        
        indices = kmp_search(haystack, needle)
        
        with open('data.out', 'w', encoding='utf-8') as f:
            f.write(' '.join(map(str, indices)))
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
