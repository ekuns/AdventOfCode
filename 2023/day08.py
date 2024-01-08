from os import path
import math


with open('inputs/input08.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def parse_inputs(lines):
    path_map = {}
    for l in lines:
        path_map[l[0:3]] = (l[7:10], l[12:15])
    return path_map


def part1(lines):
    steps = list(lines[0])
    path_map = parse_inputs(lines[2:])
    position = 'AAA'
    step_count = 0
    while position != 'ZZZ':
        for s in steps:
            step_count += 1
            position = path_map[position][0] if s == 'L' else path_map[position][1]
            if position == 'ZZZ':
                break
    print(f'Step count to get to ZZZ = {step_count}')


# ================ Part 2 ================


def part2(lines):
    steps = list(lines[0])
    path_map = parse_inputs(lines[2:])
    positions = sorted([x for x in path_map.keys() if x.endswith('A')])
    print(f'At beginning, Position is {positions}')

    # Measure length of loop of each entry in isolation
    cycle_lengths = []
    for p in positions:
        pos = p
        step_count = 0
        while not pos.endswith('Z'):
            for s in steps:
                step_count += 1
                pos = path_map[pos][0] if s == 'L' else path_map[pos][1]
                if pos.endswith('Z'):
                    break
        print(f'Step count for {p} to complete is {step_count}')
        cycle_lengths.append(step_count)

    print(f'Total cycle length before all positions end with Z: {math.lcm(*cycle_lengths)}')


if path.isfile('test_inputs/test08_A1.txt'):
    with open('test_inputs/test08_A1.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1A')
        part1(test_input_lines)

if path.isfile('test_inputs/test08_A2.txt'):
    with open('test_inputs/test08_A2.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1B')
        part1(test_input_lines)

if path.isfile('test_inputs/test08_B.txt'):
    with open('test_inputs/test08_B.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
