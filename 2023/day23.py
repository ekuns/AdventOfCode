from collections import defaultdict
from os import path

with open('inputs/input23.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day23:
    def __init__(self, lines):
        self.board: list[list[str]] = self.parse_inputs(lines)
        self.nrow = len(self.board)
        self.ncol = len(self.board[0])
        self.part = 0
        self.start_pos = (0, 1)
        self.end_row = len(self.board) - 1
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.path_list = defaultdict(set)
        self.max_solution_len = 0

    @staticmethod
    def parse_inputs(lines) -> list[list[str]]:
        board = [list(l) for l in lines]
        return board

    def dump_board(self, pth):
        brd = self.board.copy()
        brd[self.start_pos[0]][self.start_pos[1]] = 'S'
        for p in pth:
            brd[p[0]][p[1]] = 'O'
        for b in brd:
            print(''.join(b))

    def get_options(self, r, c, pth):
        opts = []
        if r == self.end_row:
            return opts
        for d in self.directions:
            nxt_row, nxt_col = r + d[0], c + d[1]
            if self.board[nxt_row][nxt_col] != '#' and (nxt_row, nxt_col) not in pth:
                opts.append((nxt_row, nxt_col))
        return opts

    def get_next_steps(self, pos, pth):
        cur_row = pos[0]
        cur_col = pos[1]
        cell = self.board[cur_row][cur_col]
        if self.part == 1 and cell in ['>', '<', '^', 'v']:
            if cell == '>':
                n = (cur_row, cur_col + 1)
            elif cell == '<':
                n = (cur_row, cur_col - 1)
            elif cell == '^':
                n = (cur_row - 1, cur_col)
            else:
                n = (cur_row + 1, cur_col)
            return [] if n in pth else [n]

        return self.get_options(cur_row, cur_col, pth)

    def follow_path(self, pos, path, successful_paths):
        for partial_path in self.path_list[pos]:
            if self.part == 1:  # For part 1, restrict direction through < > ^ v
                restriction = partial_path[1]
                second_step = partial_path[2]
                direction = self.board[restriction[0]][restriction[1]]
                if direction == '>' and restriction[1] + 1 != second_step[1]:
                    continue
                if direction == '<' and restriction[1] - 1 != second_step[1]:
                    continue
                if direction == 'v' and restriction[0] + 1 != second_step[0]:
                    continue
                if direction == '^' and restriction[0] - 1 != second_step[0]:
                    continue

            end = partial_path[-1]
            if end in path:
                continue
            new_path = path.copy()
            new_path += list(partial_path[1:])
            if end[0] == self.end_row:
                successful_paths.append(new_path)
                continue
            # Recurse for each option
            self.follow_path(end, new_path, successful_paths)

    def solve_maze(self):
        pos = self.start_pos
        successful_paths = []
        self.follow_path(pos, [], successful_paths)
        return successful_paths

    def dump_solution(self, successful_paths):
        if len(successful_paths) == 0:
            print('No solutions found')
            return
        final_steps = max([len(p) for p in successful_paths])
        for p in successful_paths:
            if len(p) == final_steps:
                self.dump_board(p)
        print(f'Found {len(successful_paths)} successful paths')
        print(f'Longest path is {final_steps} steps')

    def find_paths(self, origin, pos):
        path = [origin, pos]
        while True:
            next_steps = self.get_next_steps(pos, path)
            if len(next_steps) == 0:
                return
            if len(next_steps) == 1:
                next_step = next_steps[0]
                if next_step[0] == self.end_row:
                    path.append(next_step)
                    self.path_list[origin].add(tuple(path))
                    return
                pos = next_step
                path.append(next_step)
            else:
                # Our path has ended, save it and start the new ones
                self.path_list[origin].add(tuple(path))
                self.path_list[pos].add(tuple(path[::-1]))
                for next_step in next_steps:
                    if next_step != origin:
                        self.find_paths(pos, next_step)
                return

    def part1(self):
        self.part = 1
        self.find_paths(self.start_pos, (1, 1))
        successful_paths = self.solve_maze()
        self.dump_solution(successful_paths)

    def follow_path_2(self, pos, path, len_so_far):
        path.append(pos)
        for partial_path in self.path_list[pos]:
            end = partial_path[-1]
            if end in path:
                continue

            next_len_so_far = len_so_far + len(partial_path) - 1
            new_path = path.copy()
            if end[0] == self.end_row:
                new_path.append(end)
                if self.max_solution_len < next_len_so_far:
                    self.max_solution_len = next_len_so_far
                continue
            # Recurse for each option
            self.follow_path_2(end, new_path, next_len_so_far)

    def part2(self):
        self.part = 1
        self.find_paths(self.start_pos, (1, 1))
        self.part = 2
        self.follow_path_2(self.start_pos, [], 0)
        print(f'Maximum solution found is {self.max_solution_len} steps')


if path.isfile('test_inputs/test23.txt'):
    with open('test_inputs/test23.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day23(test_input_lines).part1()

print('\nFULL INPUT PART 1')
Day23(full_input_lines).part1()

if path.isfile('test_inputs/test23.txt'):
    with open('test_inputs/test23.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day23(test_input_lines).part2()

print('\nFULL INPUT PART 2')
Day23(full_input_lines).part2()
