from enum import Enum
import functools


class HandType(Enum):

    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_KIND = 6
    FIVE_OF_KIND = 7

    @staticmethod
    def cmp_high_first(x, y):
        """Compares HandType objects, sorting higher hands to front"""
        return y.value - x.value


class Hand(object):

    def __init__(self, cards, jokers=False):
        self.cards = cards
        self.type = self.get_hand_type_jokers() if jokers else self.get_hand_type()

    def get_card_counts(self):
        counts = {}
        for card in self.cards:
            if card in counts:
                counts[card] += 1
            else:
                counts[card] = 1
        return counts

    def get_hand_type(self):
        counts = self.get_card_counts()
        max_count = 0
        for count in counts.values():
            max_count = max(max_count, count)
        if max_count == 5:
            return HandType.FIVE_OF_KIND
        elif max_count == 4:
            return HandType.FOUR_OF_KIND
        elif max_count == 3:
            if len(counts) == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_KIND
        elif max_count == 2:
            if len(counts) == 3:
                return HandType.TWO_PAIR
            else:
                return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    def get_hand_type_jokers(self):
        counts = self.get_card_counts()
        joker_count = counts.pop('J', 0)
        max_count = 0
        for count in counts.values():
            max_count = max(max_count, count)

        max_count += joker_count

        if max_count == 5:
            return HandType.FIVE_OF_KIND
        elif max_count == 4:
            return HandType.FOUR_OF_KIND
        elif max_count == 3:
            if len(counts) == 2:
                return HandType.FULL_HOUSE
            else:
                return HandType.THREE_OF_KIND
        elif max_count == 2:
            if len(counts) == 3:
                return HandType.TWO_PAIR
            else:
                return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @staticmethod
    def cmp_high_first(x, y):
        """Compares Hand objects, sorting higher hands to front"""
        type_comp = HandType.cmp_high_first(x.type, y.type)
        if type_comp != 0:
            return type_comp
        for i, x_card in enumerate(x.cards):
            y_card = y.cards[i]
            diff = card_value(y_card) - card_value(x_card)
            if diff != 0:
                return diff
        return 0

    @staticmethod
    def cmp_high_first_jokers(x, y):
        """Compares Hand objects, sorting higher hands to front"""
        type_comp = HandType.cmp_high_first(x.type, y.type)
        if type_comp != 0:
            return type_comp
        for i, x_card in enumerate(x.cards):
            y_card = y.cards[i]
            diff = card_value_part2(y_card) - card_value_part2(x_card)
            if diff != 0:
                return diff
        return 0


def card_value(card):
    """Converts a character describing a card to a number.  A = 15, K = 14, ... 2=2"""
    if card == 'T':
        return 10
    if card == 'J':
        return 11
    if card == 'Q':
        return 12
    if card == 'K':
        return 13
    if card == 'A':
        return 14
    return int(card)


def card_value_part2(card):
    """Modification of card_value() that makes 'J' the weakest card"""
    value = card_value(card)
    if value == 11:
        value = 0
    return value


class HandAndBid(object):

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid

    def __repr__(self):
        return f"HandAndBid({self.hand.cards}, {self.bid})"


def read_all(file_name, jokers=False):

    with open(file_name) as fp:
        lines = fp.readlines()
        entries = []
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            cards, bid = line.split()
            entries.append(HandAndBid(Hand(cards, jokers=jokers), int(bid)))

    return entries


def solve_part1(file_name):
    entries = read_all(file_name)
    entries.sort(key=functools.cmp_to_key(lambda x, y: Hand.cmp_high_first(x.hand, y.hand)))

    total = 0
    for i, entry in enumerate(entries):
        rank = len(entries) - i
        winnings = entry.bid * rank
        print(f"{entry.hand.cards} ({entry.hand.type}) {entry.bid} => {winnings}")
        total += winnings
    print(f"Total = {total}")


def solve_part2(file_name):
    entries = read_all(file_name, jokers=True)
    entries.sort(key=functools.cmp_to_key(lambda x, y: Hand.cmp_high_first_jokers(x.hand, y.hand)))

    total = 0
    for i, entry in enumerate(entries):
        rank = len(entries) - i
        winnings = entry.bid * rank
        print(f"{entry.hand.cards} ({entry.hand.type}) {entry.bid} => {winnings}")
        total += winnings
    print(f"Total = {total}")


file_name = "data/day07/test.txt"
file_name = "data/day07/input.txt"
solve_part1(file_name) # 253910319
solve_part2(file_name)