import re

f = open("input12.txt", "r")
lines = f.readlines()
f.close()


def instruction(l):
    global registers

    next_step = 1

    if l.startswith('cpy '):
        m = re.match('^cpy ([^ ]+) ([^ ]+)$', l.strip())
        arg1, arg2 = m.group(1), m.group(2)
        if arg1.isdigit():
            registers[arg2] = int(arg1)
        else:
            registers[arg2] = registers[arg1]
    elif l.startswith('inc '):
        reg = l[4:].strip()
        registers[reg] += 1
    elif l.startswith('dec '):
        reg = l[4:].strip()
        registers[reg] -= 1
    elif l.startswith('jnz '):
        m = re.match('^jnz ([^ ]+) ([^ ]+)$', l.strip())
        arg1, arg2 = m.group(1), int(m.group(2))
        if arg1.isdigit():
            if int(arg1) != 0:
                next_step = arg2
        else:
            if registers[arg1] != 0:
                next_step = arg2
    else:
        raise Exception('Bad instruction: ' + l)

    return next_step
 
def run_program():
    step = 0
    while True:
        if step < 0 or step >= len(lines):
            break
        step += instruction(lines[step])

registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
run_program()
print('Part 1 - ' + str(registers))

registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
run_program()
print('Part 2 - ' + str(registers))

