from os import path
from collections import namedtuple

with open('inputs/input15.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')

Lens = namedtuple("Lens", "label focus")


class Day15:
    def __init__(self, lines):
        self.steps = self.read_steps(lines)
        self.boxes = [[] for _ in range(256)]

    @staticmethod
    def read_steps(lines):
        return lines[0].split(',')

    @staticmethod
    def hash(string):
        h = 0
        for c in string:
            h = ((h + ord(c)) * 17) % 256
        return h

    def dump_boxes(self):
        for cnt, box in enumerate(self.boxes):
            if box:
                print(f'{cnt} {"".join([f"[{b.label} {b.focus}]" for b in box])}')

    def part1(self):
        total = 0
        for step in self.steps:
            # print(f'{step}: {self.hash(step)}')
            total += self.hash(step)
        print(f'Total of all hashes = {total}')

    def find_label_index(self, label, h):
        for cnt, lens in enumerate(self.boxes[h]):
            if lens.label == label:
                return cnt
        return -1

    def part2(self):
        for step in self.steps:
            if step.endswith('-'):
                label = step[0:-1]
                h = self.hash(label)
                # print(f'REMOVE: hash({label}) = {h}')
                index = self.find_label_index(label, h)
                if index >= 0:
                    del self.boxes[h][index]
            else:
                values = step.split('=')
                label = values[0]
                focus = int(values[1])
                h = self.hash(label)
                # print(f'ADD: hash({label}) = {h} focus {focus}')
                index = self.find_label_index(label, h)
                if index >= 0:
                    self.boxes[h][index] = Lens(label, focus)
                else:
                    self.boxes[h].append(Lens(label, focus))
            # self.dump_boxes()

        total = 0
        for cnt, box in enumerate(self.boxes):
            if box:
                total += sum([(cnt + 1) * (slot + 1) * lens.focus for slot, lens in enumerate(box)])
        # self.dump_boxes()
        print(f'Total focusing power = {total}')


if path.isfile('test_inputs/test15.txt'):
    with open('test_inputs/test15.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day15(test_input_lines).part1()

if path.isfile('test_inputs/test15.txt'):
    with open('test_inputs/test15.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day15(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day15(full_input_lines).part1()
print('\nFULL INPUT PART 2')
Day15(full_input_lines).part2()
