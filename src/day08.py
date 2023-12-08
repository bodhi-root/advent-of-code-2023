import math


class Puzzle(object):

    def __init__(self, directions, nodes):
        self.directions = directions
        self.nodes = nodes

    def solve_part1(self):
        loc = 'AAA'
        idx_next = 0
        steps = 0

        while loc != 'ZZZ':
            steps += 1

            direction = self.directions[idx_next]
            idx_next += 1
            if idx_next >= len(self.directions):
                idx_next = 0

            orig_loc = loc
            if direction == 'L':
                loc = self.nodes[loc][0]
            elif direction == 'R':
                loc = self.nodes[loc][1]
            else:
                raise ValueError()

            print(f"Step {steps}: {direction} {orig_loc} => {loc}")

        print(f"Total Steps: {steps}")

    def solve_part2_brute_force(self):
        """Brute force solution (does not finish)"""
        locs = []
        print(self.nodes.keys())
        for key in self.nodes.keys():
            if key[2] == 'A':
                locs.append(key)
        print(f"Starting {locs}")

        idx_next = 0
        steps = 0

        def is_finished(locs):
            for loc in locs:
                if loc[2] != 'Z':
                    return False
            return True

        while not is_finished(locs):
            steps += 1

            direction = self.directions[idx_next]
            idx_next += 1
            if idx_next >= len(self.directions):
                idx_next = 0

            new_locs = []
            for loc in locs:
                if direction == 'L':
                    new_locs.append(self.nodes[loc][0])
                elif direction == 'R':
                    new_locs.append(self.nodes[loc][1])
                else:
                    raise ValueError()

            locs = new_locs

        print(f"Ending {locs}")
        print(f"Total Steps: {steps}")

    def find_part2_cycle(self, start):
        """Takes an individual starting location for part 2 and sees when it will
        find a location ending in 'Z'.  It was noticed while developing this that
        there is a cycle time such that it will always end on a 'Z' location after
        ```cycle * (i+1)``` where ```i``` is an integer.  We verify that this is true
        for the first 100 ending locations and then return the cycle time.
        """
        step_list = []

        loc = start
        idx_next = 0
        steps = 0

        while True:
            if loc[2] == 'Z':
                step_list.append(steps)
                if len(step_list) > 100:
                    break

            steps += 1

            direction = self.directions[idx_next]
            idx_next += 1
            if idx_next >= len(self.directions):
                idx_next = 0

            if direction == 'L':
                loc = self.nodes[loc][0]
            elif direction == 'R':
                loc = self.nodes[loc][1]
            else:
                raise ValueError()

        #print(step_list)
        for i, steps in enumerate(step_list):
            if steps != step_list[0] * (i+1):
                raise Exception("Assumption invalid!")

        return step_list[0]

    def solve_part2_cycles(self):
        """Solves part 2 using the assumption that each traveler is moving
        in a repeating pattern with a specific cycle time.  Once we have
        all the cycle times, we simply find the LCM of these values.
        """
        locs = []
        print(self.nodes.keys())
        for key in self.nodes.keys():
            if key[2] == 'A':
                locs.append(key)
        print(f"Starting {locs}")

        cycle_list = []
        for loc in locs:
            steps = self.find_part2_cycle(loc)
            cycle_list.append(steps)
            print(steps)

        #total = np.lcm.reduce(cycle_list)
        total = my_lcm_reduce(cycle_list)

        print(f"Total Steps: {total}")


def load_puzzle(file_name):
    with open(file_name) as fp:
        directions = fp.readline().strip()

        fp.readline() # empty line

        nodes = {}
        while True:
            line = fp.readline().strip()
            if len(line) == 0:
                break

            key = line[0:3]
            left = line[7:10]
            right = line[12:15]
            nodes[key] = [left, right]

    return Puzzle(directions, nodes)


# Custom LCM Code #############################################################
# This is necessary because np.lcm takes some shortcuts that result in numerical
# overflow.  This can be seen by running:
#
# np.lcm.reduce([19199, 11309, 17621, 20777, 16043, 15517])
#
# which gives an incorrect answer of 675342575.  (675342575 / 19199 = 35175.92)
# The functions below ensure everything stays in Python integers so that they
# avoid this issue.
#
# my_lcm_reduce([19199, 11309, 17621, 20777, 16043, 15517]) = 15726453850399


def my_lcm(x, y):
    """Custom version of np.lcm() that uses integer math to avoid overflow"""
    x2 = x
    y2 = y
    while x2 != y2:
        if x2 > y2:
            y2 += y * int(math.ceil((x2 - y2) / y))
        if y2 > x2:
            x2 += x * int(math.ceil((y2 - x2) / x))
    return x2


def my_lcm_reduce(x):
    """Custom version of np.lcm.reduce() that uses integer math to avoid overflow"""
    value = x[0]
    for i in range(1, len(x)):
        value = my_lcm(value, x[i])
        print(value)
    return value


# Go! #########################################################################

#file_name = "data/day08/test1.txt"
#file_name = "data/day08/test2.txt"
#file_name = "data/day08/test3.txt"
file_name = "data/day08/input.txt"

puzzle = load_puzzle(file_name)
puzzle.solve_part1()
puzzle.solve_part2_cycles()  # 15726453850399
