def main():
    import sys

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8-sig") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    edges = []
    idx = {}    
    nodes = []         

    for ln in lines:
        u, v = [p.strip() for p in ln.split(",", 1)]
        edges.append((u, v))
        if u not in idx:
            idx[u] = len(nodes)
            nodes.append(u)
        if v not in idx:
            idx[v] = len(nodes)
            nodes.append(v)

    n = len(nodes)
    M = [[0]*n for _ in range(n)]
    for u, v in edges:
        i, j = idx[u], idx[v]
        M[i][j] = 1  

    print(M)

if __name__ == "__main__":
    main()
