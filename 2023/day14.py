from copy import deepcopy
from os import path

with open('inputs/input14.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day14:
    def __init__(self, lines):
        self.board = self.read_board(lines)
        self.board_len = len(self.board)
        self.row_len = len(self.board[0])

    def dump_board(self):
        print('\nBoard is:')
        for b in self.board:
            print(''.join(b))

    def read_board(self, lines):
        board = []
        for l in lines:
            board.append(list(l))
        return board

    def get_score(self):
        total_score = 0
        for row_num, board_row in enumerate(self.board):
            total_score += sum([self.board_len - row_num if x == 'O' else 0 for x in board_row])
        return total_score

    def tilt_north(self):
        changed = True
        while changed:
            changed = False
            for row in range(self.board_len - 1):
                for col in range(self.row_len):
                    if self.board[row][col] == '.' and self.board[row+1][col] == 'O':
                        self.board[row][col] = 'O'
                        self.board[row+1][col] = '.'
                        changed = True

    def tilt_south(self):
        changed = True
        while changed:
            changed = False
            for row in range(self.board_len - 2, -1, -1):
                for col in range(self.row_len):
                    if self.board[row][col] == 'O' and self.board[row+1][col] == '.':
                        self.board[row][col] = '.'
                        self.board[row+1][col] = 'O'
                        changed = True

    def tilt_west(self):
        changed = True
        while changed:
            changed = False
            for col in range(self.row_len - 1):
                for row in range(self.board_len):
                    if self.board[row][col] == '.' and self.board[row][col+1] == 'O':
                        self.board[row][col] = 'O'
                        self.board[row][col+1] = '.'
                        changed = True

    def tilt_east(self):
        changed = True
        while changed:
            changed = False
            for col in range(self.row_len - 2, -1, -1):
                for row in range(self.board_len):
                    if self.board[row][col] == 'O' and self.board[row][col+1] == '.':
                        self.board[row][col] = '.'
                        self.board[row][col+1] = 'O'
                        changed = True

    def part1(self):
        self.tilt_north()
        score = self.get_score()
        print(f'Total load is {score}')

    def one_cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def look_for_cycles(self):
        before_range = deepcopy(self.board)
        for x in range(1000):
            self.one_cycle()
            if self.board == before_range:
                print(f'Cycle of length {x+1} detected')
                return x+1
        return None

    def cycles(self, count):
        for x in range(count):
            self.one_cycle()
            # score = self.get_score()
            # print(f'Total load is {score}')
        return count

    def part2(self):
        goal = 1000000000
        print('Part 2 - running warm-up')
        goal -= self.cycles(250)
        print('Part 2 - looking for cycles')
        cycle_length = self.look_for_cycles()
        goal -= cycle_length
        goal = goal % cycle_length
        goal -= self.cycles(goal)
        score = self.get_score()
        print(f'Total load is {score}')


if path.isfile('test_inputs/test14.txt'):
    with open('test_inputs/test14.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day14(test_input_lines).part1()

if path.isfile('test_inputs/test14.txt'):
    with open('test_inputs/test14.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day14(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day14(full_input_lines).part1()
print('\nFULL INPUT PART 2')
Day14(full_input_lines).part2()
