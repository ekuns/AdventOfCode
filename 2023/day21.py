from os import path

with open('inputs/input21.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day21:
    def __init__(self, lines):
        self.board = self.parse_inputs(lines)
        self.nrow = len(self.board)
        self.ncol = len(self.board[0])
        self.part = 0

    @staticmethod
    def parse_inputs(lines):
        board = []
        for l in lines:
            board.append(list(l))
        return board

    def dump_board(self):
        print('\nBoard is:')
        for b in self.board:
            print(''.join(b))

    def find_start(self):
        for row, b in enumerate(self.board):
            if 'S' in b:
                col = b.index('S')
                self.board[row][col] = '.'
                return {(row, col)}

    def get_next_steps(self, position_list):
        next_steps = set()
        for p in position_list:
            for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                row, col = p[0] + drow, p[1] + dcol
                check_pos = (row, col)
                if self.part == 1:
                    if row < 0 or row == self.nrow or col < 0 or col == self.ncol:
                        continue
                    board_item = self.board[row][col]
                else:
                    board_item = self.board[row % self.nrow][col % self.ncol]

                if board_item == '.':
                    next_steps.add(check_pos)
        return next_steps

    def part1(self, step_count):
        self.part = 1
        next_steps = self.find_start()
        print(f'Starting position = {next_steps}')
        for _ in range(step_count):
            next_steps = self.get_next_steps(next_steps)
        print(f'Number of possible positions after {step_count} steps is {len(next_steps)}')

    @staticmethod
    def interpolate_to_answer(numbers, destination):
        # Get a 2nd order polynomial from the first three points we have
        x1, x2, x3 = [0, 1, 2]
        y1, y2, y3 = numbers[0:3]
        # Get three coefficients a, b, c for y = a*x^2 + b*x + c
        a = (x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)) / ((x1 - x2) * (x1 - x3) * (x2 - x3))
        b = (y2 - y1) / (x2 - x1) - a * (x1 + x2)
        c = y1 - a * x1 * x1 - b * x1
        return a * destination * destination + b * destination + c

    def part2(self, step_counts, interpolate_to):
        self.part = 2
        starting_position = self.find_start()
        print(f'Starting position = {starting_position} in board that is {self.ncol} x {self.nrow}')

        # We will always get the counts in monotonic order
        last_step_count = 0
        next_steps = starting_position
        number_list = []
        for step_count in step_counts:
            for max_step in range(last_step_count, step_count):
                next_steps = self.get_next_steps(next_steps)
                # print(f'After {max_step} steps, {len(next_steps)}')
            last_step_count = step_count
            print(f'Number of possible positions after {step_count} steps is {len(next_steps)}')
            number_list.append(len(next_steps))

        print(f'Number list for 0..N is {number_list}')
        if interpolate_to != 0:
            answer = self.interpolate_to_answer(number_list, interpolate_to)
            print(f'The answer is {int(answer)}')


if path.isfile('test_inputs/test21.txt'):
    with open('test_inputs/test21.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day21(test_input_lines).part1(6)

print('\nFULL INPUT PART 1')
Day21(full_input_lines).part1(64)

if path.isfile('test_inputs/test21.txt'):
    with open('test_inputs/test21.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        # We cannot use interpolate_to here because we aren't taking equal-size steps
        Day21(test_input_lines).part2([6, 10, 50, 100, 500], 0)

print('\nFULL INPUT PART 2')
# Puzzle input is 131 x 131 -- looking for solution at 26501365 steps
# 26501365 = 202300 * 131 + 65, so let's get the solution at 65 + N*131 steps, for N=0,1,2,3...
# Then we can use a polynomial to get the solution at 65 + N*131 steps for N = 202300
Day21(full_input_lines).part2([65, 65+131, 65+2*131, 65+3*131], 202300)
