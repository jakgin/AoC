def main():
    with open("input.txt") as f:
        lines = f.readlines()

    safe_reports = 0
    for line in lines:
        report = [int(x) for x in line.strip().split()]

        if is_report_safe(report):
            safe_reports += 1
        else:
            for i in range(len(report)):
                modified_report = report[:i] + report[i + 1 :]
                if is_report_safe(modified_report):
                    safe_reports += 1
                    break

    print(safe_reports)


def is_report_safe(report: list[int]) -> bool:
    if len(report) == 0:
        return False
    if len(report) == 1:
        return True

    if report[0] < report[1]:
        if report[1] - report[0] > 3:
            return False
        direction = "increase"
    elif report[0] > report[1]:
        if report[0] - report[1] > 3:
            return False
        direction = "decrease"
    else:
        return False

    for i in range(1, len(report) - 1):
        if direction == "increase":
            if report[i] < report[i + 1]:
                if report[i + 1] - report[i] > 3:
                    return False
            else:
                return False
        else:
            if report[i] > report[i + 1]:
                if report[i] - report[i + 1] > 3:
                    return False
            else:
                return False
    return True


if __name__ == "__main__":
    main()
