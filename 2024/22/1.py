with open("in") as f:
    lines = f.read().strip().split("\n")


def new_secret(secret: int):
    res = secret * 64
    secret ^= res
    secret %= 16777216

    res = secret // 32
    secret ^= res
    secret %= 16777216

    res = secret * 2048
    secret ^= res
    secret %= 16777216

    return secret


ans = 0

for line in lines:
    secret = int(line)
    for i in range(2000):
        secret = new_secret(secret)
    ans += secret
    
print(ans)
