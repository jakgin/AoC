with open("in") as f:
    line = f.read().strip().split("\n")

time = int("".join(line[0].split()[1:]))
dis = int("".join(line[1].split()[1:]))

ans = 0

for i in range(1, time):
    if (time - i) * i > dis:
        break
ans += (time - i) - i + 1

print(ans)