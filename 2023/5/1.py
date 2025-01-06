with open("in") as f:
    lines = f.read().strip().split("\n")
    lines.append("")

seeds = [int(seed) for seed in lines[0].split(" ")[1:]]

maps = []
for line in lines[3:]:
    if "map" in line:
        continue
    if line != "":
        maps.append([int(n) for n in line.split()])
    else:
        for i, seed in enumerate(seeds):
            for x, y, z in maps:
                if y <= seed < y + z:
                    seeds[i] = x + seed - y
                    break
        maps = []

print(min(seeds))
