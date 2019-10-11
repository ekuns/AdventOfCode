import re

f = open("input25.txt", "r")
lines = f.readlines()
f.close()


def instruction(l):
    global registers

    next_step = 1

    if l.startswith('cpy '):
        m = re.match('^cpy ([^ ]+) ([^ ]+)$', l.strip())
        arg1, arg2 = m.group(1), m.group(2)
        registers[arg2] = int(arg1) if re.match('^-?[0-9]+$', arg1) else registers[arg1]
    elif l.startswith('inc '):
        reg = l[4:].strip()
        registers[reg] += 1
    elif l.startswith('dec '):
        reg = l[4:].strip()
        registers[reg] -= 1
    elif l.startswith('jnz '):
        m = re.match('^jnz ([^ ]+) ([^ ]+)$', l.strip())
        arg1, arg2 = m.group(1), m.group(2)
        arg1 = int(arg1) if re.match('^-?[0-9]+$', arg1) else registers[arg1]
        arg2 = int(arg2) if re.match('^-?[0-9]+$', arg2) else registers[arg2]
        if arg1 != 0:
            next_step = arg2
    elif l.startswith('out '):
        arg1 = l[4:].strip()
        arg1 = int(arg1) if re.match('^-?[0-9]+$', arg1) else registers[arg1]
        print(arg1)
    else:
        raise Exception('Bad instruction: ' + l)

    if l.strip() == 'cpy d a': print(registers)

    return next_step
 
def run_program():
    step = 0
    while True:
        if step < 0 or step >= len(lines):
            break
        step += instruction(lines[step])

# The program prints the binary digits of (input number + 2550) in reverse order, over and over
# 2730 == 101010101010
# So 180
registers = {'a': 180, 'b': 0, 'c': 0, 'd': 0}
run_program()
print('Part 1 - ' + str(registers))



