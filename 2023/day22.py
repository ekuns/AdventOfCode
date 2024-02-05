from os import path

with open('inputs/input22.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day22:
    def __init__(self, lines):
        self.board = self.parse_inputs(lines)
        self.part = 0

    @staticmethod
    def parse_inputs(lines):
        board = []
        for l in lines:
            board.append(list(l))
        return board

    def part1(self, step_count):
        self.part = 1

    def part2(self):
        self.part = 2


if path.isfile('test_inputs/test22.txt'):
    with open('test_inputs/test22.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day22(test_input_lines).part1(6)

# print('\nFULL INPUT PART 1')
# Day22(full_input_lines).part1(64)
#
# if path.isfile('test_inputs/test22.txt'):
#     with open('test_inputs/test22.txt', 'r') as f:
#         test_input_lines = f.readlines()
#         test_input_lines = [l.strip() for l in test_input_lines]
#         print('\nTEST INPUT PART 2')
#         # We cannot use interpolate_to here because we aren't taking equal-size steps
#         Day22(test_input_lines).part2()
#
# print('\nFULL INPUT PART 2')
# Day22(full_input_lines).part2()
