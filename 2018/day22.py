#!/usr/bin/python3

import re

#f = open("input22.txt", "r")
#lines = f.readlines()
#f.close()
#
#lines = [l.rstrip('\r\n') for l in lines]

depth = 510
target = (10,10)

depth  = 3879
target = (8,713)

geologicIndex = {}

def erosion(p):
    return (geologicIndex[p] + depth) % 20183

for x in range(0, target[0]+1):
    for y in range(0, target[1]+1):
        if (x,y) == (0,0):    geologicIndex[(x,y)] = 0
        elif (x,y) == target: geologicIndex[(x,y)] = 0
        elif x == 0:          geologicIndex[(x,y)] = y * 48271
        elif y == 0:          geologicIndex[(x,y)] = x * 16807
        else:                 geologicIndex[(x,y)] = erosion((x-1,y)) * erosion((x,y-1))

def plot():
    for y in range(0, target[1]+1):
        s = ''
        for x in range(0, target[0]+1):
            e = erosion((x,y)) % 3
            if e == 0:    s += '.'
            elif e == 1:  s += '='
            else:         s += '|'
        print(s)

def risk():
    risk = 0
    for y in range(0, target[1]+1):
        for x in range(0, target[0]+1):
            risk += erosion((x,y)) % 3
    return risk

plot()

print("Risk = %d" % ( risk() ))

