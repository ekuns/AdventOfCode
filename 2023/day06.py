from os import path
import math


with open('inputs/input06.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================

def parse_input(lines):
    times = [int(x) for x in lines[0][6:].split()]
    distances = [int(x) for x in lines[1][11:].split()]
    return times, distances


def part1(lines):
    times, distances = parse_input(lines)
    winning_race_counts = []
    for race_time, record_distance in zip(times, distances):  # Loop over races
        race_distances = [t * (race_time - t) for t in range(race_time + 1)]
        winning_race_count = sum([d > record_distance for d in race_distances])
        # print(f'{winning_race_count} races beat the record of {record_distance} among {race_distances}')
        winning_race_counts.append(winning_race_count)
    print(f'The product of the number of ways to beat {len(times)} races is {math.prod(winning_race_counts)}')


# ================ Part 2 ================

def alt_parse_input(lines):
    times = int(lines[0][6:].replace(' ', ''))
    distances = int(lines[1][11:].replace(' ', ''))
    return times, distances


def part2(lines):
    race_time, record_distance = alt_parse_input(lines)
    race_distances = [t * (race_time - t) for t in range(race_time + 1)]
    winning_race_count = sum([d > record_distance for d in race_distances])
    print(f'There are {winning_race_count} ways to beat race of {race_time:,} msec '
          f'with record distance {record_distance:,} mm')


if path.isfile('test_inputs/test06.txt'):
    with open('test_inputs/test06.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('test_inputs/test06.txt'):
    with open('test_inputs/test06.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
