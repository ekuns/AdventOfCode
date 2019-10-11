#!/usr/bin/python3

import re

f = open("input17.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

clay = []
for l in lines:
    m = re.search('(x|y)=(\d+), (x|y)=(\d+)\.\.(\d+)', l)
    if m is None:
        print("No match found for line: %s" % ( l ))
        continue
    clay += [(m.group(1), m.group(3), int(m.group(2)), int(m.group(4)), int(m.group(5)))]

minx=9999
maxx=0
miny=9999
maxy=0
for c in clay:
    if c[0] == "x":
        # vertical strip of clay
        x, y1, y2 = c[2], c[3], c[4]
        if y1 < miny:  miny = y1
        if y2 > maxy:  maxy = y2
        if x < minx:  minx = x
        elif x > maxx:  maxx = x
    else:
        # horizontal strip of clay
        y, x1, x2 = c[2], c[3], c[4]
        if y < miny:  miny = y
        elif y > maxy:  maxy = y
        if x1 < minx:  minx = x1
        if x2 > maxx:  maxx = x2

print("x ranges from %d to %d" % (minx, maxx))
print("y ranges from %d to %d" % (miny, maxy))

grid = [['.' for _ in range(minx-1, maxx+2)] for _ in range(0, maxy+1)]
grid[0][500-minx+1] = '+'

for c in clay:
    if c[0] == "x":
        # vertical strip of clay
        x, y1, y2 = c[2], c[3], c[4]
        for y in range(y1,y2+1):
            grid[y][x-minx+1] = '#'
    else:
        # horizontal strip of clay
        y, x1, x2 = c[2], c[3], c[4]
        grid[y][x1-minx+1:x2-minx+1] = ['#'] * (x2 - x1)

def dumpMap():
    for g in grid:
        print(''.join(g))
    print()

def countWater():
    count = 0
    for g in grid[miny:]:
        count += sum([1 for gg in g if gg == '~' or gg == '|'])
    return count

def countStandingWater():
    count = 0
    for g in grid[miny:]:
        count += sum([1 for gg in g if gg == '~'])
    return count

springs = [(500,0)]

def dumpSprings():
    for s in springs:
        print(s)

#dumpMap()

count = 0
while True:
    if len(springs) == 0:
        print("There are no more springs")
        break

    ss = []
    for s in springs:
        xp, yp = s[0]-minx+1, s[1]

        nxt = (s[0], s[1]+1)
        x, y = nxt[0]-minx+1, nxt[1]

        if y == len(grid):
            print("Y is off the grid at %d" % ( y ))
            continue

        if grid[y][x] == '.':
            # One row down is empty, so keep flowing down
            ss += [nxt]
            grid[y][x] = '|'
            if y >= miny: count += 1
        elif grid[y][x] == '#' or grid[y][x] == '~':
            # One row down is clay or filled with water, so look sideways
            right = True
            for i in range(xp+1,maxx-minx+2):
                #print("r: Looking at %s above %s" % ( grid[yp][i], grid[yp+1][i] ))
                if grid[yp][i] == '#': break
                if grid[yp+1][i] != '#' and grid[yp+1][i] != '~':
                    #print("right is false")
                    right = False
                    break
            left = True
            for i in range(xp-1,-1,-1):
                #print("l: Looking at %s above %s" % ( grid[yp][i], grid[yp+1][i] ))
                if grid[yp][i] == '#': break
                if grid[yp+1][i] != '#' and grid[yp+1][i] != '~':
                    #print("left is false")
                    left = False
                    break

            if right and left:
                #print("right and left")
                # Fill up one level and move the spring up one level
                ss += [(s[0], s[1]-1)]
                for i in range(xp,maxx-minx+2):
                    #print("Looking left at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '#': break
                    if grid[yp][i] == '.': count += 1
                    grid[yp][i] = '~'
                for i in range(xp-1,-1,-1):
                    #print("Looking right at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '#': break
                    if grid[yp][i] == '.': count += 1
                    grid[yp][i] = '~'
            elif right:
                # Spill to the left, one level up
                #print("only right")
                for i in range(xp,maxx-minx+2):
                    #print("Looking left at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '.': count += 1
                    if grid[yp][i] == '#': break
                    grid[yp][i] = '|'
                for i in range(xp-1,-1,-1):
                    #print("Looking right at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '.': count += 1
                    if grid[yp+1][i] != '#' and grid[yp+1][i] != '~':
                        ss += [(i+minx-1, yp)]
                        grid[yp][i] = '|'
                        break
                    grid[yp][i] = '|'
            elif left:
                # Spill to the right, one level up
                #print("only left")
                for i in range(xp,maxx-minx+2):
                    #print("Looking left at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '.': count += 1
                    if grid[yp+1][i] != '#' and grid[yp+1][i] != '~':
                        ss += [(i+minx-1, yp)]
                        grid[yp][i] = '|'
                        break
                    grid[yp][i] = '|'
                for i in range(xp-1,-1,-1):
                    #print("Looking right at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '.': count += 1
                    if grid[yp][i] == '#': break
                    grid[yp][i] = '|'
            else:
                # Spill both directions
                #print("not right and not left")
                for i in range(xp,maxx-minx+2):
                    #print("Looking left at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '.': count += 1
                    if grid[yp+1][i] != '#' and grid[yp+1][i] != '~':
                        ss += [(i+minx-1, yp)]
                        grid[yp][i] = '|'
                        break
                    grid[yp][i] = '|'
                for i in range(xp-1,-1,-1):
                    #print("Looking right at %s" % ( grid[yp][i] ))
                    if grid[yp][i] == '.': count += 1
                    if grid[yp+1][i] != '#' and grid[yp+1][i] != '~':
                        ss += [(i+minx-1, yp)]
                        grid[yp][i] = '|'
                        break
                    grid[yp][i] = '|'
        elif grid[y][x] == '|':
            pass
            # Nothing to do here as we hit a spot already fully processed
        else:
            print("Unexpected stop at %s" % ( grid[y][x] ))

    springs = ss
    #dumpSprings()
    #dumpMap()
    #print("Count = %d or %d" % ( count, countWater() ))


#dumpMap()
print("Standing or flowing water count = %d or %d" % ( count, countWater() ))
print("Standing water count = %d" % ( countStandingWater() ))

