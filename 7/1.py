from itertools import product

with open("input.txt") as f:
    lines = f.read().strip().split("\n")

ans = 0


def is_solvable(res, nums):
    prods = product(range(2), repeat=len(nums) - 1)
    for prod in prods:
        cum = nums[0]
        for i, symbol in enumerate(prod):
            if symbol == 0:
                cum += nums[i + 1]
            else:
                cum *= nums[i + 1]
        if cum == res:
            return True
    return False


for line in lines:
    nums = [int(num) for num in line.replace(":", "").split(" ")]
    if is_solvable(nums[0], nums[1:]):
        ans += nums[0]

print(ans)
