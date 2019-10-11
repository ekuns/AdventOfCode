import re

f = open("input23.txt", "r")
lines = f.readlines()
f.close()


def instruction(lines, step):
    global registers

    l = lines[step]
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
    elif l.startswith('tgl '):
        reg = l[4:].strip()
        modified = registers[reg] + step
        if modified < 0 or modified >= len(lines):
            return next_step
        if lines[modified].startswith('inc '):
            lines[modified] = 'dec ' + lines[modified][4:]
        elif lines[modified].startswith('dec '):
            lines[modified] = 'inc ' + lines[modified][4:]
        elif lines[modified].startswith('jnz '):
            lines[modified] = 'cpy ' + lines[modified][4:]
        elif lines[modified].startswith('cpy '):
            lines[modified] = 'jnz ' + lines[modified][4:]
        elif lines[modified].startswith('tgl '):
            lines[modified] = 'inc ' + lines[modified][4:]
        else:
            print('Tried to toggle unxpected instruction: ' + lines[modified])
            raise Exception('Tried to toggle unxpected insruction : ' + l)
    else:
        raise Exception('Bad instruction: ' + l)

    return next_step
 
def run_program(lines):
    lines = list(lines)
    step = 0
    while True:
        if step < 0 or step >= len(lines):
            break
        #print('Before: ' + lines[step].strip() + '    ' + str(registers))
        step += instruction(lines, step)
        #print('Next step is now ' + str(step))

# Part 1

registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
run_program(lines)
print('Part 1 - ' + str(registers))

# Part 2

# The input program reduces to this:
# (As long as b >= 6 else it will never finish)
# It has to toggle b-4, b-3, b=2, b=1 and b starts out as input - 2 at that point
def factorial(inp):
    a = inp
    b = inp - 1
    while b > 0:
        d = a
        a = b * d
        b -= 1

    a += 6600
    return a

print('Part 2 - ' + str(factorial(12)))

registers = {'a': 6, 'b': 0, 'c': 0, 'd': 0}
run_program(lines)
print(str(registers))

