from os import path

with open('inputs/input16.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day16:
    def __init__(self, lines):
        self.board = self.read_steps(lines)

    @staticmethod
    def read_steps(lines):
        return lines[0].split(',')

    def dump_board(self):
        for row in self.board:
            print(''.join(row))

    def part1(self):
        pass

    def part2(self):
        pass


if path.isfile('test_inputs/test16.txt'):
    with open('test_inputs/test16.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day16(test_input_lines).part1()

# if path.isfile('test_inputs/test16.txt'):
#     with open('test_inputs/test16.txt', 'r') as f:
#         test_input_lines = f.readlines()
#         test_input_lines = [l.strip() for l in test_input_lines]
#         print('\nTEST INPUT PART 2')
#         Day16(test_input_lines).part2()
#
# print('\nFULL INPUT PART 1')
# Day16(full_input_lines).part1()
# print('\nFULL INPUT PART 2')
# Day16(full_input_lines).part2()
