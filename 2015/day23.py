import re

f = open("input23.txt", "r")
lines = f.readlines()
f.close()

def step(line):
    step = 1
    x = re.split('[, ]+', line.strip())
    inst = x[0]
    oper = x[1:]
    if inst == 'hlf':
        registers[oper[0]] //= 2
    elif inst == 'tpl':
        registers[oper[0]] *= 3
    elif inst == 'inc':
        registers[oper[0]] += 1
    elif inst == 'jmp':
        step = int(oper[0])
    elif inst == 'jie':
        if registers[oper[0]] % 2 == 0:
            step = int(oper[1])
    elif inst == 'jio':
        if registers[oper[0]] == 1:
            step = int(oper[1])

    #print('After instruction ' + inst + ' operands ' + str(oper) + ' registers are ' + str(registers) +
    #      ' and step is ' + str(step))
    return step

def run_program():
    offset = 0
    steps = 0
    while True:
        offset += step(lines[offset])
        if offset >= len(lines) or offset < 0:
            break
        steps += 1

    print('Registers when program terminates after ' + str(steps) + ' steps:')
    print(registers)

# Part 1

registers = {'a': 0, 'b': 0}
run_program()

# Part 2
registers = {'a': 1, 'b': 0}
run_program()

