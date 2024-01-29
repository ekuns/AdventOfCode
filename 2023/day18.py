from os import path
from typing import NamedTuple
import re

with open('inputs/input18.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')

Step = NamedTuple('Step', dir=str, count=int, color=str)


class Day18:
    def __init__(self, lines):
        self.steps, self.start, self.size = self.parse_inputs(lines)
        print(f'{len(self.steps)} steps read in')
        print(f'Board is {self.size} and starting position is {self.start}')
        self.board = [['.'] * self.size[1] for x in range(self.size[0])]

    @staticmethod
    def parse_inputs(lines):
        steps = []
        for l in lines:
            m = re.match(r'([UDRL]) (\d+) \(#(......)\)', l)
            if m is None:
                break
            steps.append(Step(m.group(1), int(m.group(2)), m.group(3)))

        # Now find the range from the starting point...
        rows = [0]
        cols = [0]
        for s in steps:
            if s.dir == 'U':
                rows.append(rows[-1] - s.count)
            elif s.dir == 'D':
                rows.append(rows[-1] + s.count)
            elif s.dir == 'L':
                cols.append(cols[-1] - s.count)
            else:
                cols.append(cols[-1] + s.count)

        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        # I want the outer edge to not include the trench
        return steps, (1 - min_row, 1 - min_col), (max_row - min_row + 3, max_col - min_col + 3)

    def dump_board(self):
        for row in self.board:
            print(''.join(row))

    def follow_steps(self):
        row = self.start[0]
        col = self.start[1]
        self.board[row][col] = '#'
        for s in self.steps:
            if s.dir == 'U' or s.dir == 'D':
                for x in range(s.count):
                    row += 1 if s.dir == 'D' else -1
                    self.board[row][col] = '#'
            else:
                for x in range(s.count):
                    col += 1 if s.dir == 'R' else -1
                    self.board[row][col] = '#'

    def flood_fill(self):
        queue = [(0, 0)]
        while queue:
            row, col = queue.pop()
            if self.board[row][col] != '.':
                continue
            self.board[row][col] = 'O'
            if row > 0:
                queue.append((row - 1, col))
            if row < self.size[0] - 1:
                queue.append((row + 1, col))
            if col > 0:
                queue.append((row, col - 1))
            if col < self.size[1] - 1:
                queue.append((row, col + 1))

    def fill_lagoon(self):
        self.board = [['#' if x == '.' else x for x in b] for b in self.board]

    def unfill_border(self):
        self.board = [['.' if x == 'O' else x for x in b] for b in self.board]

    def measure_lagoon(self):
        return sum([b.count('#') for b in self.board])

    def part1(self):
        self.follow_steps()
        self.flood_fill()
        self.fill_lagoon()
        self.unfill_border()
        # self.dump_board()
        print(f'Lagoon area is {self.measure_lagoon()}')

    def turn_color_info_new_steps(self):
        def get_dir(x):
            if x == '0':
                return 'R'
            elif x == '1':
                return 'D'
            elif x == '2':
                return 'L'
            elif x == '3':
                return 'U'
            else:
                raise ValueError('Invalid input')
        self.steps = [Step(get_dir(s.color[5]), int(s.color[0:5], 16), '') for s in self.steps]

    def get_vertices(self):
        vertices = [(1, 1)]
        perimeter = 0
        for s in self.steps:
            perimeter += s.count
            if s.dir == 'U':
                new_row = vertices[-1][1] - s.count
                new_col = vertices[-1][0]
            elif s.dir == 'D':
                new_row = vertices[-1][1] + s.count
                new_col = vertices[-1][0]
            elif s.dir == 'L':
                new_row = vertices[-1][1]
                new_col = vertices[-1][0] - s.count
            else:
                new_row = vertices[-1][1]
                new_col = vertices[-1][0] + s.count
            vertices.append((new_col, new_row))
        return vertices, perimeter

    @staticmethod
    def calculate_area(vertices, perimeter):
        # Use Pick's Theorem to calculate the area: Shoelace formula + 1/2 perimeter + 1
        # We have a closed polygon so we don't need to loop back to the 1st entry
        l = len(vertices)
        return 0.5 * abs(sum(x0 * y1 - x1 * y0
                             for (x0, y0), (x1, y1) in zip(vertices[:l-1], vertices[1:l]))) + perimeter/2 + 1

    def part2(self):
        self.turn_color_info_new_steps()
        vertices, perimeter = self.get_vertices()
        print(f'{len(vertices)} vertices returned')
        area = self.calculate_area(vertices, perimeter)
        print(f'Lagoon area = {int(area)}')


if path.isfile('test_inputs/test18.txt'):
    with open('test_inputs/test18.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day18(test_input_lines).part1()

if path.isfile('test_inputs/test18.txt'):
    with open('test_inputs/test18.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day18(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day18(full_input_lines).part1()
print('\nFULL INPUT PART 2')
Day18(full_input_lines).part2()
