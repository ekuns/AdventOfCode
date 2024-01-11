from itertools import combinations
from os import path

with open('inputs/input11.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def read_and_expand_board(lines, expansion_factor=1):
    stars = [[row, col] for row, l in enumerate(lines) for col, ch in enumerate(l) if ch == '#']
    # print(f'Stars: {stars}')
    nrow = len(stars)
    ncol = len(lines[0])
    # print(f'nrow={nrow}, ncol={ncol}')

    expanded_rows = [row for row in range(nrow) if sum([0 if star[0] != row else 1 for star in stars]) == 0]
    expanded_cols = [col for col in range(ncol) if sum([0 if star[1] != col else 1 for star in stars]) == 0]
    # print(f'Expanded rows: {expanded_rows}')
    # print(f'Expanded cols: {expanded_cols}')

    expanded_stars = []
    for star in stars:
        nrow_add = sum([expansion_factor for x in expanded_rows if star[0] >= x])
        ncol_add = sum([expansion_factor for x in expanded_cols if star[1] >= x])
        expanded_stars.append([star[0]+nrow_add, star[1]+ncol_add])

    return nrow+len(expanded_rows), ncol+len(expanded_cols), expanded_stars


def part1(lines):
    nrow, ncol, stars = read_and_expand_board(lines, expansion_factor=1)
    # print(f'nrow={nrow}, ncol={ncol}')
    # print(f'Stars: {stars}')
    total_distance = 0
    for z, b in combinations(stars, 2):
        total_distance += abs(z[0] - b[0]) + abs(z[1] - b[1])
    print(f'Total distance of all pair = {total_distance}')


# ================ Part 2 ================


def part2(lines, expansion_factor=1):
    nrow, ncol, stars = read_and_expand_board(lines, expansion_factor=expansion_factor)
    # print(f'nrow={nrow}, ncol={ncol}')
    # print(f'Stars: {stars}')
    total_distance = 0
    for z, b in combinations(stars, 2):
        total_distance += abs(z[0] - b[0]) + abs(z[1] - b[1])
    print(f'Total distance of all pair = {total_distance}')


if path.isfile('test_inputs/test11.txt'):
    with open('test_inputs/test11.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('test_inputs/test11.txt'):
    with open('test_inputs/test11.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2 with expansion x10')
        part2(test_input_lines, expansion_factor=9)
        print('\nTEST INPUT PART 2 with expansion x100')
        part2(test_input_lines, expansion_factor=99)

print('\nFULL INPUT')
part1(full_input_lines)
part2(full_input_lines, expansion_factor=999999)
