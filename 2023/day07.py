from collections import Counter
from functools import cmp_to_key
from os import path

with open('inputs/input07.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def parse_input(lines):
    return [(l[0:5], int(l[6:])) for l in lines]


def game_classifier(game):
    x = Counter(game)
    if 5 in x.values():
        return 7  # Five of a kind
    if 4 in x.values():
        return 6  # Four of a kind
    if 3 in x.values() and 2 in x.values():
        return 5  # Full House
    if 3 in x.values():
        return 4  # Three of a kind
    if 2 in x.values():
        if list(x.values()).count(2) == 2:
            return 3  # Two pair
        return 2  # One pair
    return 1  # High Card


def game_comparator(game1, game2):
    class1 = game_classifier(game1[0])
    class2 = game_classifier(game2[0])
    # print(f'Game 1 {class1} for {game1[0]}')
    # print(f'Game 2 {class2} for {game2[0]}')
    if class1 != class2:
        return class1 - class2
    for i in range(5):
        c1, c2 = game1[0][i], game2[0][i]
        if c1 == c2:
            continue
        index1 = "23456789TJQKA".index(c1)
        index2 = "23456789TJQKA".index(c2)
        return index1 - index2
    return 0


def part1(lines):
    games = parse_input(lines)
    games = sorted(games, key=cmp_to_key(game_comparator))
    winnings = sum([(i+1) * x[1] for i, x in enumerate(games)])
    print(f'Winnings is {winnings}')


# ================ Part 2 ================


def alt_game_classifier(game):
    joker_count = game.count('J')
    game = game.replace('J', '')

    # Either four or five jokers means five of a kind
    if joker_count >= 4:
        return 7  # Five of a kind

    # We know that joker_count is 0-3

    x = Counter(game)
    if 5 - joker_count in x.values():
        return 7  # Five of a kind
    if 4 - joker_count in x.values():
        return 6  # Four of a kind

    # Three jokers and two of a kind is five of a kind
    # Three jokers and two different cards is four of a kind
    # So if we get here we know that joker_count is 0-2

    # One joker and two pair is a full house
    # Two jokers cannot give a full house:
    #    Two jokers and three of a kind is five of a kind
    #    Two jokers and one pair is four of a kind
    #    Two jokers and three different cards is three of a kind
    if joker_count == 0 and 3 in x.values() and 2 in x.values():
        return 5  # Full House
    if joker_count == 1 and 2 in x.values() and list(x.values()).count(2) == 2:
        return 5  # Full House from one joker and two pair

    if 3 - joker_count in x.values():
        return 4  # Three of a kind

    # If we get here we know that joker_count is 0-1

    if joker_count == 0 and 2 in x.values():
        if list(x.values()).count(2) == 2:
            return 3  # Two pair
        return 2  # One pair

    if joker_count == 1 and 2 in x.values() and 1 in x.values():
        return 3  # Two pair

    if joker_count == 1:
        return 2  # One pair

    return 1  # High Card


def alt_game_comparator(game1, game2):
    class1 = alt_game_classifier(game1[0])
    class2 = alt_game_classifier(game2[0])
    if class1 != class2:
        return class1 - class2
    for i in range(5):
        c1, c2 = game1[0][i], game2[0][i]
        if c1 == c2:
            continue
        index1 = "J23456789TQKA".index(c1)
        index2 = "J23456789TQKA".index(c2)
        return index1 - index2
    return 0


def part2(lines):
    games = parse_input(lines)
    games = sorted(games, key=cmp_to_key(alt_game_comparator))
    winnings = sum([(i+1) * x[1] for i, x in enumerate(games)])
    print(f'Winnings is {winnings}')


if path.isfile('inputs/test07.txt'):
    with open('inputs/test07.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('inputs/test07.txt'):
    with open('inputs/test07.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
