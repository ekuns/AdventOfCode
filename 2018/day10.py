#!/usr/bin/python3

import re

f = open("input10.txt", "r")
lines = f.readlines()
f.close()

points = []

for l in lines:
    m = re.search('position=<([^,]+),([^>]+)> velocity=<([^,]+),([^>]+)>', l)
    points.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

def dump():
    for p in points:
        print("(%d,%d) - speed (%d,%d)" % (p[0], p[1], p[2], p[3]))

def limits():
    minx = 9999
    maxx = -9999
    miny = 9999
    maxy = -9999
    for p in points:
        if p[0] < minx: minx = p[0]
        if p[0] > maxx: maxx = p[0]
        if p[1] < miny: miny = p[1]
        if p[1] > maxy: maxy = p[1]
    return (minx, maxx, miny, maxy)

def area():
    l = limits()
    return (l[1] - l[0] + 1) * (l[3] - l[2] + 1)

def step():
    global points
    points = [(p[0] + p[2], p[1] + p[3], p[2], p[3]) for p in points]

def stepback():
    global points
    points = [(p[0] - p[2], p[1] - p[3], p[2], p[3]) for p in points]

def dumpPlot():
    l = limits()
    minx = l[0]
    maxx = l[1]
    miny = l[2]
    maxy = l[3]
    output = []
    for i in range(0, maxy - miny + 2):
        output.append(['.'] * (maxx - minx + 2))
    for p in points:
        output[p[1]-miny+1][p[0]-minx+1] = '#'

    for o in output:
        print(''.join(o))

t = 0
bounds = area()
while True:
    step()
    new = area()
    if new > bounds: break
    t = t + 1
    bounds = new

print("At time t=%d seconds, the result is" % (t))
stepback()
dumpPlot()

