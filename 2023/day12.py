from os import path
from itertools import groupby


with open('inputs/input12.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def read_board(lines):
    board = []
    for l in lines:
        split1 = l.split(' ')
        springs = list(split1[0])
        counts = [int(x) for x in split1[1].split(',')]
        board.append((springs, counts))
    return board


def replace_unknowns(board, replacements):
    positions = [x for x in range(len(board)) if board[x] == '?']
    new_board = board.copy()
    for cnt, p in enumerate(positions):
        new_board[p] = replacements[cnt]
    return new_board


def check_numbers(board, counts):
    lens = []
    for k, g in groupby(board):
        if k != '#':
            continue
        count = sum([1 for _ in g])
        lens.append(count)
    return lens == counts


def unique_permutations(elements):
    if len(elements) == 1:
        yield (elements[0],)
    else:
        unique_elements = set(elements)
        for first_element in unique_elements:
            remaining_elements = list(elements)
            remaining_elements.remove(first_element)
            for sub_permutation in unique_permutations(remaining_elements):
                yield (first_element,) + sub_permutation


def part1(lines):
    total_matches = 0
    boards = read_board(lines)
    for springs, counts in boards:
        total_damaged_springs = sum(counts)
        known_damaged_springs = sum([1 if x == '#' else 0 for x in springs])
        needed_damaged_springs = total_damaged_springs - known_damaged_springs
        unknown_springs = sum([1 if x == '?' else 0 for x in springs])
        extra_items = '#' * needed_damaged_springs + '.' * (unknown_springs - needed_damaged_springs)
        successful_counts = 0
        for choice in unique_permutations(extra_items):
            new_board = replace_unknowns(springs, choice)
            if check_numbers(new_board, counts):
                successful_counts += 1
        # print(f'# successful matches = {successful_counts}')
        total_matches += successful_counts
    print(f'Total of all successful matches = {total_matches}')


# ================ Part 2 ================


def part2(lines):
    total_matches = 0
    boards = read_board(lines)
    for springs, counts in boards:
        print(springs)
        springs = springs + ['?'] + springs + ['?'] + springs + ['?'] + springs + ['?'] + springs
        counts = counts * 5

        total_damaged_springs = sum(counts)
        known_damaged_springs = sum([1 if x == '#' else 0 for x in springs])
        needed_damaged_springs = total_damaged_springs - known_damaged_springs
        unknown_springs = sum([1 if x == '?' else 0 for x in springs])
        extra_items = '#' * needed_damaged_springs + '.' * (unknown_springs - needed_damaged_springs)
        successful_counts = 0
        for choice in unique_permutations(extra_items):
            new_board = replace_unknowns(springs, choice)
            if check_numbers(new_board, counts):
                successful_counts += 1
        # print(f'# successful matches = {successful_counts}')
        total_matches += successful_counts
    print(f'Total of all successful matches = {total_matches}')


if path.isfile('test_inputs/test12.txt'):
    with open('test_inputs/test12.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('test_inputs/test12.txt'):
    with open('test_inputs/test12.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
# part2(full_input_lines)
