with open("in") as f:
    line = f.read().strip().split("\n")

times = [int(time) for time in line[0].split()[1:]]
distances = [int(dist) for dist in line[1].split()[1:]]

ans = 1

for time, dis in zip(times, distances):
    for i in range(1, time):
        if (time - i) * i > dis:
            break
    ans *= (time - i) - i + 1

print(ans)