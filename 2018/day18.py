#!/usr/bin/python3

import re
import os

f = open("input18.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

def countNeighbors(x,y, board):
    counts = {'.': 0, '|': 0, '#': 0}
    if y > 0:
        if x > 0: counts[board[y-1][x-1]] += 1
        counts[board[y-1][x]] += 1
        if x < len(board[0])-1: counts[board[y-1][x+1]] += 1

    if x > 0: counts[board[y][x-1]] += 1
    if x < len(board[0])-1: counts[board[y][x+1]] += 1

    if y < len(board)-1:
        if x > 0: counts[board[y+1][x-1]] += 1
        counts[board[y+1][x]] += 1
        if x < len(board[0])-1: counts[board[y+1][x+1]] += 1
    return counts

def step():
    board = lines[:]
    changed = False
    for x in range(0, len(lines[0])):
        for y in range(0, len(lines)):
            neighbors = countNeighbors(x,y,board)
            if board[y][x] == '.': # If open
                if neighbors['|'] >= 3:
                    changed = True
                    lines[y] = lines[y][:x] + '|' + lines[y][x+1:]
            elif board[y][x] == '|': # If trees
                if neighbors['#'] >= 3:
                    changed = True
                    lines[y] = lines[y][:x] + '#' + lines[y][x+1:]
            else: # If lumberyard
                if neighbors['#'] == 0 or neighbors['|'] == 0:
                    changed = True
                    lines[y] = lines[y][:x] + '.' + lines[y][x+1:]
    return changed

def dumpBoard():
    for l in lines:
        print(''.join(l))
    print()

for i in range(0, 10):
    step()
    dumpBoard()

counts = {'.': 0, '|': 0, '#': 0}
for x in range(0, len(lines[0])):
    for y in range(0, len(lines)):
        counts[lines[y][x]] += 1

print(counts)
print(counts['|'] * counts['#'])

# Part 2

for i in range(10, 1000):
    step()

values = []
for i in range(1000, 1050):
    if not step():
        print("Stopped changing")
        break

    counts = {'.': 0, '|': 0, '#': 0}
    for x in range(0, len(lines[0])):
        for y in range(0, len(lines)):
            counts[lines[y][x]] += 1
    #print(counts)
    print("%d: %d" % (i+1, counts['|'] * counts['#']))
    values += [counts['|'] * counts['#']]

print(values)
print(values[0] == values[35])
print(values[1] == values[36])
print(values[2] == values[37])

end = 1000000000
#end = 1102
remaining = end - 1051
delta = remaining % 35
print("Final score = %d" % ( values[len(values)-35+delta] ))

if end < 10000:
    for i in range(1050, end):
        step()

    counts = {'.': 0, '|': 0, '#': 0}
    for x in range(0, len(lines[0])):
        for y in range(0, len(lines)):
            counts[lines[y][x]] += 1
    #print(counts)
    print("%d: %d" % (i+1, counts['|'] * counts['#']))

