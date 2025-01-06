with open("in") as f:
    part1, part2 = f.read().strip().split("\n\n")

wires = {}
for line in part1.split("\n"):
    wire, val = line.split(": ")
    wires[wire] = int(val)

operations: dict[str, tuple[str, str, str]] = {}
for line in part2.split("\n"):
    wire1, op, wire2, _, wire3 = line.split(" ")
    operations[wire3] = (wire1, op, wire2)


def process(wire1, op, wire2):
    if op == "AND":
        return wire1 & wire2
    elif op == "OR":
        return wire1 | wire2
    else:
        return wire1 ^ wire2


def wire_val(wire):
    val = wires.get(wire)
    if val != None:
        return val
    wire1, op, wire2 = operations[wire]
    wire1_val = wire_val(wire1)
    wire2_val = wire_val(wire2)
    res = process(wire1_val, op, wire2_val)
    wires[wire] = res
    return res


outputs: list[tuple[str, int]] = []

for wire in operations:
    wire1, _, wire2 = operations[wire]
    val = wire_val(wire)
    if wire.startswith("z"):
        outputs.append((wire, val))

outputs.sort(key=lambda x: x[0])
binary = [n[1] for n in outputs]

ans = 0
for i, n in enumerate(binary):
    if n == 1:
        ans += 2 ** i
print(ans)