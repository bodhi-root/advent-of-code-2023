import numpy as np


class Card(object):

    def __init__(self, id, winning_nums, card_nums):
        self.id = id
        self.winning_nums = winning_nums
        self.card_nums = card_nums

    def get_matches(self):
        return set(self.winning_nums).intersection(set(self.card_nums))

    @staticmethod
    def parse(line):
        game_info, remainder = line.split(":")
        game_id = int(game_info.strip().split()[1])

        winning_text, card_text = remainder.split("|")
        winning_nums = [int(x.strip()) for x in winning_text.strip().split()]
        card_nums = [int(x.strip()) for x in card_text.strip().split()]

        return Card(game_id, winning_nums, card_nums)


def solve_part1(lines):
    total = 0
    for line in lines:
        card = Card.parse(line)
        matches = card.get_matches()
        value = 0 if len(matches) == 0 else 2 ** (len(matches) - 1)
        print(f"Card {card.id}: {len(matches)} => {value}")
        total += value
    print(f"Total = {total}")


def solve_part2(lines):
    # create array with number of matches for each card:
    match_counts = []
    for line in lines:
        card = Card.parse(line)
        matches = card.get_matches()
        match_counts.append(len(matches))

    # number of cards you would get if someone gave you each card:
    cumulative = [1] * len(match_counts)
    for i in range(1, len(match_counts)):
        idx = len(match_counts)-i-1
        match_count = match_counts[idx]
        if match_count > 0:
            add_idx_start = idx + 1
            add_idx_end = min(idx + match_count, len(match_counts)-1)

            j = add_idx_start
            while j <= add_idx_end:
                cumulative[idx] += cumulative[j]
                j += 1

    #print(cumulative)

    # since we get 1 copy of each card, we add up the cumulatives to see how
    # many we get total
    total = np.sum(cumulative)
    print(f"Total = {total}")


### Go! ###

file_name = "data/day04/test.txt"
file_name = "data/day04/input.txt"
with open(file_name) as fp:
    lines = fp.readlines()


solve_part1(lines)
solve_part2(lines)
