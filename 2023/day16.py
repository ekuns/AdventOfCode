from collections import namedtuple
from os import path

with open('inputs/input16.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')

QueueEntry = namedtuple("QueueEntry", "dir row col")


class Day16:
    def __init__(self, lines):
        self.board = self.read_board(lines)
        self.row_count = len(self.board)
        self.col_count = len(self.board[0])
        self.next_moves = {
            '.': {
                'R': [('R', 0, 1)],
                'L': [('L', 0, -1)],
                'U': [('U', -1, 0)],
                'D': [('D', 1, 0)]
            },
            '/': {
                'R': [('U', -1, 0)],
                'L': [('D', 1, 0)],
                'U': [('R', 0, 1)],
                'D': [('L', 0, -1)]
            },
            '\\': {
                'R': [('D', 1, 0)],
                'L': [('U', -1, 0)],
                'U': [('L', 0, -1)],
                'D': [('R', 0, 1)]
            },
            '-': {
                'R': [('R', 0, 1)],
                'L': [('L', 0, -1)],
                'U': [('R', 0, 1), ('L', 0, -1)],
                'D': [('R', 0, 1), ('L', 0, -1)]
            },
            '|': {
                'R': [('U', -1, 0), ('D', 1, 0)],
                'L': [('U', -1, 0), ('D', 1, 0)],
                'U': [('U', -1, 0)],
                'D': [('D', 1, 0)]
            }
        }

    @staticmethod
    def read_board(lines):
        return [list(l) for l in lines]

    def dump_board(self):
        for row in self.board:
            print(''.join(row))

    def annotate_board(self, move_list, dump_board=False):
        board = [[' ' for _ in range(self.col_count)] for _ in range(self.row_count)]
        count = 0
        for move in move_list:
            if board[move.row][move.col] == ' ':
                count += 1
                board[move.row][move.col] = '#'
        if dump_board:
            for row in board:
                print(''.join(row))
        return count

    def follow_light(self, first_queue_entry):
        queue = [first_queue_entry]

        move_list = []
        while queue:
            queue_entry = queue.pop()
            if queue_entry in move_list:
                # print(f'Queue entry already executed before: {queue_entry}')
                continue

            move_list.append(queue_entry)
            cell = self.board[queue_entry.row][queue_entry.col]
            for next_move in self.next_moves[cell][queue_entry.dir]:
                # print(f'Next move: {next_move}')
                next_dir, next_row, next_col = (next_move[0], queue_entry.row + next_move[1],
                                                queue_entry.col + next_move[2])
                if 0 <= next_row < self.row_count and 0 <= next_col < self.col_count:
                    # print(f'append to queue: {next_dir}, {next_row}, {next_col}')
                    queue.append(QueueEntry(next_dir, next_row, next_col))
                # else:
                #     print(f'out of bounds: {next_row}, {next_col}')
        # print('done')
        # print(move_list)
        return self.annotate_board(move_list, dump_board=False)

    def part1(self):
        count = self.follow_light(QueueEntry('R', 0, 0))
        print(f'Total energized cells: {count}')

    def part2(self):
        counts = []
        for row in range(self.row_count):
            counts.append(self.follow_light(QueueEntry('R', row, 0)))
            counts.append(self.follow_light(QueueEntry('L', row, self.col_count - 1)))
        for col in range(self.col_count):
            counts.append( self.follow_light(QueueEntry('D', 0, col)))
            counts.append(self.follow_light(QueueEntry('U', self.row_count - 1, col)))
        print(f'Maximum energized cells: {max(counts)}')


if path.isfile('test_inputs/test16.txt'):
    with open('test_inputs/test16.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day16(test_input_lines).part1()

if path.isfile('test_inputs/test16.txt'):
    with open('test_inputs/test16.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day16(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day16(full_input_lines).part1()
print('\nFULL INPUT PART 2')
Day16(full_input_lines).part2()
