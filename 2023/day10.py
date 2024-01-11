from os import path

with open('inputs/input10.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


# ================ Part 1 ================


def read_board(lines):
    board = [list(l) for l in lines]
    beast_pos = [(c, l.index('S')) for c, l in enumerate(lines) if 'S' in l][0]
    return beast_pos, board


# Map from last move and current board piece to next move
move_map = {
    'L': {'L': 'U', 'F': 'D', '-': 'L'},
    'R': {'J': 'U', '7': 'D', '-': 'R'},
    'U': {'7': 'L', 'F': 'R', '|': 'U'},
    'D': {'J': 'L', 'L': 'R', '|': 'D'}
}


def get_first_moves(beast_pos, board):
    beast_row = beast_pos[0]
    beast_col = beast_pos[1]
    to_left = board[beast_row][beast_col-1] if beast_col > 0 else '.'
    to_right = board[beast_row][beast_col+1] if beast_col < len(board[0]) else '.'
    up = board[beast_row-1][beast_col] if beast_row > 0 else '.'
    down = board[beast_row+1][beast_col] if beast_row < len(board) else '.'

    next_moves = []

    if to_left == 'L' or to_left == 'F' or to_left == '-':
        next_moves.append((beast_row, beast_col-1, move_map['L'][to_left], 1, to_left))
    if to_right == 'J' or to_right == '7' or to_right == '-':
        next_moves.append((beast_row, beast_col+1, move_map['R'][to_right], 1, to_right))
    if up == '7' or up == 'F' or up == '|':
        next_moves.append((beast_row-1, beast_col, move_map['U'][up], 1, up))
    if down == 'J' or down == 'L' or down == '|':
        next_moves.append((beast_row+1, beast_col, move_map['D'][down], 1, down))

    return next_moves


def get_next_move(move, board):
    move_row = move[0]
    move_col = move[1]
    direction = move[2]
    move_number = move[3] + 1
    next_move = move_map[direction]

    if direction == 'L':
        next_col = move_col - 1
        to_left = board[move_row][next_col] if next_col >= 0 else '.'
        return move_row, next_col, next_move[to_left], move_number, to_left
    if direction == 'R':
        next_col = move_col + 1
        to_right = board[move_row][next_col] if next_col < len(board[0]) else '.'
        return move_row, next_col, next_move[to_right], move_number, to_right
    if direction == 'U':
        next_row = move_row - 1
        up = board[next_row][move_col] if next_row >= 0 else '.'
        return next_row, move_col, next_move[up], move_number, up
    if direction == 'D':
        next_row = move_row + 1
        down = board[next_row][move_col] if next_row < len(board) else '.'
        return next_row, move_col, next_move[down], move_number, down
    return None, None, None, None, None


def part1(lines):
    beast_pos, board = read_board(lines)
    next_moves = get_first_moves(beast_pos, board)
    move_history = [next_moves]
    while True:
        next_moves = [get_next_move(move, board) for move in next_moves]
        move_history.append(next_moves)
        if next_moves[0][0] == next_moves[1][0] and next_moves[0][1] == next_moves[1][1]:
            print(f'Simultaneous arrival after {next_moves[0][3]} moves')
            break

# ================ Part 2 ================


def part2(lines):
    pass


if path.isfile('test_inputs/test10_A1.txt'):
    with open('test_inputs/test10_A1.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1A')
        part1(test_input_lines)

if path.isfile('test_inputs/test10_A2.txt'):
    with open('test_inputs/test10_A2.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1B')
        part1(test_input_lines)

# if path.isfile('test_inputs/test09.txt'):
#     with open('test_inputs/test09.txt', 'r') as f:
#         test_input_lines = f.readlines()
#         test_input_lines = [l.strip() for l in test_input_lines]
#         print('\nTEST INPUT PART 2')
#         part2(test_input_lines)

print('\nFULL INPUT')
part1(full_input_lines)
# part2(full_input_lines)
