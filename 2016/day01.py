import re

f = open("input01.txt", "r")
lines = f.readlines()
f.close()

x, y = 0, 0

visited = set()
firstVisitedTwice = None
dir = 90
for i in re.split('[, ]+', lines[0].strip()):
    if i.startswith('R'):
        dir -= 90
    elif i.startswith('L'):
        dir += 90
    else:
        print('Bad direction: ' + x)
        break

    dist = int(i[1:])
    dir = (dir + 360) % 360

    for d in range(0, dist):
        if dir == 0:
            x += 1
        elif dir == 90:
            y += 1
        elif dir == 180:
            x -= 1
        elif dir == 270:
            y -= 1
        if not firstVisitedTwice and (x,y) in visited:
            firstVisitedTwice = (x,y)
        visited.add((x,y))

print('Part 1')
print('Final position is (' + str(x) + ',' + str(y) + ')')
print('Total distance = ' + str(abs(x)+abs(y)))

print()
print('Part 2')
print('First place visited twice is ' + str(firstVisitedTwice))
print('Total distance = ' + str(abs(firstVisitedTwice[0])+abs(firstVisitedTwice[1])))

