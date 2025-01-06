with open("input.txt") as f:
    line = f.read().strip()

memory = []
for i in range(len(line)):
    for _ in range(int(line[i])):
        if i % 2 == 0:
            memory.append(i // 2)
        else:
            memory.append(".")

i = 0
j = len(memory) - 1
while i < j:
    for i in range(i, j + 1):
        if memory[i] == ".":
            break
        else:
            continue
    for j in range(j, i - 1, -1):
        if memory[j] != ".":
            break
        else:
            continue
    if i < j:
        memory[i] = memory[j]
        memory[j] = "."
    
ans = 0

for i, element in enumerate(memory):
    if element != ".":
        ans += element * i

print(ans)