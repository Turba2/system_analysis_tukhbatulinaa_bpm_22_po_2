from typing import Tuple, List, Set, Dict
import math
import sys

def task(s: str, e: str) -> Tuple[float, float]:
    edges: List[Tuple[str, str]] = []
    nodes: Set[str] = set()
    s = s.strip()
    if not s:
        return (0.0, 0.0)

    for line in s.splitlines():
        a, b = [x.strip() for x in line.split(",")]
        edges.append((a, b))
        nodes.add(a); nodes.add(b)
    root = e
    nodes.add(root)

    children: Dict[str, List[str]] = {v: [] for v in nodes}
    depth: Dict[str, int] = {root: 0}
    for u, v in edges:
        children.setdefault(u, []).append(v)

    stack = [root]
    while stack:
        u = stack.pop()
        for v in children.get(u, []):
            depth[v] = depth[u] + 1
            stack.append(v)

    def fill_desc(u: str, out: Dict[str, Set[str]]) -> Set[str]:
        acc: Set[str] = set()
        for v in children.get(u, []):
            acc.add(v)
            acc |= fill_desc(v, out)
        out[u] = acc
        return acc

    descendants: Dict[str, Set[str]] = {}
    fill_desc(root, descendants)

    r1 = set(edges)
    r2 = {(v, u) for (u, v) in edges}
    r3 = set()
    for u in nodes:
        for v in descendants.get(u, set()):
            if depth.get(v, 0) - depth.get(u, 0) >= 2:
                r3.add((u, v))
    r4 = {(v, u) for (u, v) in r3}
    r5 = set()
    for p, ch in children.items():
        for i in range(len(ch)):
            for j in range(len(ch)):
                if i != j:
                    r5.add((ch[i], ch[j]))

    rels = [r1, r2, r3, r4, r5]
    n = len(nodes)

    if n <= 1:
        return (0.0, 0.0)

    H = 0.0
    denom = n - 1
    for m in nodes:
        for R in rels:
            outdeg = sum(1 for (a, _) in R if a == m)
            p = outdeg / denom
            if p > 0:
                H += -p * math.log(p, 2)

    c = 1 / (math.e * math.log(2))
    Href = c * n * len(rels)
    h = H / Href if Href > 0 else 0

    return round(H, 1), round(h, 1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python task.py <csv_file> <root>")
        sys.exit(1)

    filename = sys.argv[1]
    root = sys.argv[2]

    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    H, h = task(data, root)
    print(H, h)
