

def diff(x):
    output = [0] * (len(x) - 1)
    for i in range(len(x) - 1):
        output[i] = x[i+1] - x[i]
    return output


def is_zeros(x):
    for value in x:
        if value != 0:
            return False
    return True


def extend_series(x):

    diffs = [x.copy()]
    last_diff = diffs[-1]
    while not is_zeros(last_diff):
        last_diff = diff(last_diff)
        diffs.append(last_diff)

    last_diff.append(0)
    for i in range(1, len(diffs)):
        to_extend = diffs[len(diffs) - 1 - i]
        to_extend.append(to_extend[-1] + last_diff[-1])
        last_diff = to_extend

    return diffs[0]


def extend_series_backward(x):
    diffs = [x.copy()]
    last_diff = diffs[-1]
    while not is_zeros(last_diff):
        last_diff = diff(last_diff)
        diffs.append(last_diff)

    last_diff.insert(0, 0)
    for i in range(1, len(diffs)):
        to_extend = diffs[len(diffs) - 1 - i]
        to_extend.insert(0, to_extend[0] - last_diff[0])
        last_diff = to_extend

    return diffs[0]


def solve_part1(file_name):
    series_list = read_input(file_name)
    total = 0
    for series in series_list:
        extended = extend_series(series)
        total += extended[-1]
    print(f"Total: {total}")


def solve_part2(file_name):
    series_list = read_input(file_name)
    total = 0
    for series in series_list:
        extended = extend_series_backward(series)
        total += extended[0]
    print(f"Total: {total}")


def read_input(file_name):
    results = []
    with open(file_name) as fp:
        lines = fp.readlines()
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                break
            results.append([int(x) for x in line.split()])
    return results

file_name = "data/day09/test.txt"
file_name = "data/day09/input.txt"
solve_part1(file_name)
solve_part2(file_name)


