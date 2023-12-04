

class Game(object):

    def __init__(self, id, results):
        self.id = id
        self.results = results

    @staticmethod
    def parse(line):
        game_info, result_info = line.split(":")
        game_id = int(game_info.split()[1])

        result_text_list = result_info.strip().split(";")
        results = []
        for result_text in result_text_list:
            results.append(Result.parse(result_text))

        return Game(game_id, results)

    def is_possible(self, available):
        for result in self.results:
            if not result.is_possible(available):
                return False
        return True

    def update_minimums(self, available):
        for result in self.results:
            result.update_minimums(available)

    def get_minimum_power(self):
        available = {}
        self.update_minimums(available)
        return available.get('red', 0) * \
               available.get('green', 0) * \
               available.get('blue', 0)


class Result(object):

    def __init__(self, counts):
        self.counts = counts

    @staticmethod
    def parse(text):
        counts = {}
        parts = text.split(",")
        for part in parts:
            count, color = part.split()
            counts[color.strip()] = int(count.strip())
        return Result(counts)

    def is_possible(self, available):
        for color, count in self.counts.items():
            if count > available.get(color, 0):
                return False
        return True

    def update_minimums(self, available):
        for color, count in self.counts.items():
            if count > available.get(color, 0):
                available[color] = count


def solve_part1(lines):
    available = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    total = 0
    for line in lines:
        game = Game.parse(line)
        is_possible = game.is_possible(available)
        print(f"{game.id}: {is_possible}")
        if is_possible:
            total += game.id

    print(f"Total: {total}")


def solve_part2(lines):
    total = 0
    for line in lines:
        game = Game.parse(line)
        power = game.get_minimum_power()
        print(f"Game {game.id}: {power}")
        total += power
    print(f"Total: {total}")


### Go! ###

#with open("data/day02/test.txt") as fp:
with open("data/day02/input.txt") as fp:
    lines = fp.readlines()

solve_part1(lines)
solve_part2(lines)
