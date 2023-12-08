import math

def count_ways_to_win(time, record):
    wins = 0
    for hold_time in range(1, time):
        distance = hold_time * (time - hold_time)
        if distance > record:
            wins += 1
    return wins

def count_ways_to_win_fast(time, record):
    # use some math (finding quadratic roots) to find answers analytically:
    #   total_time = hold_time + travel_time
    #   distance = hold_time * (travel_time) = hold_time * (total_time - hold_time)
    #   excess = distance - record = -hold_time^2 + hold_time*total_time - record
    a = -1
    b = time
    c = -record
    det = math.sqrt(b*b - (4*a*c))
    upper = (-b - det) / (2*a)
    lower = (-b + det) / (2*a)
    print(f"{lower} - {upper}")
    lower = round((int(lower) + 1 - lower) + lower) # round up but force int to next int
    upper = math.floor(upper) if upper > int(upper) else round(upper-1)
    print(f"{lower} - {upper}")
    return upper - lower + 1


def solve_part1(times, records):
    total = 1
    for i in range(len(times)):
        time = times[i]
        record = records[i]
        wins = count_ways_to_win(time, record)
        print(f"time={time}, record={record}, wins={wins}")
        total *= wins
    print(f"Product: {total}")

def solve_part2(times, records):
    time = int("".join([str(x) for x in times]))
    record = int("".join([str(x) for x in records]))
    wins = count_ways_to_win_fast(time, record)
    print(f"Ways to win = {wins}")

times = []
records = []

#file_name = "data/day06/test.txt"
file_name = "data/day06/input.txt"
with open(file_name) as fp:
    line = fp.readline().strip()
    times = [int(x) for x in line[5:].strip().split()]
    line = fp.readline().strip()
    records = [int(x) for x in line[9:].strip().split()]

solve_part1(times, records)
solve_part2(times, records)

