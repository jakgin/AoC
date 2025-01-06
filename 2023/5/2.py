with open("in") as f:
    lines = f.read().strip().split("\n")
    lines.reverse()

ranges = [int(range) for range in lines[-1].split(" ")[1:]]

maps = []
map = []
for line in lines[:-1]:
    if line == "":
        continue
    if not "map" in line:
        map.append([int(n) for n in line.split()])
    else:
        maps.append(map)
        map = []

location = 0
while True:
    seed = location
    for map in maps:
        for x, y, z in map:
            if x <= seed < x + z:
                seed = y + seed - x
                break
    
    for i in range(0, len(ranges), 2):
        if ranges[i] <= seed < ranges[i] + ranges[i + 1]:
            print(location)
            exit()
    location += 1
