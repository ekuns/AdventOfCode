import os
import re

with open('input03.txt', 'r') as f:
    full_input_lines = f.readlines()
print(f'Number of lines: {len(full_input_lines)}')

# ================ Part 1 ================

deltas = [(delta_x, delta_y) for delta_x in range(-1, 2) for delta_y in range(-1, 2) if delta_x != 0 or delta_y != 0]


def dump_table(is_symbol_adjacent):
    for p in is_symbol_adjacent:
        print(''.join(p))


def set_true(x, y, is_symbol_adjacent):
    # print(f'x = {x}, y = {y}')
    for dx, dy in deltas:
        is_symbol_adjacent[x + dx][y + dy] = 'T'
    return is_symbol_adjacent


def part1(lines):
    lines = [l.strip() for l in lines if l]
    is_symbol_adjacent = [list(' ' * (len(lines) + 2)) for i in range(len(lines[0]) + 2)]
    for line_no, l in enumerate(lines):
        for pos, char in enumerate(list(l)):
            if not char.isdigit() and char != '.':
                # print(f'Found symbol at {pos},{line_no}')
                is_symbol_adjacent = set_true(line_no+1, pos+1, is_symbol_adjacent)

    adjacent_sum = 0
    for line_no, l in enumerate(lines):
        offset = 0
        while True:
            m = re.search(r'(\d+)', l[offset:])
            if not m:
                break
            # print(f'Found a number in line {line_no} at offset {offset + m.start(1)}-{offset + m.end(1)-1}: {m.group(1)}')
            yes = False
            for off in range(offset + m.start(1), offset + m.end(1)):
                if is_symbol_adjacent[line_no+1][off+1] == 'T':
                    yes = True
            # print(f'Is Adjacent: {yes}')
            if yes:
                adjacent_sum += int(m.group(1))
            offset += m.end(1)
    print(f'Sum of all part numbers: {adjacent_sum}')

# ================ Part 2 ================


def part2(lines):
    lines = [l.strip() for l in lines if l]

    # Find the position of all *
    star_list = []
    for line_no, l in enumerate(lines):
        for pos, c in enumerate(list(l)):
            if c == '*':
                star_list.append((line_no, pos))

    # Find the position of all numbers
    numbers_list = []
    for line_no, l in enumerate(lines):
        offset = 0
        while True:
            m = re.search(r'(\d+)', l[offset:])
            if not m:
                break
            numbers_list.append((int(m.group(1)), line_no, list(range(offset + m.start(1), offset + m.end(1)))))
            offset += m.end(1)
    # print(numbers_list)

    # Now for each star, find out how many numbers are around it
    score = 0
    for line_no, pos in star_list:
        adj_list = []
        for number, n_line_no, n_pos_list in numbers_list:
            for dx, dy in deltas:
                if line_no + dy == n_line_no and pos + dx in n_pos_list:
                    adj_list.append(number)
                    break
        # print(f'Star at {line_no}, {pos} is adjacent to {len(adj_list)} numbers: {adj_list}')
        if len(adj_list) == 2:
            score += adj_list[0] * adj_list[1]

    print(f'Sum of all gear ratios = {score}')


if os.path.isfile('test03.txt'):
    with open('test03.txt', 'r') as f:
        test_input_lines = f.readlines()
        print('TEST INPUT PART 1')
        part1(test_input_lines)

if os.path.isfile('test03.txt'):
    with open('test03.txt', 'r') as f:
        test_input_lines = f.readlines()
        print('TEST INPUT PART 2')
        part2(test_input_lines)

print('FULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
