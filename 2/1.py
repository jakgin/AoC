with open("test.txt") as f:
    lines = f.readlines()

safe_reports = 0

for line in lines:
    report = [int(x) for x in line.strip().split()]

    if len(report) == 0:
        continue
    if len(report) == 1:
        safe_reports += 1
        continue

    if report[0] < report[1]:
        if report[1] - report[0] > 3:
            continue
        direction = "increase"
    elif report[0] > report[1]:
        if report[0] - report[1] > 3:
            continue
        direction = "decrease"
    else:
        continue

    is_safe = True
    for i in range(1, len(report) - 1):
        if direction == "increase":
            if report[i] < report[i + 1]:
                if report[i + 1] - report[i] > 3:
                    is_safe = False
                    break
            else:
                is_safe = False
                break
        else:
            if report[i] > report[i + 1]:
                if report[i] - report[i + 1] > 3:
                    is_safe = False
                    break
            else:
                is_safe = False
                break
    if is_safe:
        safe_reports += 1

print(safe_reports)
