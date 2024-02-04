from os import path
from typing import NamedTuple
import re
from math import lcm

with open('inputs/input20.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')

Module = NamedTuple('Module', type=str, dests=list)


class Day20:
    def __init__(self, lines):
        self.modules = self.parse_inputs(lines)
        self.pulses = []
        self.low = 0
        self.high = 0
        self.flip_flop = {}
        self.conjunction = {}
        self.cycle = 0
        self.part = 0
        self.modules_to_watch = {}
        for k, v in self.modules.items():
            # print(f'{k} = {v}')
            if v.type == '&':  # conjunction
                inputs = [kk for kk, vv in self.modules.items() if k in vv.dests]
                self.conjunction[k] = {i: False for i in inputs}
            elif v.type == '%':  # flip-flop
                self.flip_flop[k] = False

    @staticmethod
    def parse_inputs(lines):
        modules = {}
        for l in lines:
            m = re.match(r'([&%])?([^ ]+) -> (.*)', l)
            if m is None:
                return
            modules[m.group(2)] = Module(m.group(1), [x.strip() for x in m.group(3).split(',')])
        return modules

    def button_push(self):
        # print('button -low-> broadcaster')
        self.low += 1  # Don't forget to count the low for the button push

        # Issue "low" to broadcast
        for dest in self.modules['broadcaster'].dests:
            self.pulses.append(('broadcaster', dest, False))
            # print(f'broadcaster -low-> {dest}')
            self.low += 1

    def process_pulses(self):
        while self.pulses:
            origin, dest_name, is_high = self.pulses.pop(0)
            if dest_name not in self.modules:
                # print(f'Skipping {dest_name}')
                continue
            module = self.modules[dest_name]
            if module.type == '%':
                if not is_high:  # flip-flops ignore high pulses
                    # but if we get a low pulse, change state and send our new state as a pulse
                    self.flip_flop[dest_name] = not self.flip_flop[dest_name]
                    new_pulse = self.flip_flop[dest_name]
                    for d in module.dests:
                        self.pulses.append((dest_name, d, new_pulse))
                        # print(f'{dest_name} -{"high" if new_pulse else "low"}-> {d}')
                        if self.flip_flop[dest_name]:
                            self.high += 1
                        else:
                            self.low += 1
            elif module.type == '&':
                self.conjunction[dest_name][origin] = is_high
                all_high = all([pulse for name, pulse in self.conjunction[dest_name].items()])
                new_pulse = not all_high
                for d in module.dests:
                    self.pulses.append((dest_name, d, new_pulse))
                    # print(f'{dest_name} -{"high" if new_pulse else "low"}-> {d}')
                    if new_pulse:
                        self.high += 1
                    else:
                        self.low += 1

                    # Look for information for part 2
                    if d == 'rx' and self.part == 2:
                        for key, val in self.conjunction['sq'].items():
                            if val and self.modules_to_watch[key] == 0:
                                self.modules_to_watch[key] = self.cycle + 1
                        if sum([1 for x in self.modules_to_watch.values() if x > 0]) == 4:
                            print(self.modules_to_watch)
                            print(lcm(*list(self.modules_to_watch.values())))
                            exit(0)

    def part1(self):
        self.part = 1
        for _ in range(1000):
            # print('')
            self.button_push()
            self.process_pulses()
        print(f'Pulses: high = {self.high}, low = {self.low}, combination = {self.high * self.low}')

    def instrument_things(self):
        targets = [key for key, module in self.modules.items() if 'rx' in module.dests]
        # Assume targets is only length 1 because it is in our inputs
        self.modules_to_watch = {key: 0 for key, module in self.modules.items() if targets[0] in module.dests}
        print(f'targets to watch = {self.modules_to_watch}')

    def part2(self):
        self.part = 2
        # Add our destination module
        self.modules['rx'] = Module('&', [])
        inputs = [kk for kk, vv in self.modules.items() if 'rx' in vv.dests]
        self.conjunction['rx'] = {i: False for i in inputs}
        self.instrument_things()
        for cycle in range(1000000):
            self.cycle = cycle
            self.button_push()
            self.process_pulses()


if path.isfile('test_inputs/test20.txt'):
    with open('test_inputs/test20.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day20(test_input_lines).part1()

# if path.isfile('test_inputs/test20.txt'):
#     with open('test_inputs/test20.txt', 'r') as f:
#         test_input_lines = f.readlines()
#         test_input_lines = [l.strip() for l in test_input_lines]
#         print('\nTEST INPUT PART 2')
#         Day19(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day20(full_input_lines).part1()
print('\nFULL INPUT PART 2')
Day20(full_input_lines).part2()
