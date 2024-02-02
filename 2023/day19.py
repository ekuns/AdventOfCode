from os import path
from typing import NamedTuple

with open('inputs/input19.txt', 'r') as f:
    full_input_lines = f.readlines()
full_input_lines = [l.strip() for l in full_input_lines]
print(f'Number of lines: {len(full_input_lines)}')

Range = NamedTuple('Range', min=int, max=int)

Rule = NamedTuple('Rule', name=str, values=dict)


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

    def follow_one_rule(self, rule, accepted, queue):
        values = rule.values
        for x in self.rules[rule.name]:
            if ':' not in x:
                if x == 'A':
                    accepted.append(rule)
                elif x != 'R':
                    queue.append(Rule(x, values))
                return

            varname = x[0]
            test = x[1]
            z = x[2:].split(':')
            comparison_value = int(z[0])
            next_rule = z[1]
            if test == '<':
                if comparison_value > values[varname].max:
                    # All values are already below the limit, so all values go to the next step
                    if next_rule == 'A':
                        accepted.append(rule)
                    elif next_rule != 'R':
                        queue.append(Rule(next_rule, values))
                    return
                elif comparison_value < values[varname].min:
                    # No values are below the limit, so go to the next rule in the list
                    continue
                else:  # Some values are below the limit and some are above
                    new_values = values.copy()
                    new_values[varname] = Range(values[varname].min, comparison_value - 1)
                    if next_rule == 'A':
                        accepted.append(Rule(next_rule, new_values))
                    elif next_rule != 'R':
                        queue.append(Rule(next_rule, new_values))

                    # Continue processing this step with a modified minimum
                    values[varname] = Range(comparison_value, values[varname].max)
            else:
                if comparison_value < values[varname].min:
                    # All values are already above the limit, so all values go to the next step
                    if next_rule == 'A':
                        accepted.append(rule)
                    elif next_rule != 'R':
                        queue.append(Rule(next_rule, values))
                    return
                elif comparison_value > values[varname].max:
                    # No values are above the limit, so go to the next rule in the list
                    continue
                else:  # Some values are below the limit and some are above
                    new_values = values.copy()
                    new_values[varname] = Range(comparison_value + 1, values[varname].max)
                    if next_rule == 'A':
                        accepted.append(Rule(next_rule, new_values))
                    elif next_rule != 'R':
                        queue.append(Rule(next_rule, new_values))

                    # Continue processing this step with a modified minimum
                    values[varname] = Range(values[varname].min, comparison_value)

    def make_decision_tree(self):
        queue = [Rule('in', {'x': Range(1, 4000), 'm': Range(1, 4000),
                             'a': Range(1, 4000), 's': Range(1, 4000)})]
        accepted = []
        while queue:
            rule = queue.pop()
            self.follow_one_rule(rule, accepted, queue)
        return accepted

    def part2(self):
        accepted = self.make_decision_tree()
        total_solutions = 0
        for a in accepted:
            x_range = a.values['x']
            m_range = a.values['m']
            a_range = a.values['a']
            s_range = a.values['s']
            total_solutions += ((x_range.max - x_range.min + 1) * (m_range.max - m_range.min + 1) *
                                (a_range.max - a_range.min + 1) * (s_range.max - s_range.min + 1))
        print(f'Total solutions = {total_solutions}')


if path.isfile('test_inputs/test19.txt'):
    with open('test_inputs/test19.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 1')
        Day19(test_input_lines).part1()

if path.isfile('test_inputs/test19.txt'):
    with open('test_inputs/test19.txt', 'r') as f:
        test_input_lines = f.readlines()
        test_input_lines = [l.strip() for l in test_input_lines]
        print('\nTEST INPUT PART 2')
        Day19(test_input_lines).part2()

print('\nFULL INPUT PART 1')
Day19(full_input_lines).part1()
print('\nFULL INPUT PART 2')
Day19(full_input_lines).part2()
