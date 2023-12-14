

class Location(object):

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def up(self):
        return Location(self.row - 1, self.col)

    def down(self):
        return Location(self.row + 1, self.col)

    def left(self):
        return Location(self.row, self.col - 1)

    def right(self):
        return Location(self.row, self.col + 1)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __repr__(self):
        return f"Location({self.row}, {self.col})"


class Maze(object):

    def __init__(self, lines):
        self.lines = lines

    def print(self):
        for line in self.lines:
            line = line.replace('.', ' ') # '...' doesn't print correctly
            print(line)

    def is_valid(self, loc):
        return 0 <= loc.row < len(self.lines) and \
               0 <= loc.col < len(self.lines[loc.row])

    def get(self, loc):
        return self.lines[loc.row][loc.col]

    def find_start(self):
        for row, line in enumerate(self.lines):
            for col, ch in enumerate(line):
                if ch == 'S':
                    return Location(row, col)
        raise ValueError("'S' not found")

    def find_start_adjacent(self, start_loc):
        locs = []

        left = start_loc.left()
        right = start_loc.right()
        up = start_loc.up()
        down = start_loc.down()

        if self.is_valid(left) and self.get(left) in ['-', 'L' 'F']:
            locs.append(left)
        if self.is_valid(right) and self.get(right) in ['-', '7', 'J']:
            locs.append(right)
        if self.is_valid(up) and self.get(up) in ['|', '7', 'F']:
            locs.append(up)
        if self.is_valid(down) and self.get(down) in ['|', 'L', 'J']:
            locs.append(down)

        if len(locs) != 2:
            raise ValueError("Starting position does not have exactly 2 adjacent paths!")

        return locs

    def find_adjacent(self, loc):
        ch = self.get(loc)
        if ch == '-':
            return [loc.left(), loc.right()]
        if ch == '|':
            return [loc.up(), loc.down()]
        if ch == 'L':
            return [loc.up(), loc.right()]
        if ch == 'J':
            return [loc.up(), loc.left()]
        if ch == 'F':
            return [loc.down(), loc.right()]
        if ch == '7':
            return [loc.left(), loc.down()]
        raise ValueError(f"Undefined symbol: '{ch}'")

    def extend_path(self, path):
        options = self.find_adjacent(path[-1])
        for loc in options:
            if loc != path[-2]:
                path.append(loc)
                return
        raise Exception("Unable to extend path")

    def solve_part1(self):
        start_loc = self.find_start()
        next_locs = self.find_start_adjacent(start_loc)

        path1 = [start_loc, next_locs[0]]
        path2 = [start_loc, next_locs[1]]

        while path1[-1] != path2[-1]:
            self.extend_path(path1)
            self.extend_path(path2)

        distance = len(path1) - 1
        print(f"Distance {distance}")



def load_maze(file_name):
    with open(file_name) as fp:
        lines = fp.readlines()
    lines = [line.strip() for line in lines]
    return Maze(lines)


file_name = "data/day10/test.txt"
file_name = "data/day10/test2.txt"
file_name = "data/day10/input.txt"

maze = load_maze(file_name)
#maze.print()
#start = maze.find_start()
#print(start)

maze.solve_part1()
