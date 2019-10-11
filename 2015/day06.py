import re

f = open("input06.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

### Part 1

lights = []
for i in range(0,1000):
    lights.append([False] * 1000)

def parse(line):
    m = re.match('^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)\s*$', line)
    if m == None:
        return

    x1, y1 = (int(m.group(2)), int(m.group(3)))
    x2, y2 = (int(m.group(4)), int(m.group(5)))

    if m.group(1) == 'turn on':
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                lights[y][x] = True
    elif m.group(1) == 'turn off':
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                lights[y][x] = False
    else:
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                lights[y][x] = not lights[y][x]

def count():
    return sum([sum(l) for l in lights])

#parse('turn on 0,0 through 999,999')
#print(count())
#parse('toggle 0,0 through 999,0')
#print(count())
#parse('turn off 499,499 through 500,500')
#print(count())

for l in lines:
    parse(l)

print('Lights left lit after it\'s all done: ' + str(count()))

### Part 2

lights = []
for i in range(0,1000):
    lights.append([0] * 1000)

def parse2(line):
    m = re.match('^(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)\s*$', line)
    if m == None:
        return

    x1, y1 = (int(m.group(2)), int(m.group(3)))
    x2, y2 = (int(m.group(4)), int(m.group(5)))

    if m.group(1) == 'turn on':
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                lights[y][x] += 1
    elif m.group(1) == 'turn off':
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                if lights[y][x] > 0:
                    lights[y][x] -= 1
    else:
        for y in range(y1, y2+1):
            for x in range(x1, x2+1):
                lights[y][x] += 2

for l in lines:
    parse2(l)

print('Lights level after it\'s all done: ' + str(count()))

