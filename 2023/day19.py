from os import path

with open('inputs/input19.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')


class Day19:
    def __init__(self, lines):
        self.rules, self.ratings = self.parse_inputs(lines)

    @staticmethod
    def parse_inputs(lines):
        rules = {}
        rating_offset = 0
        for count, l in enumerate(lines):
            if len(l) == 0:
                rating_offset = count
                break
            x = l.split('{')
            rules[x[0]] = x[1][0:-1].split(',')

        ratings = [{x[0]: int(x[2:]) for x in r}
                   for r in [r[1:-1].split(',') for r in lines[rating_offset + 1:]]]

        return rules, ratings

    def apply_rules(self, item):
        current_rule = 'in'
        while True:
            for x in self.rules[current_rule]:
                if ':' not in x:
                    if x == 'A':
                        return True
                    if x == 'R':
                        return False
                    current_rule = x
                    break

                var = item[x[0]]
                test = x[1]
                z = x[2:].split(':')
                comparison = int(z[0])
                destination = z[1]
                if (test == '<' and var < comparison) or (test == '>' and var > comparison):
                    if destination == 'A':
                        return True
                    if destination == 'R':
                        return False
                    current_rule = destination
                    break

    def rate_items(self):
        total_ratings = 0
        for item in self.ratings:
            if self.apply_rules(item):
                total_ratings += sum([x for x in item.values()])
        return total_ratings

    def part1(self):
        total_ratings = self.rate_items()
        print(f'Total rating of accepted items: {total_ratings}')

    def part2(self):
        pass


if path.isfile('test_inputs/test19.txt'):
    with open('test_inputs/test19.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day19(test_input_lines).part1()

# if path.isfile('test_inputs/test19.txt'):
#     with open('test_inputs/test19.txt', 'r') as f:
#         test_input_lines = f.readlines()
#         test_input_lines = [l.strip() for l in test_input_lines]
#         print('\nTEST INPUT PART 2')
#         Day19(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day19(full_input_lines).part1()
# print('\nFULL INPUT PART 2')
# Day19(full_input_lines).part2()
