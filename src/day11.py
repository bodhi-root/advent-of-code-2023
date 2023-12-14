
class Location(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Location({self.row}, {self.col})"


class Universe(object):

    def __init__(self, lines):
        self.lines = lines

    def get_galaxy_locations(self):
        results = []
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                if ch == '#':
                    results.append(Location(row, col))
        return results

    def get_empty_rows_and_columns(self):
        empty_rows = []
        empty_cols = []

        for row, line in enumerate(self.lines):
            empty_row = True
            for ch in line:
                if ch != '.':
                    empty_row = False
                    break
            if empty_row:
                empty_rows.append(row)

        for col in range(len(self.lines[0])):
            empty_col = True
            for row in range(len(self.lines)):
                ch = self.lines[row][col]
                if ch != '.':
                    empty_col = False
                    break
            if empty_col:
                empty_cols.append(col)

        return empty_rows, empty_cols

    def expand(self):
        empty_rows, empty_cols = self.get_empty_rows_and_columns()

        empty_rows.reverse()
        for empty_row_idx in empty_rows:
            line = "".join(['.'] * len(self.lines[0]))
            self.lines.insert(empty_row_idx, line)

        empty_cols.reverse()
        for empty_col_idx in empty_cols:
            for row in range(len(self.lines)):
                line = self.lines[row]
                self.lines[row] = line[0:empty_col_idx] + "." + line[empty_col_idx:]

    def print(self):
        for line in self.lines:
            line = line.replace('.', 'x')
            print(line)

    def get_distances_between_galaxies(self):
        total = 0
        galaxy_locs = self.get_galaxy_locations()
        for i in range(len(galaxy_locs)-1):
            loc1 = galaxy_locs[i]
            for j in range(i+1, len(galaxy_locs)):
                loc2 = galaxy_locs[j]
                distance = abs(loc2.row - loc1.row) + abs(loc2.col - loc1.col)
                #print(f"{i+1} to {j+1}: {distance}")
                total += distance

        return total

    def get_distances_between_galaxies_part2(self, expand_times):
        # part2: keep track of empty_row and empty_col indices and just add to distance if we cross them
        # don't do expand()
        empty_rows, empty_cols = self.get_empty_rows_and_columns()

        total = 0
        galaxy_locs = self.get_galaxy_locations()
        for i in range(len(galaxy_locs) - 1):
            loc1 = galaxy_locs[i]
            for j in range(i + 1, len(galaxy_locs)):
                loc2 = galaxy_locs[j]
                distance = abs(loc2.row - loc1.row) + abs(loc2.col - loc1.col)

                row1, row2 = (loc1.row, loc2.row) if loc2.row > loc1.row else (loc2.row, loc1.row)
                col1, col2 = (loc1.col, loc2.col) if loc2.col > loc1.col else (loc2.col, loc1.col)

                for empty_row in empty_rows:
                    if row1 < empty_row < row2:
                        distance += expand_times - 1
                for empty_col in empty_cols:
                    if col1 < empty_col < col2:
                        distance += expand_times - 1

                # print(f"{i+1} to {j+1}: {distance}")
                total += distance

        return total


def load_universe(file_name):
    with open(file_name) as fp:
        lines = fp.readlines()
    lines = [line.strip() for line in lines]
    return Universe(lines)


def solve_part1(file_name):
    universe = load_universe(file_name)
    # universe.print()
    universe.expand()
    # universe.print()
    total = universe.get_distances_between_galaxies()
    print(total)


def solve_part2(file_name, expand_size=1000000):
    universe = load_universe(file_name)
    total = universe.get_distances_between_galaxies_part2(expand_size)
    print(total)


file_name = "data/day11/test.txt"
solve_part1(file_name)
solve_part2(file_name, 2)  # should be same as part1
solve_part2(file_name, 10)

file_name = "data/day11/input.txt"
solve_part1(file_name)
solve_part2(file_name, 2)  # should be same as part1
solve_part2(file_name)
