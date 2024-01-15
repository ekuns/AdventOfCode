from os import path
from copy import deepcopy

with open('inputs/input10.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day10:
    def __init__(self, lines):
        # Map from last move and current board piece to next move
        self.move_map = {
            'L': {'L': 'U', 'F': 'D', '-': 'L'},
            'R': {'J': 'U', '7': 'D', '-': 'R'},
            'U': {'7': 'L', 'F': 'R', '|': 'U'},
            'D': {'J': 'L', 'L': 'R', '|': 'D'}
        }
        self.beast_pos, self.board = self.read_board(lines)
        self.initial_beast_pos = self.beast_pos
        self.row_count = len(self.board)
        self.col_count = len(self.board[0])
        self.expanded_board = []

    @staticmethod
    def read_board(lines):
        board = [list(l) for l in lines]
        beast_pos = [(c, l.index('S')) for c, l in enumerate(lines) if 'S' in l][0]
        return beast_pos, board

    def dump_board(self):
        for row in self.board:
            print(''.join(row))

    def dump_expanded_board(self):
        for row in self.expanded_board:
            print(''.join(row))

    def get_first_moves(self):
        beast_row = self.beast_pos[0]
        beast_col = self.beast_pos[1]
        to_left = self.board[beast_row][beast_col-1] if beast_col > 0 else '.'
        to_right = self.board[beast_row][beast_col+1] if beast_col < self.col_count else '.'
        up = self.board[beast_row-1][beast_col] if beast_row > 0 else '.'
        down = self.board[beast_row+1][beast_col] if beast_row < self.row_count else '.'

        next_moves = []

        if to_left == 'L' or to_left == 'F' or to_left == '-':
            next_moves.append((beast_row, beast_col-1, self.move_map['L'][to_left], 1, to_left))
        if to_right == 'J' or to_right == '7' or to_right == '-':
            next_moves.append((beast_row, beast_col+1, self.move_map['R'][to_right], 1, to_right))
        if up == '7' or up == 'F' or up == '|':
            next_moves.append((beast_row-1, beast_col, self.move_map['U'][up], 1, up))
        if down == 'J' or down == 'L' or down == '|':
            next_moves.append((beast_row+1, beast_col, self.move_map['D'][down], 1, down))

        return next_moves

    def get_next_move(self, move):
        move_row = move[0]
        move_col = move[1]
        direction = move[2]
        move_number = move[3] + 1
        next_move = self.move_map[direction]

        if direction == 'L':
            next_col = move_col - 1
            to_left = self.board[move_row][next_col] if next_col >= 0 else '.'
            return move_row, next_col, next_move[to_left], move_number, to_left
        if direction == 'R':
            next_col = move_col + 1
            to_right = self.board[move_row][next_col] if next_col < self.col_count else '.'
            return move_row, next_col, next_move[to_right], move_number, to_right
        if direction == 'U':
            next_row = move_row - 1
            up = self.board[next_row][move_col] if next_row >= 0 else '.'
            return next_row, move_col, next_move[up], move_number, up
        if direction == 'D':
            next_row = move_row + 1
            down = self.board[next_row][move_col] if next_row < self.row_count else '.'
            return next_row, move_col, next_move[down], move_number, down
        return None, None, None, None, None

    def part1(self):
        next_moves = self.get_first_moves()
        while True:
            next_moves = [self.get_next_move(move) for move in next_moves]
            if next_moves[0][0] == next_moves[1][0] and next_moves[0][1] == next_moves[1][1]:
                print(f'Simultaneous arrival after {next_moves[0][3]} moves')
                break

    def make_expanded_board(self):
        new_row = ['.', ' '] * self.col_count + ['.']
        for row in self.board:
            self.expanded_board.append(deepcopy(new_row))
            self.expanded_board.append([y for x in row for y in [' ', x]] + ['.'])

        # Fill in missing items of the expanded board
        for row_num, row in enumerate(self.expanded_board):
            for col_num, col in enumerate(row):
                if col == ' ':
                    above = self.expanded_board[row_num - 1][col_num] if row_num > 0 else '.'
                    below = self.expanded_board[row_num + 1][col_num] if row_num < 2 * self.row_count - 1 else '.'
                    left = self.expanded_board[row_num][col_num - 1] if col_num > 0 else '.'
                    right = self.expanded_board[row_num][col_num + 1] if col_num < 2 * self.col_count - 1 else '.'
                    # Only one connector will fit in this box
                    above = above == '7' or above == 'F' or above == '|' or above == 'S'
                    below = below == 'J' or below == 'L' or below == '|' or below == 'S'
                    right = right == '7' or right == 'J' or right == '-' or right == 'S'
                    left = left == 'F' or left == 'L' or left == '-' or left == 'S'
                    if above and below:
                        self.expanded_board[row_num][col_num] = '|'
                    elif above and right:
                        self.expanded_board[row_num][col_num] = 'L'
                    elif above and left:
                        self.expanded_board[row_num][col_num] = 'J'
                    elif below and right:
                        self.expanded_board[row_num][col_num] = 'F'
                    elif below and left:
                        self.expanded_board[row_num][col_num] = '7'
                    elif right and left:
                        self.expanded_board[row_num][col_num] = '-'
                    else:
                        self.expanded_board[row_num][col_num] = '.'

    def collapse_expanded_board(self):
        del self.expanded_board[0::2]
        for row in self.expanded_board:
            del row[0::2]

    def flood_fill(self, start_row, start_col):
        queue = [(start_row, start_col)]
        while queue:
            row, col = queue.pop()
            if self.expanded_board[row][col] != '.':
                continue
            self.expanded_board[row][col] = 'O'
            if row > 0:
                queue.append((row - 1, col))
            if row < len(self.expanded_board) - 1:
                queue.append((row + 1, col))
            if col > 0:
                queue.append((row, col - 1))
            if col < len(self.expanded_board[0]) - 1:
                queue.append((row, col + 1))

    def annotate_inside_tiles(self):
        count = 0
        for row in range(len(self.expanded_board)):
            for col in range(len(self.expanded_board[0])):
                inside = self.expanded_board[row][col] == '.'
                self.expanded_board[row][col] = 'I' if inside else '.'
                if inside:
                    count += 1
        return count

    def part2(self):
        # Identify the loop so we can clean out everything not part of the loop
        next_moves = self.get_first_moves()
        move_history = [self.initial_beast_pos] + next_moves
        while True:
            next_moves = [self.get_next_move(move) for move in next_moves]
            move_history.extend(next_moves)
            if next_moves[0][0] == next_moves[1][0] and next_moves[0][1] == next_moves[1][1]:
                print(f'Simultaneous arrival after {next_moves[0][3]} moves')
                break

        # Clean up board by removing anything not in the loop
        clean_move_history = [(move[0], move[1]) for move in move_history]
        for row in range(self.row_count):
            for col in range(self.col_count):
                if (row, col) not in clean_move_history:
                    self.board[row][col] = '.'
        # self.dump_board()
        self.make_expanded_board()
        # self.dump_expanded_board()
        self.flood_fill(0, 0)
        # self.dump_expanded_board()
        self.collapse_expanded_board()
        # self.dump_expanded_board()
        inside_tile_count = self.annotate_inside_tiles()
        self.dump_expanded_board()
        print(f'Inside tiles count: {inside_tile_count}')


if path.isfile('test_inputs/test10_A1.txt'):
    with open('test_inputs/test10_A1.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1A')
        Day10(test_input_lines).part1()

if path.isfile('test_inputs/test10_A2.txt'):
    with open('test_inputs/test10_A2.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1B')
        Day10(test_input_lines).part1()

if path.isfile('test_inputs/test10_B1.txt'):
    with open('test_inputs/test10_B1.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day10(test_input_lines).part2()

if path.isfile('test_inputs/test10_B2.txt'):
    with open('test_inputs/test10_B2.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day10(test_input_lines).part2()

print('\nFULL INPUT Part 1')
Day10(full_input_lines).part1()
print('\nFULL INPUT Part 2')
Day10(full_input_lines).part2()
