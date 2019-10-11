from collections import deque
import re

f = open("input21.txt", "r")
lines = f.readlines()
f.close()


def step(line, string, reverse=False):
    if line.startswith('swap position '):
        m = re.match('^swap position (\d+) with position (\d+)$', line)
        pos1, pos2 = int(m.group(1)), int(m.group(2))
        s = list(string)
        s[pos1], s[pos2] = s[pos2], s[pos1]
        string = ''.join(s)
    elif line.startswith('swap letter '):
        m = re.match('^swap letter (.) with letter (.)$', line)
        let1, let2 = m.group(1), m.group(2)
        string = string.replace(let1, ':').replace(let2, let1).replace(':', let2)
    elif line.startswith('rotate based on position of letter '):
        letter = line[-1]
        count = string.index(letter)
        if not reverse:
            if count >= 4:
                count += 1
            count += 1
        else:
            count = [-1, -1, 2, -2, 1, -3, 0, 4][count]
        s = deque(string)
        s.rotate(count)
        string = ''.join(s)
    elif line.startswith('rotate '):
        m = re.match('^rotate (left|right) (\d+) steps?$', line)
        direction, count = m.group(1), int(m.group(2))
        if direction == 'left':
            count *= -1
        if reverse:
            count *= -1
        s = deque(string)
        s.rotate(count)
        string = ''.join(s)
    elif line.startswith('reverse positions '):
        m = re.match('^reverse positions (\d+) through (\d+)$', line)
        pos1, pos2 = int(m.group(1)), int(m.group(2))
        s = string[0:pos1] if pos1 > 0 else ''
        s += string[pos1:pos2+1][::-1]
        s += string[pos2+1:] if pos2+1 < len(string) else ''
        string = s
    elif line.startswith('move position '):
        m = re.match('^move position (\d+) to position (\d+)$', line)
        pos1, pos2 = int(m.group(1)), int(m.group(2))
        if reverse:
            pos1, pos2 = pos2, pos1
        letter = string[pos1]
        string = string[0:pos1] + string[pos1+1:]
        string = string[0:pos2] + letter + string[pos2:]
    else:
        print('Bad command: ' + line)
    #print('After ' + line + ' string is ' + string)
    return string

string = 'abcdefgh'
for l in lines:
    string = step(l.strip(), string)

# Part 1

print('Part 1 - String is ' + string)

# Part 2

string = 'fbgdceah'
for l in lines[::-1]:
    string = step(l.strip(), string, True)

print('Part 2 - String is ' + string)

