
class Puzzle(object):

    def __init__(self, lines):
        self.lines = lines

    def find_reflect_row(self):
        for row in range(len(self.lines) - 1):
            if self.can_reflect_after_row(row):
                return row
        return -1

    def find_reflect_col(self):
        for col in range(len(self.lines[0]) - 1):
            if self.can_reflect_after_col(col):
                return col
        return -1

    def find_reflect_rows_with_err(self, max_err=1):
        rows = []
        for row in range(len(self.lines) - 1):
            if self.can_reflect_after_row_with_err(row, max_err):
                rows.append(row)
        return rows

    def find_reflect_cols_with_err(self, max_err=1):
        cols = []
        for col in range(len(self.lines[0]) - 1):
            if self.can_reflect_after_col_with_err(col, max_err):
                cols.append(col)
        return cols

    def can_reflect_after_row(self, row):
        rows_before = row + 1
        rows_after = len(self.lines) - row - 1
        rows_compare = min(rows_before, rows_after)
        for i in range(rows_compare):
            if self.lines[row - i] != self.lines[row + i + 1]:
                return False
        return True

    def can_reflect_after_col(self, col):
        cols = len(self.lines[0])
        cols_before = col + 1
        cols_after = cols - col - 1
        cols_compare = min(cols_before, cols_after)
        for i in range(cols_compare):
            for row in range(len(self.lines)):
                if self.lines[row][col - i] != self.lines[row][col + i + 1]:
                    return False
        return True

    def can_reflect_after_row_with_err(self, row, max_err=1):
        rows_before = row + 1
        rows_after = len(self.lines) - row - 1
        rows_compare = min(rows_before, rows_after)

        errors = 0
        for i in range(rows_compare):
            for col in range(len(self.lines[0])):
                if self.lines[row - i][col] != self.lines[row + i + 1][col]:
                    errors += 1
                    if errors > max_err:
                        return False

        return True

    def can_reflect_after_col_with_err(self, col, max_err=1):
        cols = len(self.lines[0])
        cols_before = col + 1
        cols_after = cols - col - 1
        cols_compare = min(cols_before, cols_after)

        errors = 0
        for i in range(cols_compare):
            for row in range(len(self.lines)):
                if self.lines[row][col - i] != self.lines[row][col + i + 1]:
                    errors += 1
                    if errors > max_err:
                        return False
        return True

    def print(self):
        print("Puzzle:")
        for line in self.lines:
            print(line)


def read_all(file_name):

    puzzles = []
    with open(file_name) as fp:
        current_block = []
        while True:
            line = fp.readline()
            if len(line) == 0:
                break

            line = line.strip()
            if len(line) == 0:
                puzzles.append(Puzzle(current_block))
                current_block = []
            else:
                current_block.append(line)

        if len(current_block) > 0:
            puzzles.append(Puzzle(current_block))

    return puzzles


def solve_part1(puzzles):
    rows_total = 0
    cols_total = 0

    for puzzle in puzzles:

        col = puzzle.find_reflect_col()
        row = puzzle.find_reflect_row()
        print(f"{row} : {col}")

        if row >= 0:
            rows_total += (row + 1)
        if col >= 0:
            cols_total += (col + 1)

    total = rows_total * 100 + cols_total
    print(f"Total = {total}")


def solve_part2(puzzles):
    rows_total = 0
    cols_total = 0

    for puzzle in puzzles:

        col = puzzle.find_reflect_col()
        row = puzzle.find_reflect_row()

        cols_with_err = puzzle.find_reflect_cols_with_err()
        rows_with_err = puzzle.find_reflect_rows_with_err()
        if col >= 0:
            cols_with_err.remove(col)
        if row >= 0:
            rows_with_err.remove(row)

        print(f"{row} : {col} => {rows_with_err} : {cols_with_err}")

        if len(rows_with_err) > 0:
            rows_total += (rows_with_err[0] + 1)
        if len(cols_with_err) > 0:
            cols_total += (cols_with_err[0] + 1)

    total = rows_total * 100 + cols_total
    print(f"Total = {total}")


#file_name = "data/day13/test.txt"
file_name = "data/day13/input.txt"
puzzles = read_all(file_name)
solve_part1(puzzles)
solve_part2(puzzles)
