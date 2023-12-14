
def calc_checksum(line):
    result = []
    parts = line.split('.')
    for part in parts:
        if len(part) > 0 and part[0] == '#':
            result.append(len(part))
    return result


def verify_checksum(line, checksum):
    calculated = calc_checksum(line)
    if len(calculated) != len(checksum):
        return False
    for i, ch in enumerate(calculated):
        if ch != checksum[i]:
            return False
    return True


def count_occurs(values, target):
    """Count the number of time the given value appears in the list.
    (Also counts chars in a string)"""
    count = 0
    for value in values:
        if value == target:
            count += 1
    return count


def get_indexes(values, target):
    """Returns a list of indices where the given value appears in the list"""
    indexes = []
    for i, value in enumerate(values):
        if value == target:
            indexes.append(i)

    return indexes


def explore_permutation_tree(collection, visitor, path=[]):
    """Creates permutations of values from the ```collection```, calling a visitor
    function each time a new permutation is created.  At the first level of the
    tree the visitor will be called ```len(collection)``` times with an array containing
    a single value from the collection.  If the visitor returns True, this path
    will be explored further.  The next level of the tree will have a two-element
    array containing all two-element permutations of the collection.  This continues
    as deep into the tree as the visitor would like.  The tree is explored in a
    depth-first search.

    We can print all 4 digit binary numbers with the visitor:

    def print_values(values):
        if len(values) == 4:
            print(values)
        return len(values) < 4  # do not continue past length 4

    explore_permutation_tree([0,1], print_values)
    """
    for value in collection:
        path.append(value)
        if visitor(path):
            explore_permutation_tree(collection, visitor, path)
        path.pop(len(path)-1)


class PermutationExplorer(object):

    def __init__(self, line, checksum):
        self.line = line
        self.checksum = checksum

        self.checksum_total = 0
        for x in checksum:
            self.checksum_total += x
        self.pound_signs_needed = self.checksum_total - count_occurs(line, '#')

        self.unknown_indexes = get_indexes(line, '?')
        self.count = 0

    def visit(self, values):
        # we've reached a leaf naturally:
        if len(values) == len(self.unknown_indexes):
            self.visit_leaf(values)
            return False

        # if we've run out of '#'s before hitting leaf.
        # we can fill rest with '.'s and end now
        if count_occurs(values, '#') == self.pound_signs_needed:
            remainder = ['.'] * (len(self.unknown_indexes) - len(values))
            self.visit_leaf(values + remainder)
            return False

        # if we can determine there's no way to get to the checksum
        # we can just quit
        if not self.is_feasible(values):
            return False

        return True

    def is_feasible(self, values):
        test_line = self.substitute(values)

        current_checksum_idx = 0
        current_run = 0
        for ch in test_line:

            if ch == '.':
                # see if we've terminated a run of '#'.
                # if so, it must match checkum exactly
                if current_run > 0:
                    if current_run != self.checksum[current_checksum_idx]:
                        return False
                    else:
                        current_run = 0
                        current_checksum_idx += 1

            elif ch == '#':
                current_run += 1
                if current_run > self.checksum[current_checksum_idx]:
                    return False

            elif ch == '?':
                return True

        return True

    def substitute(self, values):
        chars = [ch for ch in self.line]

        #for i, replace_index in enumerate(self.unknown_indexes):
        #    chars[replace_index] = values[i]

        # the code below does not require len(values) == len(unkown_indexes):
        for i, value in enumerate(values):
            chars[self.unknown_indexes[i]] = value

        return "".join(chars)

    def visit_leaf(self, values):
        test_line = self.substitute(values)
        if verify_checksum(test_line, self.checksum):
            self.count += 1


class Entry(object):

    def __init__(self, line, checksum):
        self.line = line
        self.checksum = checksum

    def get_all_possibilities_count(self):
        explorer = PermutationExplorer(self.line, self.checksum)
        explore_permutation_tree(['#', '.'], explorer.visit)
        return explorer.count

    def __repr__(self):
        return f"Entry({self.line}, {self.checksum})"


def read_all(file_name):
    with open(file_name) as fp:
        lines = fp.readlines()
    lines = [line.strip() for line in lines]
    entries = []
    for line in lines:
        first, second = line.split(maxsplit=2)
        counts = [int(x.strip()) for x in second.split(",")]
        entries.append(Entry(first, counts))

    return entries


def solve_part1(entries):
    total = 0
    for entry in entries:
        #count = len(entry.get_all_possibilities())
        count = entry.get_all_possibilities_count()
        print(count)
        total += count
    print(f"Total: {total}")


def expand_entry(entry):
    """Expand Entry object for part 2"""
    new_line = "?".join([entry.line] * 5)
    new_checksum = []
    for i in range(5):
        new_checksum.extend(entry.checksum)
    return Entry(new_line, new_checksum)


def solve_part2(entries):
    total = 0
    for entry in entries:
        expanded_entry = expand_entry(entry)
        count = expanded_entry.get_all_possibilities_count()
        print(count)
        total += count
    print(f"Total: {total}")


file_name = "data/day12/test.txt"
file_name = "data/day12/input.txt"
entries = read_all(file_name)
#print(entries)
#print(entries[1].get_all_possibilities())
solve_part1(entries)
solve_part2(entries)
