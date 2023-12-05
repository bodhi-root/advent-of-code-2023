
class MapEntry(object):

    def __init__(self, src_start, dst_start, len_range):
        self.src_start = src_start
        self.dst_start = dst_start
        self.len_range = len_range

    def contains_source(self, src):
        return self.src_start <= src < self.src_start + self.len_range

    def contains_dest(self, dst):
        return self.dst_start <= dst < self.dst_start + self.len_range

    def source_to_dest(self, src):
        return self.dst_start + (src - self.src_start)

    def dest_to_source(self, dst):
        return self.src_start + (dst - self.dst_start)

    def get_source_range(self):
        return Range(self.src_start, self.src_start + self.len_range - 1)

    def source_range_to_dest(self, src):
        offset = self.dst_start - self.src_start
        return Range(src.start + offset, src.end + offset)


class Mapping(object):

    def __init__(self, entries):
        self.entries = entries

    def source_to_dest(self, src):
        for entry in self.entries:
            if entry.contains_source(src):
                return entry.source_to_dest(src)
        return src

    def dest_to_source(self, dst):
        for entry in self.entries:
            if entry.contains_dest(dst):
                return entry.dest_to_source(dst)
        return dst

    def source_to_dest_range(self, src_range):
        dst_ranges = []

        idx = src_range.start
        while idx <= src_range.end:

            # find next applicable MapEntry
            next_entry = None
            for entry in self.entries:
                if entry.contains_source(idx):
                    if next_entry is not None:
                        raise Exception("Overlapping mappings!")
                    else:
                        next_entry = entry
                    # if next_entry is None or entry.src_start < next_entry.src_start:
                    #     next_entry = entry

            # no MapEntry: everything in current range passes through as-is
            if next_entry is None:
                dst_ranges.append(Range(idx, src_range.end))
                idx = src_range.end + 1

            # MapEntry applies to range (idx, min(src_range.end, next_entry_src.end))
            else:
                next_entry_src = next_entry.get_source_range()

                # MapEntry starts after idx: pass everything from [idx, next_entry.start-1] through as-is:
                if next_entry_src.start > idx:
                    dst_ranges.append(Range(idx, next_entry_src.start-1))
                    idx = next_entry_src.start

                # add transformed range:
                segment = Range(idx, min(src_range.end, next_entry_src.end))
                dst_ranges.append(next_entry.source_range_to_dest(segment))
                idx = segment.end + 1

        return dst_ranges


class Puzzle(object):

    def __init__(self, seeds, mappings):
        self.seeds = seeds
        self.mappings = mappings

    def seed_to_location(self, seed):
        soil = self.mappings['seed-to-soil'].source_to_dest(seed)
        fertilizer = self.mappings['soil-to-fertilizer'].source_to_dest(soil)
        water = self.mappings['fertilizer-to-water'].source_to_dest(fertilizer)
        light = self.mappings['water-to-light'].source_to_dest(water)
        temp = self.mappings['light-to-temperature'].source_to_dest(light)
        humidity = self.mappings['temperature-to-humidity'].source_to_dest(temp)
        location = self.mappings['humidity-to-location'].source_to_dest(humidity)
        return location

    def seed_to_location_ranges(self, range_list):
        keys = [
            'seed-to-soil',
            'soil-to-fertilizer',
            'fertilizer-to-water',
            'water-to-light',
            'light-to-temperature',
            'temperature-to-humidity',
            'humidity-to-location'
        ]
        for key in keys:
            mapping = self.mappings[key]
            new_list = []
            for rng in range_list:
                new_list.extend(mapping.source_to_dest_range(rng))
            range_list = new_list

        return range_list

    def get_seeds_part2(self):
        new_seeds = []
        for i in range(0, len(self.seeds), 2):
            start = self.seeds[i]
            end = start + self.seeds[i + 1] - 1
            new_seeds.append(Range(start, end))
        return new_seeds


class Range(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Range({self.start}, {self.end})"


def load_puzzle(file_name):

    with open(file_name, "r") as fp:
        line = fp.readline()
        if not line.startswith("seeds: "):
            raise Exception("Invalid input.  Expected 'seeds:' line")

        seeds = [int(x) for x in line[7:].strip().split()]

        fp.readline()

        mappings = {}
        mapping = None

        while True:
            line = fp.readline()
            if line == '':  # eof
                break

            line = line.strip()
            if line == '':  # skip empty lines
                continue

            if line.endswith(" map:"):
                name = line.split()[0]
                mapping = Mapping([])
                mappings[name] = mapping
                continue

            dst_start, src_start, len_range = (int(x) for x in line.split())
            mapping.entries.append(MapEntry(src_start, dst_start, len_range))

        puzzle = Puzzle(seeds, mappings)
        return puzzle


def solve_part1(puzzle):
    best = None
    for seed in puzzle.seeds:
        location = puzzle.seed_to_location(seed)
        print(f"{seed} => {location}")
        best = location if best is None else min(best, location)
    print(f"Best: {best}")


def solve_part2(puzzle):

    seed_ranges = puzzle.get_seeds_part2()
    location_ranges = puzzle.seed_to_location_ranges(seed_ranges)

    best = None

    for location_range in location_ranges:
        best = location_range.start if best is None else min(location_range.start, best)
    print(f"Best: {best}")


### Go! ###

# file_name = "data/day05/test.txt"
file_name = "data/day05/input.txt"
puzzle = load_puzzle(file_name)

solve_part1(puzzle)
solve_part2(puzzle)
