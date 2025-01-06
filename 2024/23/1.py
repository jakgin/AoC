from collections import defaultdict


with open("in") as f:
    lines = f.read().strip().split("\n")

connections = defaultdict(set)

for pair in lines:
    pc1 = pair[:2]
    pc2 = pair[3:]
    connections[pc1].add(pc2)
    connections[pc2].add(pc1)

trios = set()

for key, value in connections.items():
    for con in value:
        cons = connections[con]
        for con2 in cons:
            if con2 in value:
                trios.add(tuple(sorted([key, con, con2])))

correct_trios = set()

for trio in trios:
    a, b, c = trio
    if "t" in [a[0], b[0], c[0]]:
        correct_trios.add(trio)

print(len(correct_trios))


