list1 = []
list2 = []

with open("input.txt", "r") as file:
    for line in file:
        numbers = line.strip().split()
        list1.append(int(numbers[0]))
        list2.append(int(numbers[1]))

list1.sort()
list2.sort()

sum = 0
for a, b in zip(list1, list2):
    sum += abs(a - b)

print(sum)
