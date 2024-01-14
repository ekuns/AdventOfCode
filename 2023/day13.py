from collections import namedtuple
from copy import deepcopy
from os import path

with open('inputs/input13.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


Skip = namedtuple("Skip", "direction pair type")


def read_boards(lines):
    boards = []
    board = []
    for l in lines:
        if l:
            board.append(list(l))
        else:
            boards.append(board)
            board = []
    if board:
        boards.append(board)
    return boards


def find_reflection(board, board_num, direction, skip=None):
    """
    Find vertical reflections in the board provided
    :param board: A 2D array representing the board
    :param board_num: Board number 0 to N-1
    :param direction: either 'vertical' or 'horizontal'
    :param skip: If not None, indicates a reflection to ignore if found
    :return: score, min row, row count; score is None if no mirror found
    """
    board_len = len(board)

    matching_pair = []
    for row1 in range(board_len):
        for row2 in range(row1+1, board_len):
            if board[row1] == board[row2]:
                matching_pair.append((row1, row2))

    # print(f'\n{board_num}: {direction} board length = {board_len}, matching pair found: {matching_pair}')

    if len(matching_pair) == 0:
        # print(f'{board_num}: No mirror found')
        return None, None, None, None

    # Did we find a reflection starting in the first row?
    for test_pair in [pair for pair in matching_pair if pair[0] == 0]:
        if skip and skip.direction == direction and skip.pair == test_pair and skip.type == 'forward':
            # print(f'Skipping previously-found forward {direction} reflection')
            continue

        # Is our match a single pair?
        if test_pair == (0, 1):
            # print(f'{board_num}: Found forward {direction} mirror, length 1, ending at {1}')
            return 1, 0, 1, Skip(direction, test_pair, 'forward')

        end_row = test_pair[1]
        row_num = 1
        while (row_num, end_row - row_num) in matching_pair:
            if row_num + 1 == end_row - row_num:
                # print(f'{board_num}: Found forward {direction} mirror, length {row_num+1}, ending at {row_num + 1}')
                return row_num + 1, 0, (row_num+1) * 2, Skip(direction, test_pair, 'forward')
            row_num += 1

    # Did we find a 2+ row reflection starting in the last row?
    for test_pair in [pair for pair in matching_pair if pair[1] == board_len - 1]:
        if skip and skip.direction == direction and skip.pair == test_pair and skip.type == 'backward':
            # print(f'Skipping previously-found backward {direction} reflection')
            continue

        # Is our match a single pair?
        if test_pair == (board_len - 2, board_len - 1):
            # print(f'{board_num}: Found backward {direction} mirror, length 1, ending at {board_len - 1}')
            return board_len - 1, board_len - 1, 1, Skip(direction, test_pair, 'backward')

        row_num = 1
        while (test_pair[0] + row_num, test_pair[1] - row_num) in matching_pair:
            if test_pair[0] + row_num + 1 == test_pair[1] - row_num:
                # print(f'{board_num}: Found backward {direction} mirror, length {row_num + 1}, ending at {test_pair[0] + row_num + 1}')
                return test_pair[0] + row_num + 1, board_len - (row_num+1) * 2, (row_num+1) * 2, Skip(direction, test_pair, 'backward')
            row_num += 1

    # print(f'{board_num}: No mirror found')
    return None, None, None, None


def check_horizontal_and_vertical(board, board_num, skip=None):
    # Search for horizontal reflections
    direction = 'vertical'
    reflection, start, length, new_skip = find_reflection(board, board_num, direction, skip=skip)
    if reflection is not None:
        return reflection * 100, direction, start, length, new_skip
    else:
        # Flip the board across the diagonal so we can use the same code to search
        # for vertical reflections
        board = list(zip(*board))
        direction = 'horizontal'
        reflection, start, length, new_skip = find_reflection(board, board_num, direction, skip=skip)
        if reflection is not None:
            return reflection, direction, start, length, new_skip
        else:
            return None, None, None, None, None


def part1(lines):
    boards = read_boards(lines)
    scores = [check_horizontal_and_vertical(board, board_num) for board_num, board in enumerate(boards)]
    # for board_num, (score, direction, start, length, skip) in enumerate(scores):
    #     if score is None:
    #         print(f'{board_num}: No mirror found')
    #     else:
    #         print(f'{board_num}: Found {direction} mirror from {start} to {start + length - 1}')

    total_sum = sum([score[0] for score in scores if score[0]])
    print(f'Total summary: {total_sum}')


# ================ Part 2 ================


def dump_board(board):
    for b in board:
        print(''.join(b))


def try_all_smudges(board, board_num):
    # First locate the original mirror
    orig_score, orig_dir, orig_start, orig_length, skip = check_horizontal_and_vertical(board, board_num)

    # Now try to change each smudge one at a time
    for row in range(len(board)):
        for col in range(len(board[0])):
            # print(f'Checking {row},{col}')
            new_board = deepcopy(board)
            # dump_board(new_board)
            new_board[row][col] = '#' if board[row][col] == '.' else '.'
            score, dir, start, length, _ = check_horizontal_and_vertical(new_board, board_num, skip=skip)
            if score:
                return score

    print(f'{board_num}: No new mirror found')
    return None


def part2(lines):
    boards = read_boards(lines)
    total_sum = 0
    for board_num, board in enumerate(boards):
        score = try_all_smudges(board, board_num)
        if score:
            total_sum += score
    print(f'Total summary: {total_sum}')


if path.isfile('test_inputs/test13.txt'):
    with open('test_inputs/test13.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        part1(test_input_lines)

if path.isfile('test_inputs/test13.txt'):
    with open('test_inputs/test13.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        part2(test_input_lines)

print('\nFULL INPUT PART 1')
part1(full_input_lines)
print('\nFULL INPUT PART 2')
part2(full_input_lines)
