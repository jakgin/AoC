with open("in") as f:
    lines = f.readlines()

sol = 0

for line in lines:
    nums = [[int(n) for n in line.split(" ")]]
    while True:
        row = nums[-1]
        new_row = []
        for i in range(len(row) - 1):
            new_row.append(row[i + 1] - row[i])
        if not any(new_row):
            lower_num = 0
            for h_row in nums[::-1]:
                lower_num += h_row[-1]
            sol += lower_num
            break
        else:
            nums.append(new_row)

print(sol)
