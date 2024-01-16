from collections import namedtuple
from itertools import groupby
from os import path

with open('inputs/input12.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')

Permutation = namedtuple("Permutation", "group count paths remaining")


class Day12:
    def __init__(self, lines):
        self.boards = self.read_board(lines)

    @staticmethod
    def read_board(lines):
        board = []
        for l in lines:
            split1 = l.split(' ')
            springs = list(split1[0])
            counts = [int(x) for x in split1[1].split(',')]
            board.append((springs, counts))
        return board

    def dump_board(self):
        print('\nBoard:')
        for springs, counts in self.boards:
            print(f'{springs} - {counts}')

    def expand_board(self):
        self.boards = [('?'.join([''.join(springs)] * 5), counts * 5) for springs, counts in self.boards]

    @staticmethod
    def replace_unknowns(springs, replacements):
        positions = [x for x in range(len(springs)) if springs[x] == '?']
        new_springs = springs.copy()
        for cnt, p in enumerate(positions):
            new_springs[p] = replacements[cnt]
        return new_springs

    @staticmethod
    def check_numbers(board, counts):
        lens = []
        for k, g in groupby(board):
            if k != '#':
                continue
            count = sum([1 for _ in g])
            lens.append(count)
        return lens == counts

    def unique_permutations(self, elements):
        if len(elements) == 1:
            yield (elements[0],)
        else:
            unique_elements = set(elements)
            for first_element in unique_elements:
                remaining_elements = list(elements)
                remaining_elements.remove(first_element)
                for sub_permutation in self.unique_permutations(remaining_elements):
                    yield (first_element,) + sub_permutation

    def part1(self):
        total_matches = 0
        for springs, counts in self.boards:
            total_damaged_springs = sum(counts)
            known_damaged_springs = sum([1 if x == '#' else 0 for x in springs])
            needed_damaged_springs = total_damaged_springs - known_damaged_springs
            unknown_springs = sum([1 if x == '?' else 0 for x in springs])

            extra_items = '#' * needed_damaged_springs + '.' * (unknown_springs - needed_damaged_springs)
            successful_counts = 0
            for choice in self.unique_permutations(extra_items):
                new_board = self.replace_unknowns(springs, choice)
                if self.check_numbers(new_board, counts):
                    successful_counts += 1
            # print(f'# successful matches for {springs} = {successful_counts}')
            total_matches += successful_counts
        print(f'Total of all successful matches = {total_matches}')

    @staticmethod
    def add_to_queue(queue, permutation):
        for q in queue:
            if q.group == permutation.group and q.count == permutation.count and q.remaining == permutation.remaining:
                queue.remove(q)
                queue.append(Permutation(q.group, q.count, q.paths + permutation.paths, q.remaining))
                return
        else:
            queue.append(permutation)

    def count_permutations(self, springs, counts):
        queue = [Permutation(0, 0, 1, springs)]
        next_queue = []
        while queue:
            item = queue.pop()
            next_remaining = item.remaining[1:]
            current_count = counts[item.group] if item.group < len(counts) else -1
            next_char = item.remaining[0]

            if next_char == '.' or next_char == '?':
                if item.count == 0:  # If we are not currently in a group, just move forward in the string
                    self.add_to_queue(next_queue, Permutation(item.group, 0, item.paths, next_remaining))
                elif item.count == current_count:  # We have finished a group so move onto the next
                    self.add_to_queue(next_queue, Permutation(item.group + 1, 0, item.paths, next_remaining))

            if next_char == '#' or next_char == '?':
                if item.count + 1 <= current_count:
                    self.add_to_queue(next_queue, Permutation(item.group, item.count + 1, item.paths, next_remaining))

            if not queue:
                if len(next_remaining) == 0:
                    break
                queue = next_queue
                next_queue = []

        solutions = []
        last_group_count = counts[-1]
        for q in next_queue:
            if q.group + 1 == len(counts) and q.count == last_group_count:
                self.add_to_queue(solutions, Permutation(q.group + 1, 0, q.paths, ''))
            elif q.group == len(counts) and q.count == 0:
                self.add_to_queue(solutions, q)

        return solutions

    def part2(self):
        self.expand_board()
        solution_count = 0
        for springs, counts in self.boards:
            solutions = self.count_permutations(springs, counts)
            if len(solutions) == 1:
                solution_count += solutions[0].paths
        print(f'Grand total of all solutions = {solution_count}')


if path.isfile('test_inputs/test12.txt'):
    with open('test_inputs/test12.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day12(test_input_lines).part1()

if path.isfile('test_inputs/test12.txt'):
    with open('test_inputs/test12.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day12(test_input_lines).part2()

print('\nFULL INPUT - Part 1')
Day12(full_input_lines).part1()
print('\nFULL INPUT - Part 2')
Day12(full_input_lines).part2()
