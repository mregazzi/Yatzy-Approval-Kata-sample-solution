#!/usr/bin/env python3

import sys
from collections import defaultdict

def _parse_dice(dice_str):
    return [int(d) for d in dice_str.split(',')]

def _frequencies(dice):
    frequencies = defaultdict(int)
    for die in dice:
        frequencies[die] += 1
    return frequencies

def score(dice, category):
    score_function = CATEGORIES[category]
    return score_function(dice)

def chance(dice):
    return sum(dice)

def yatzy(dice):
    if 5 in _frequencies(dice).values():
        return 50
    else:
        return 0

def _number_frequency(dice, number):
    return _frequencies(dice)[number]*number

def ones(dice):
    return _number_frequency(dice, 1)

def twos(dice):
    return _number_frequency(dice, 2)

def threes(dice):
    return _number_frequency(dice, 3)

def fours(dice):
    return _number_frequency(dice, 4)

def fives(dice):
    return _number_frequency(dice, 5)

def sixes(dice):
    return _number_frequency(dice, 6)

def _n_of_a_kind(dice, n):
    frequencies = _frequencies(dice)
    for i in [6,5,4,3,2,1]:
        if frequencies[i] >= n:
            return i*n
    return 0

def pair(dice):
    return _n_of_a_kind(dice, 2)


def three_of_a_kind(dice):
    return _n_of_a_kind(dice, 3)

def four_of_a_kind(dice):
    return _n_of_a_kind(dice, 4)

def _is_straight(frequencies):
    return len(filter(lambda x: x == 1, frequencies.values())) == 5

def small_straight(dice):
    frequencies = _frequencies(dice)
    if _is_straight(frequencies) and frequencies[6] == 0:
        return sum(dice)
    else:
        return 0

def large_straight(dice):
    frequencies = _frequencies(dice)
    if _is_straight(frequencies) and frequencies[1] == 0:
        return sum(dice)
    else:
        return 0

def two_pairs(dice):
    frequencies = _frequencies(dice)
    score = 0
    if len(filter(lambda x: x >=2, frequencies.values())) == 2:
        for i in [6,5,4,3,2,1]:
            if frequencies[i] >= 2:
                score += i*2
    return score

def full_house(dice):
    frequencies = _frequencies(dice)
    if 3 in frequencies.values() and 2 in frequencies.values():
        return sum(dice)
    return 0

CATEGORIES = {"chance": chance,
              "yatzy": yatzy,
              "ones": ones, "twos": twos, "threes": threes, "fours": fours, "fives": fives, "sixes": sixes,
              "pair": pair, "threeofakind": three_of_a_kind, "fourofakind": four_of_a_kind,
              "smallstraight": small_straight, "largestraight": large_straight,
              "twopairs": two_pairs, "fullhouse": full_house}

if __name__ == "__main__":
    category = None
    if len(sys.argv) > 1:
        category = sys.argv[1]
    if not category in CATEGORIES.keys():
        print("unknown category: {}".format(category))
        sys.exit(-1)

    for dice_input in sys.stdin.readlines():
        dice_str = dice_input.strip()
        dice = _parse_dice(dice_str)
        print("""[{}] "{}": {}""".format(dice_str, category, score(dice, category)))