
f = open("input18.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

def initialize():
    lights = []
    for l in lines:
        if len(l.strip()) > 0:
            lights += [list(l.strip())]
    return lights

def dump_board(lights):
    for l in lights:
        print(''.join(l))
    print()

def count_neighbors(x,y,lights):
    s = ''
    if y > 0:
        s += lights[y-1][x-1] if x > 0 else ''
        s += lights[y-1][x]
        s += lights[y-1][x+1] if x < size-1 else ''
    s += lights[y][x-1] if x > 0 else ''
    s += lights[y][x+1] if x < size-1 else ''
    if y < size-1:
        s += lights[y+1][x-1] if x > 0 else ''
        s += lights[y+1][x]
        s += lights[y+1][x+1] if x < size-1 else ''
    #print(s + ' ' + str(s.count('#')))
    return s.count('#')

def step(lights):
    newlights = []
    for y in range(0,size):
        line = []
        for x in range(0,size):
            c = count_neighbors(x,y,lights)
            if lights[y][x] == '#':
                char = '#' if c == 2 or c == 3 else '.'
            else:
                char = '#' if c == 3 else '.'
            line += [char]
        newlights += [line]
    return newlights

#dump_board(lights)
#print(count_neighbors(1,1,lights))

# Part 1

lights = initialize()
size = len(lights)
#dump_board(lights)
for i in range(0, 100):
    lights = step(lights)

#dump_board(lights)

print('The number of lights that is on is ' + str(sum([''.join(l).count('#') for l in lights])))

#Part 2

lights = initialize()
size = len(lights)
lights[0][0] = '#'
lights[0][-1] = '#'
lights[-1][0] = '#'
lights[-1][-1] = '#'
for i in range(0, 100):
    lights = step(lights)
    lights[0][0] = '#'
    lights[0][-1] = '#'
    lights[-1][0] = '#'
    lights[-1][-1] = '#'

print('The number of lights that is on is ' + str(sum([''.join(l).count('#') for l in lights])))

