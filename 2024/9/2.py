with open("input.txt") as f:
    line = f.read().strip()

memory = []
for i in range(len(line)):
    for _ in range(int(line[i])):
        if i % 2 == 0:
            memory.append(str(i // 2))
        else:
            memory.append(".")

free = []
start_index = -1
for i in range(len(memory)):
    if memory[i] == ".":
        if start_index == -1:
            start_index = i
    elif start_index != -1:
        free.append((start_index, i - start_index))
        start_index = -1


def switch(memory: list[str], free: list[tuple[int]], block: list[str], block_i):
    for free_index, (index, length) in enumerate(free):
        if index > block_i:
            break
        if length < len(block):
            continue
        for i in range(index, index + len(block)):
            memory[i] = block[0]
        if length > len(block):
            free[free_index] = (index + len(block), length - len(block))
        elif length == len(block):
            free.pop(free_index)
        for i in range(block_i, block_i + len(block)):
            memory[i] = "."
        break

block = []
moved_blocks = set()
for i in range(len(memory) - 1, 0, -1):
    if memory[i].isdigit():
        if len(block) == 0:
            block.append(memory[i])
        else:
            if memory[i] == block[0]:
                block.append(memory[i])
            else:
                if block[0] not in moved_blocks:
                    switch(memory, free, block, i + 1)
                    moved_blocks.add(block[0])
                block = [memory[i]]
    elif len(block) > 0:
        if block[0] not in moved_blocks:
            switch(memory, free, block, i + 1)
            moved_blocks.add(block[0])
        block = []

ans = 0

for i, el in enumerate(memory):
    if el != ".":
        ans += int(el) * i

print(ans)
