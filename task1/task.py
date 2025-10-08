import sys

def build_indices(edges):
    idx = {}
    nodes = []
    for u, v in edges:
        if u not in idx:
            idx[u] = len(nodes)
            nodes.append(u)
        if v not in idx:
            idx[v] = len(nodes)
            nodes.append(v)
    return idx, nodes

def compute_matrices(edges, idx, nodes, root):
    n = len(nodes)
    r1 = [[False]*n for _ in range(n)]
    r2 = [[False]*n for _ in range(n)]
    r3 = [[False]*n for _ in range(n)]
    r4 = [[False]*n for _ in range(n)]
    r5 = [[False]*n for _ in range(n)]

    children = {}
    for v in nodes:
        children[v] = []
    for u, v in edges:
        children[u].append(v)

    for u, v in edges:
        i = idx[u]
        j = idx[v]
        r1[i][j] = True
        r2[j][i] = True

    def dfs(start, cur, visited):
        for ch in children[cur]:
            if ch not in visited:
                visited.add(ch)
                dfs(start, ch, visited)

    for u in nodes:
        visited = set()
        dfs(u, u, visited)
        if u in visited:
            visited.remove(u)
        for v in visited:
            i = idx[u]
            j = idx[v]
            if not r1[i][j]:
                r3[i][j] = True
            if not r2[j][i]:
                r4[j][i] = True

    for u, vs in children.items():
        if len(vs) > 1:
            for i1 in range(len(vs)):
                for i2 in range(i1 + 1, len(vs)):
                    x = vs[i1]
                    y = vs[i2]
                    ix = idx[x]
                    iy = idx[y]
                    r5[ix][iy] = True
                    r5[iy][ix] = True

    return r1, r2, r3, r4, r5


def main():
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8-sig") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    edges = []
    for ln in lines:
        u, v = [p.strip() for p in ln.split(",", 1)]
        edges.append((u, v))

    root = sys.argv[2] if len(sys.argv) > 2 else edges[0][0]
    idx, nodes = build_indices(edges)

    r1, r2, r3, r4, r5 = compute_matrices(edges, idx, nodes, root)

    def print_mat(name, M):
        print("\n" + name)
        for row in M:
            print(" ".join("1" if x else "0" for x in row))

    print_mat("r1", r1)
    print_mat("r2", r2)
    print_mat("r3 ", r3)
    print_mat("r4", r4)
    print_mat("r5", r5)


if __name__ == "__main__":
    main()
