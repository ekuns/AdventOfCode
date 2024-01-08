from os import path

with open('inputs/input04.txt', 'r') as f:
    full_input_lines = f.readlines()
print(f'Number of lines: {len(full_input_lines)}')

# ================ Part 1 ================


def get_numbers(string):
    length = len(string)
    return [int(string[z:z + 3]) for z in range(0, length, 3) if length >= z + 3]


def get_winning_count(string):
    colon_split = string.strip().split(':')
    line_split = colon_split[1].split('|')
    winning_numbers = get_numbers(line_split[0])
    my_numbers = get_numbers(line_split[1])
    winning_count = len([m for m in my_numbers if m in winning_numbers])
    return winning_count


def part1(lines):
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    scratchcard_points = 0
    for l in lines:
        winning_count = get_winning_count(l)
        scratchcard_points += 2 ** (winning_count - 1) if winning_count > 0 else 0

    print(f'Total scratchcard points: {scratchcard_points}')


# ================ Part 2 ================


def part2(lines):
    extra_counts = [0] * (2 * len(lines))
    total_cards = 0
    for l in lines:
        current_count = extra_counts.pop(0) + 1
        total_cards += current_count
        winning_count = get_winning_count(l)
        for i in range(winning_count):
            extra_counts[i] += current_count
    print(f'Total cards: {total_cards}')


if path.isfile('inputs/test04.txt'):
    with open('inputs/test04.txt', 'r') as f:
        test_input_lines = f.readlines()
        print('TEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('inputs/test04.txt'):
    with open('inputs/test04.txt', 'r') as f:
        test_input_lines = f.readlines()
        print('TEST INPUT PART 2')
        part2(test_input_lines)

print('FULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
