#!/usr/bin/python3

import sys

if (len(sys.argv) < 3):
    print("Supply two arguments:  1) Number of players, 2) Number of marbles")
    sys.exit()

playercount = int(sys.argv[1])
marblecount = int(sys.argv[2])
print("Number of players: %d" % ( playercount ))
print("Number of marbles: %d" % ( marblecount ))

scores = [0] * playercount
marbles = [0]
currentIndex = 0
currentPlayer = 1

def dumpBoard():
    for i in range(0, len(marbles)):
        if (currentIndex == i):
            print("(%d)" % (marbles[i]), end=" ")
        else:
            print(marbles[i], end=" ")
    print()

for i in range(1, marblecount):
    insertAt = (currentIndex + 1) % len(marbles) + 1
    #print("inserting %d at offset %d" % (i, insertAt))
    if i % 23 != 0:
        marbles.insert(insertAt, i)
        currentIndex = insertAt
    else:
        deleteAt = (currentIndex + len(marbles) - 7) % len(marbles)
        scores[currentPlayer-1] += i + marbles[deleteAt]
        #dumpBoard()
        #print("Player %d deleting marble %d aka %d" % (playercount, deleteAt, marbles[deleteAt]))
        del marbles[deleteAt]
        currentIndex = deleteAt
        #dumpBoard()

    #dumpBoard()
    currentPlayer = (currentPlayer + 1) % playercount

#print("Final board is")
#dumpBoard()
#print("Final scores are: %s" % (scores))
print("High score is %d" % (max(scores)))

