#!/usr/bin/python3

import sys
from collections import deque

if (len(sys.argv) < 3):
    print("Supply two arguments:  1) Number of players, 2) Number of marbles")
    sys.exit()

playercount = int(sys.argv[1])
marblecount = int(sys.argv[2])
print("Number of players: %d" % ( playercount ))
print("Number of marbles: %d" % ( marblecount ))

scores = [0] * playercount
marbles = deque([0], marblecount)
currentPlayer = 1
rotation = 0

def dumpBoard():
    marbles.rotate(-rotation)
    for i in range(0, len(marbles)):
        if i == len(marbles) - rotation - 1:
            print("(%d)" % (marbles[i]), end=" ")
        else:
            print(marbles[i], end=" ")
    print()
    marbles.rotate(rotation)

for i in range(1, marblecount+1):
    if i % 23 != 0:
        marbles.rotate(-1)
        rotation = (rotation + len(marbles) - 1) % len(marbles)
        marbles.append(i)
    else:
        marbles.rotate(7)
        scores[currentPlayer-1] += i + marbles.pop()
        marbles.rotate(-1)
        rotation = (rotation + 7 - 1) % len(marbles)

    #dumpBoard()
    currentPlayer = (currentPlayer + 1) % playercount

#print("Final board is")
#dumpBoard()
#print("Final scores are: %s" % (scores))
print("High score is %d" % (max(scores)))

