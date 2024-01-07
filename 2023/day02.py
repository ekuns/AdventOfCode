import os
import re
from itertools import chain

with open('input02.txt', 'r') as f:
    full_input_lines = f.readlines()
print(f'Number of lines: {len(full_input_lines)}')

# ================ Part 1 ================


def part_1_and_2(lines):
    game_max = {'red': 12, 'green': 13, 'blue': 14}

    total = 0
    power_total = 0
    for l in lines:
        if not l:
            continue
        x = l.split(':')
        # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        game_no = int(x[0][5:])
        games = x[1].split(';')
        regex = re.compile(r'(\d+) (red|blue|green)(, )?')
        maxes = {'red': 0, 'green': 0, 'blue': 0}
        for game in games:
            for m in regex.finditer(game.strip()):
                count = int(m.group(1))
                color = m.group(2)
                maxes[color] = max(count, maxes[color])

        if all(list(chain.from_iterable([maxes[c] <= game_max[c]] for c in ['red', 'green', 'blue']))):
            total += game_no
            # print(f'Game {game_no} passes')

        power = maxes['red'] * maxes['blue'] * maxes['green']
        # print(f'Game {game_no} power is {power}')
        power_total += power

    print(f'Total of possible games: {total}')
    print(f'Power total: {power_total}')

# ================ Part 2 ================


if os.path.isfile('test02.txt'):
    with open('test02.txt', 'r') as f:
        test_input_lines = f.readlines()
        print('TEST INPUT')
        part_1_and_2(test_input_lines)


print('FULL INPUT')
part_1_and_2(full_input_lines)
