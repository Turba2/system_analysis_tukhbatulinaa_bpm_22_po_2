import json
import os
import sys

def flatten(r):
    res = []
    for x in r:
        if isinstance(x, list):
            res.extend(x)
        else:
            res.append(x)
    return res

def collect_objects(A, B):
    objs = []
    for x in flatten(A) + flatten(B):
        if x not in objs:
            objs.append(x)
    return objs

def build_blocks(r):
    blocks = []
    for el in r:
        if isinstance(el, list):
            blocks.append(el)
        else:
            blocks.append([el])
    return blocks

def build_matrix(blocks, objs):
    n = len(objs)
    pos = {o: i for i, o in enumerate(objs)}
    M = [[0] * n for _ in range(n)]

    for i, block in enumerate(blocks):
        for a in block:
            for b in block:
                M[pos[a]][pos[b]] = 1
        for right in blocks[i + 1:]:
            for a in block:
                for b in right:
                    M[pos[a]][pos[b]] = 1

    return M

def find_conflicts(MA, MB, objs):
    n = len(objs)
    conflicts = []

    for i in range(n):
        for j in range(i + 1, n):
            a1 = MA[i][j] == 1 and MA[j][i] == 0
            a2 = MA[j][i] == 1 and MA[i][j] == 0
            b1 = MB[i][j] == 1 and MB[j][i] == 0
            b2 = MB[j][i] == 1 and MB[i][j] == 0

            if (a1 and b2) or (a2 and b1):
                conflicts.append([objs[i], objs[j]])

    return conflicts

def apply_conflicts(conflicts, objs):
    used = set()
    result = []

    for obj in objs:
        if obj in used:
            continue

        group = [obj]
        for c in conflicts:
            if obj in c:
                for x in c:
                    if x != obj:
                        group.append(x)
                        used.add(x)

        used.add(obj)
        if len(group) > 1:
            group.sort()
            result.append(group)
        else:
            result.append(obj)

    return result

def load_ranking(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(result):
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def main(pathA, pathB):
    A = load_ranking(pathA)
    B = load_ranking(pathB)
    objs = collect_objects(A, B)
    blocksA = build_blocks(A)
    blocksB = build_blocks(B)
    MA = build_matrix(blocksA, objs)
    MB = build_matrix(blocksB, objs)
    conflicts = find_conflicts(MA, MB, objs)
    ranking = apply_conflicts(conflicts, objs)
    save_json({"conflicts": conflicts, "ranking": ranking})

    return json.dumps(ranking, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print(main(sys.argv[1], sys.argv[2]))