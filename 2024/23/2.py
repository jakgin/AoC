from collections import defaultdict


with open("in") as f:
    lines = f.read().strip().split("\n")

connections = defaultdict(set)

for pair in lines:
    pc1 = pair[:2]
    pc2 = pair[3:]
    connections[pc1].add(pc2)
    connections[pc2].add(pc1)


def solve(pc: str, party: set):
    if connections[pc].intersection(party) != party:
        return party
    party.add(pc)
    diff = connections[pc].difference(party)
    longest_party = set()
    for n_pc in diff:
        local_party = solve(n_pc, party)
        if len(local_party) > len(longest_party):
            longest_party = local_party
    return longest_party


longest_party = set()

for pc in connections:
    party = solve(pc, set())
    if len(party) > len(longest_party):
        longest_party = party

print(",".join(sorted(list(longest_party))))
