import operator
from os import path

with open('inputs/input09.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def part1(lines):
    next_numbers = []
    for l in lines:
        l = [int(n) for n in l.split()]
        diff_lists = []
        sub_list = l
        diff_lists.append(sub_list)
        while True:
            diffs = list(map(operator.sub, sub_list[1:], sub_list[:-1]))
            diff_lists.append(diffs)
            if all([d == 0 for d in diffs]):
                break
            sub_list = diffs
        next_numbers.append(sum([d[-1] for d in diff_lists]))
        # print(f'Next number is {next_numbers[-1]}')
    print(f'Sum of extrapolated values: {sum(next_numbers)}')

# ================ Part 2 ================


def part2(lines):
    prev_numbers = []
    for l in lines:
        l = [int(n) for n in l.split()]
        diff_lists = []
        sub_list = l
        diff_lists.append(sub_list)
        while True:
            diffs = list(map(operator.sub, sub_list[1:], sub_list[:-1]))
            diff_lists.append(diffs)
            if all([d == 0 for d in diffs]):
                break
            sub_list = diffs
        # print(diff_lists)
        diff_lists[-1].insert(0, 0)
        for d in range(len(diff_lists) - 2, -1, -1):
            diff_lists[d].insert(0, diff_lists[d][0] - diff_lists[d+1][0])

        prev_numbers.append(diff_lists[0][0])
        # print(f'Previous number is {prev_numbers[-1]}')
    print(f'Sum of extrapolated values: {sum(prev_numbers)}')


if path.isfile('test_inputs/test09.txt'):
    with open('test_inputs/test09.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('test_inputs/test09.txt'):
    with open('test_inputs/test09.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
part2(full_input_lines)
