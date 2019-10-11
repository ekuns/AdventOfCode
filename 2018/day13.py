#!/usr/bin/python3
from collections import deque

f = open("input13.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

carts = {}
for y in range(0, len(lines)):
    l = lines[y]
    for x in range(0, len(l)):
        c = l[x]
        if c in "<>":
            carts[(x,y)] = (deque("l-r"), c)
            lines[y] = l[:x] + '-' + l[x+1:]
        elif c in "^v":
            carts[(x,y)] = (deque("l-r"), c)
            lines[y] = l[:x] + '|' + l[x+1:]

def dumpPieces():
    for k,v in sorted(carts.items()):
        print("%s,%s" % (k,v))

def dumpBoard():
    for l in lines:
        print(l)

def dumpPopulatedBoard():
    popLines = lines[:]
    for k,v in carts.items():
        x = k[0]
        y = k[1]
        popLines[y] = popLines[y][:x] + v[1] + popLines[y][x+1:]
    for l in popLines:
        print(l)

def takeStep():
    collision = None
    for k,v in sorted(carts.items()):
        pos = k
        turns = v[0]
        piece = v[1] 

        #print("Moving piece %s at %s with current turns %s" % (piece, pos, turns))
  
        if piece == '^':
            nextpos = (pos[0], pos[1] - 1)
            nextpiece = lines[nextpos[1]][nextpos[0]]
            if nextpiece == '|':
                pass
            elif nextpiece == '/':
                piece = '>'
            elif nextpiece == '\\':
                piece = '<'
            elif nextpiece == '+':
                nextTurn = turns.popleft()
                turns.append(nextTurn)
                if nextTurn == 'l':
                    piece = '<'
                elif nextTurn == 'r':
                    piece = '>'
            else:
                print("Piece %s, %s OFF THE BOARD on '%s'" % ( k, v, nextpiece ))
                dumpPieces()
                dumpPopulatedBoard()
                return True
        elif piece == 'v':
            nextpos = (pos[0], pos[1] + 1)
            nextpiece = lines[nextpos[1]][nextpos[0]]
            if nextpiece == '|':
                pass
            elif nextpiece == '/':
                piece = '<'
            elif nextpiece == '\\':
                piece = '>'
            elif nextpiece == '+':
                nextTurn = turns.popleft()
                turns.append(nextTurn)
                if nextTurn == 'l':
                    piece = '>'
                elif nextTurn == 'r':
                    piece = '<'
            else:
                print("Piece %s, %s OFF THE BOARD on '%s'" % ( k, v, nextpiece ))
                dumpPieces()
                dumpPopulatedBoard()
                return True
        elif piece == '>':
            nextpos = (pos[0] + 1, pos[1])
            nextpiece = lines[nextpos[1]][nextpos[0]]
            if nextpiece == '-':
                pass
            elif nextpiece == '/':
                piece = '^'
            elif nextpiece == '\\':
                piece = 'v'
            elif nextpiece == '+':
                nextTurn = turns.popleft()
                turns.append(nextTurn)
                if nextTurn == 'l':
                    piece = '^'
                elif nextTurn == 'r':
                    piece = 'v'
            else:
                print("Piece %s, %s OFF THE BOARD on '%s'" % ( k, v, nextpiece ))
                dumpPieces()
                dumpPopulatedBoard()
                return True
        elif piece == '<':
            nextpos = (pos[0] - 1, pos[1])
            nextpiece = lines[nextpos[1]][nextpos[0]]
            if nextpiece == '-':
                pass
            elif nextpiece == '/':
                piece = 'v'
            elif nextpiece == '\\':
                piece = '^'
            elif nextpiece == '+':
                nextTurn = turns.popleft()
                turns.append(nextTurn)
                if nextTurn == 'l':
                    piece = 'v'
                elif nextTurn == 'r':
                    piece = '^'
            else:
                print("Piece %s, %s OFF THE BOARD on '%s'" % ( k, v, nextpiece ))
                dumpPieces()
                dumpPopulatedBoard()
                return True
        else:
            print("INVALID PIECE")

        try:
            del carts[pos]
        except:
            continue

        #print("Next position %s at piece %s" % (nextpos, nextpiece))
        if nextpos in carts.keys():
            print("COLLISION")
            # Part 1 code:
            #collision = nextpos
            #break
            # Part 2 code:
            del carts[nextpos]
        else:
            carts[nextpos] = (turns, piece)

    return collision

#dumpPieces()
#dumpPopulatedBoard()

i = 0
while True:
    i += 1
    pos = takeStep()
    if pos:
        print("COLLISION in step %d at %s" % (i, pos))
        break

    if len(carts.keys()) == 1:
        print("Only one cart is left at %s" % ( carts.keys() ))
        break
    #dumpPieces()
    #dumpPopulatedBoard()

