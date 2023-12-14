
class Platform(object):

    def __init__(self, values):
        self.values = values
        self.rows = len(self.values)
        self.cols = len(self.values[0])

    def tilt_up(self):
        count = 0
        for i in range(1, self.rows):
            for j in range(self.cols):
                if self.values[i][j] == 'O' and self.values[i-1][j] == '.':
                    self.values[i-1][j] = 'O'
                    self.values[i][j] = '.'
                    count += 1
        return count

    def tilt_down(self):
        count = 0
        for i in range(1, self.rows):
            for j in range(self.cols):
                if self.values[self.rows-i-1][j] == 'O' and self.values[self.rows-i][j] == '.':
                    self.values[self.rows-i][j] = 'O'
                    self.values[self.rows-i-1][j] = '.'
                    count += 1
        return count

    def tilt_left(self):
        count = 0
        for j in range(1, self.cols):
            for i in range(self.rows):
                if self.values[i][j] == 'O' and self.values[i][j-1] == '.':
                    self.values[i][j-1] = 'O'
                    self.values[i][j] = '.'
                    count += 1
        return count

    def tilt_right(self):
        count = 0
        for j in range(1, self.cols):
            for i in range(self.rows):
                if self.values[i][self.cols-j-1] == 'O' and self.values[i][self.cols-j] == '.':
                    self.values[i][self.cols-j] = 'O'
                    self.values[i][self.cols-j-1] = '.'
                    count += 1
        return count

    def spin_cycle(self):
        while self.tilt_up() > 0:
            pass
        while self.tilt_left() > 0:
            pass
        while self.tilt_down() > 0:
            pass
        while self.tilt_right() > 0:
            pass

    def get_load(self):
        total = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.values[i][j] == 'O':
                    total += (self.rows - i)
        return total

    def to_canonical_string(self):
        return "".join(["".join(row) for row in self.values])

    def print(self):
        for row in self.values:
            for ch in row:
                print(ch if ch != '.' else ' ', end="")
            print()


def read_file(file_name):
    with open(file_name) as fp:
        lines = fp.readlines()

    values = []
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            values.append([ch for ch in line])

    return Platform(values)


def solve_part1(platform):
    while platform.tilt_up() > 0:
        pass

    load = platform.get_load()
    print(f"Load = {load}")


def find_pattern(x):
    """Find the minimum length pattern that can be repeated to
    cover all of the values in x."""
    max_length = int(len(x) / 3)
    for pattern_length in range(1, max_length):
        pattern = x[0:pattern_length]
        valid = True
        for i in range(pattern_length, len(x)):
            if x[i] != pattern[i % pattern_length]:
                valid = False
                break
        if valid:
            return pattern
    return None


def solve_part2(platform):

    # brute force (too slow):
    # for t in range(1000000000):
    #     platform.spin_cycle()
    # load = platform.get_load()
    # print(f"Load = {load}")

    loads = []
    test_iterations = 1000
    for t in range(test_iterations):
        if t % 100 == 0:
            print(f"t = {t}")
        platform.spin_cycle()
        loads.append(platform.get_load())

    skip = 500
    pattern = find_pattern(loads[skip:])
    if pattern is None:
        raise Exception("No pattern found!")
    print(f"Pattern of length {len(pattern)} found!")

    remainder = 1000000000 - skip
    full_cycles = int(remainder / len(pattern))
    remainder -= (full_cycles * len(pattern))
    print(f"Load(t=1000000000) = {pattern[remainder-1]}")


#file_name = "data/day14/test.txt"
file_name = "data/day14/input.txt"

platform = read_file(file_name)
platform.print()
#solve_part1(platform)
solve_part2(platform)
