
def is_symbol(txt):
    return txt != '.' and not txt.isdigit()


class Number(object):

    def __init__(self, row, start, end):
        self.row = row
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Number({self.row}, {self.start}, {self.end})"

    def value(self, lines):
        return int(lines[self.row][self.start:(self.end+1)])

    def is_part_number(self, lines):

        max_col = len(lines[self.row]) - 1
        max_row = len(lines) - 1

        if self.row > 0:
            line_above = lines[self.row - 1]
            for i in range(self.start, self.end+1):
                if is_symbol(line_above[i]):
                    return True

            if self.start > 0 and is_symbol(line_above[self.start-1]):
                return True
            if self.end < max_col and is_symbol(line_above[self.end+1]):
                return True

        if self.row < max_row:
            line_below = lines[self.row + 1]
            for i in range(self.start, self.end+1):
                if is_symbol(line_below[i]):
                    return True

            if self.start > 0 and is_symbol(line_below[self.start-1]):
                return True
            if self.end < max_col and is_symbol(line_below[self.end+1]):
                return True

        my_line = lines[self.row]
        if self.start > 0 and is_symbol(my_line[self.start-1]):
            return True
        if self.end < max_col and is_symbol(my_line[self.end+1]):
            return True

        return False


def find_numbers(lines):
    numbers = []
    for row, line in enumerate(lines):
        i = 0
        while i < len(line):
            if line[i].isdigit():
                start = i
                end = i

                while i+1 < len(line) and line[i+1].isdigit():
                    i += 1
                    end += 1

                numbers.append(Number(row, start, end))
            i += 1

    return numbers


class Gear(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Gear({self.row}, {self.col})"

    def get_adjacent_numbers(self, numbers):
        result = []
        for number in numbers:
            if abs(number.row - self.row) <= 1 and \
               number.end >= self.col - 1 and \
               number.start <= self.col + 1:
                result.append(number)
        return result


def find_gears(lines):
    gears = []
    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == '*':
                gears.append(Gear(row, col))
    return gears


def solve_part1(lines):
    numbers = find_numbers(lines)

    total = 0
    for i, number in enumerate(numbers):
        value = number.value(lines)
        is_part_number = number.is_part_number(lines)
        print(f"{i}: {value} => {is_part_number}")
        if is_part_number:
            total += value

    print(f"Total: {total}")


def solve_part2(lines):
    numbers = find_numbers(lines)
    gears = find_gears(lines)

    total = 0
    for gear in gears:
        adjacent = gear.get_adjacent_numbers(numbers)
        if len(adjacent) == 2:
            gear_ratio = adjacent[0].value(lines) * adjacent[1].value(lines)
            total += gear_ratio

    print(f"Total = {total}")


### Go! ###

#file_name = "data/day03/test.txt"
file_name = "data/day03/input.txt"
with open(file_name) as fp:
    lines = fp.readlines()

lines = [line.strip() for line in lines if len(line.strip()) > 0]

solve_part1(lines)
solve_part2(lines)
