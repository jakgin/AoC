import re


with open("in") as f:
    lines = f.read().strip().split("\n")

start_a = int(re.findall(r"\d+", lines[0])[0])
start_b = int(re.findall(r"\d+", lines[1])[0])
start_c = int(re.findall(r"\d+", lines[2])[0])
program = [int(n) for n in re.findall(r"\d+", lines[4])]

combo = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
}

a = start_a
b = start_b
c = start_c
combo[4] = a
combo[5] = b
combo[6] = c

output = []

i = 0
program_correct = True

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
        val = combo[operand] % 8
        if val != program[len(output)]:
            program_correct = False
            break
        output.append(val)
    elif inst == 6:
        b = a // (2 ** combo[operand])
        combo[5] = b
    elif inst == 7:
        c = a // (2 ** combo[operand])
        combo[6] = c
    i += 2
