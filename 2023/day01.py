import os

with open("input01.txt", "r") as f:
    full_input_lines = f.readlines()

print('Number of lines: ' + str(len(full_input_lines)))

# ================ Part 1 ================

def part1(lines):
    code_sum = 0
    for c, l in enumerate(lines):
        if not l:
            continue
        numbers = [x for x in l if x.isdigit()]
        to_add = int(numbers[0]) * 10 + int(numbers[-1])
        code_sum += to_add

    print(f'Total Part One sum = {code_sum}')

# ================ Part 2 ================

def part2(lines):
    value_list = [['one', 1], ['two', 2], ['three', 3], ['four', 4], ['five', 5],
                  ['six', 6], ['seven', 7], ['eight', 8], ['nine', 9]]

    code_sum = 0
    for c, l in enumerate(lines):
        if not l:
            continue
        l = l.lower()
        numbers = []
        while l:
            # Numbers might overlap, e.g. twone has both "two" and "one"
            for v in value_list:
                digit_str, digit_int = v
                if l.startswith(digit_str):
                    numbers.append(digit_int)
                    break
            else:
                if l[0].isdigit():
                    numbers.append(int(l[0]))
            l = l[1:]
        to_add = numbers[0] * 10 + numbers[-1]
        code_sum += to_add

    print(f'Total Part Two sum = {code_sum}')


if os.path.isfile('test01_A.txt'):
    with open("test01_A.txt", "r") as f:
        test_input_lines = f.readlines()
        print('TEST INPUT PART 1')
        part1(test_input_lines)

if os.path.isfile('test01_B.txt'):
    with open("test01_B.txt", "r") as f:
        test_input_lines = f.readlines()
        print('TEST INPUT PART 2')
        part2(test_input_lines)

part1(full_input_lines)
part2(full_input_lines)
