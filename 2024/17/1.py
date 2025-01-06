import re


with open("in") as f:
    lines = f.read().strip().split("\n")

a = int(re.findall(r"\d+", lines[0])[0])
b = int(re.findall(r"\d+", lines[1])[0])
c = int(re.findall(r"\d+", lines[2])[0])
program = [int(n) for n in re.findall(r"\d+", lines[4])]


combo = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: a,
    5: b,
    6: c,
}

output = []

i = 0
while i < len(program):
    inst = program[i]
    operand = program[i + 1]

    if inst == 0:
        a = a // (2 ** combo[operand])
        combo[4] = a
    elif inst == 1:
        b ^= operand
        combo[5] = b
    elif inst == 2:
        b = combo[operand] % 8
        combo[5] = b
    elif inst == 3:
        if a != 0:
            i = operand
            continue
    elif inst == 4:
        b ^= c
        combo[5] = b
    elif inst == 5:
        output.append(combo[operand] % 8)
    elif inst == 6:
        b = a // (2 ** combo[operand])
        combo[5] = b
    elif inst == 7:
        c = a // (2 ** combo[operand])
        combo[6] = c
    i += 2

print(",".join([str(n) for n in output]))