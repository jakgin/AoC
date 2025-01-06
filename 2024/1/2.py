import time

list1 = []
list2 = []

with open("input.txt", "r") as file:
    for line in file:
        numbers = line.strip().split()
        list1.append(int(numbers[0]))
        list2.append(int(numbers[1]))

similarity_score = 0

# Solution 1 O(n^2)
start = time.time()
for n in list1:
    similarity_score += n * list2.count(n)
end = time.time()
diff1 = end - start

print("Solution 1 similarity score:", similarity_score)

similarity_score = 0

# Solution 2 O(n)
start2 = time.time()
map = {}
for n in list2:
    if n in map:
        map[n] += 1
    else:
        map[n] = 1
for n in list1:
    if n in map:
        similarity_score += n * map[n]
end2 = time.time()
diff2 = end2 - start2

print("Solution 2 similarity score:", similarity_score)

print("Solution 1 time:", diff1)
print("Solution 2 time:", diff2)
print("How many times faster is solution 2 than solution 1:", diff1 / diff2)
