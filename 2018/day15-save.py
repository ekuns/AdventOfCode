#!/usr/bin/python3

import re
import os

f = open("input15.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

def printBoard():
    iii = 0
    for l in lines:
        zzz = [v[1] for k,v in sorted(pieces.items()) if k[0] == iii]
        print(l + ' ' + ','.join(map(str,zzz)))
        iii += 1

pieces = {}
for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        p = lines[y][x]
        if p == 'G' or p == 'E':
            pieces[(y,x)] = (p, 200)

def printPieces():
    for k,v in sorted(pieces.items()):
        print("%s - %s" % (k,v))

def countPieces():
    sums = {'G': 0, 'E': 0}
    for k,v in sorted(pieces.items()):
        sums[v[0]] += 1
    return sums

for k,v in sorted(pieces.items()):
    print("%s - %s" % ((k[1],k[0]),v))

def dijkstraCore(p, stopAt=9999):
    vertices = set()
    dist = {}
    prev = {}
    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if lines[y][x] in '.GE':
                dist[(y,x)] = 9999
                prev[(y,x)] = None
                vertices.add((y,x))

    dist[p] = 0

    # Find the unvisited node with the minimum distance
    while len([v for v in vertices if dist[v] < 9999]) > 0:
        mindist = 9999
        minnode = None
        for v in vertices:
            if dist[v] < mindist:
                mindist = dist[v]
                minnode = v

        vertices.remove(minnode)

        # Stop navigating if we hit a piece
        if lines[minnode[0]][minnode[1]] in 'EG' and not dist[minnode] == 0:
            continue

        # Find neighbors of that node
        dst = dist[minnode]
        if dst <= stopAt:
            for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)]:
                node = (minnode[0]+dy,minnode[1]+dx)
                #print("Looking at node %s with distance %d" % (node, dist[node] if node in dist else 0))
                if node in vertices and dst + 1 < dist[node]:
                    #print("Distance %d for neighbor %s" % (dst + 1, node))
                    dist[node] = dst + 1
                    prev[node] = minnode
                #else:
                #    print("No match for neighbor %s dist %d" % (node, dist[node] if node in dist else 0))

    # Remove unreachable items from our working lists
    for v in vertices:
        del dist[v]
        del prev[v]

    return dist, prev

def dijkstra(p, stopAt=9999):
    dist, prev = dijkstraCore(p, stopAt)

    piece = pieces[p][0]

    # See if we have any legal moves toward an emeny
    pieceDist = [dist[key] for key in pieces if key in prev and prev[key] and piece != pieces[key][0]]
    if len(pieceDist) == 0:
        return None

    # Find distance to closest enemy
    mindist = min(pieceDist)
    if mindist == 1:
        return None  # We don't move pieces already next to an enemy

    # Get all enemies at the closest distance
    found = [key for key in pieces if key in prev and prev[key] and piece != pieces[key][0] and dist[key] == mindist]
    if len(found) == 0:
        return None  # If no path found, we cannot move this piece

    # Sorting puts the destination pieces in reading order, then take the first.
    # Compute reverse path from chosen node.
    dist, prev = dijkstraCore(sorted(found)[0], mindist+5)
    ppp = [(p[0]+dy,p[1]+dx) for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)]]
    ll = []
    for pp in ppp:
        if pp[0] >= 0 and pp[1] >= 0 and pp[0] < len(lines) and pp[1] < len(lines[0]):
            if lines[pp[0]][pp[1]] == '.' and pp in dist and dist[pp] <= mindist:
                ll += [(dist[pp], pp)]
    if len(ll) == 0: print("Different: len = 0")
    return sorted(ll)[0][1]
    #return sorted([pp for pp in ppp if pp[0] >= 0 and pp[1] >= 0 and pp[0] < len(lines) and pp[1] < len(lines[0]) and lines[pp[0]][pp[1]] == '.' and pp in dist and dist[pp] <= mindist])[0]

def findNextStep(key, v, turn):
    board = lines[:]
    piece = v[0]
    opponents = []
    adjacent = False
    distance = {}

    def getMin(p, value):
        val = distance[p]
        if val == 0 or (val > 0 and val > value):
            distance[p] = value
            return True
        return False

    def dumpItemizedBoard():
        bbb = []
        for bb in board:
            bbb += [list(bb)]
        for y in range(0, len(board)):
            for x in range(0, len(board[y])):
                if distance[(x,y)] > 0:
                    bbb[y][x] = str(distance[(x,y)])
        for b in bbb:
            print('-'.join(b))
        print()
        #for y in range(0, len(board)):
        #    for x in range(0, len(board[y])):
        #        if distance[(x,y)] > 0:  board[y] = board[y][:x] + str(distance[(x,y)]) + board[y][x+1:]
        #for b in board:
        #    print(''.join(b))
        #print()
        ####for d in distance:
        ####    print("%s - %s" % ( d, distance[d] ))

    for y in range(0, len(board)):
        for x in range(0, len(board[y])):
            if board[y][x] == '#':
                distance[(x,y)] = -1 # Can't move into walls
            elif board[y][x] == '.':
                if not (x,y) in distance: distance[(x,y)] = 0 # Open space
            elif board[y][x] == piece:
                distance[(x,y)] = -1 # Can't move onto my peer
            else:
                distance[(x,y)] = -1 # Can't move onto my enemy
                opponents += [(x,y)]
                if distance.get((x-1,y),1) >= 0:  distance[(x-1,y)] = 1
                if distance.get((x+1,y),1) >= 0:  distance[(x+1,y)] = 1
                if distance.get((x,y-1),1) >= 0:  distance[(x,y-1)] = 1
                if distance.get((x,y+1),1) >= 0:  distance[(x,y+1)] = 1
                if abs(x-key[0]) == 1 and y == key[1]: adjacent = True
                if x == key[0] and abs(y-key[1]) == 1: adjacent = True
    #print("Opponents of %s at %s are at %s" % (piece, key, opponents))
    if adjacent:
        #print("This piece will not move because one piece is already in range")
        return None

    changed = True
    while changed:
        changed = False
        for k,v in distance.items():
            x = k[0]
            y = k[1]
            p = distance[(x,y)]
            if p > 0:
                changed |= getMin((x-1,y), p + 1)
                changed |= getMin((x+1,y), p + 1)
                changed |= getMin((x,y-1), p + 1)
                changed |= getMin((x,y+1), p + 1)
    #dumpItemizedBoard()
    x, y = key
    m = 9999

    if distance.get((x-1,y)) > 0:   m = min(m, distance.get((x-1,y)))
    if distance.get((x+1,y)) > 0:   m = min(m, distance.get((x+1,y)))
    if distance.get((x,y-1)) > 0:   m = min(m, distance.get((x,y-1)))
    if distance.get((x,y+1)) > 0:   m = min(m, distance.get((x,y+1)))
    #print("Minimum step = %d" % ( m ))
    if m > 0 and m != 9999:
        if distance.get((x,y-1)) == m: return (x,y-1)
        if distance.get((x-1,y)) == m: return (x-1,y)
        if distance.get((x+1,y)) == m: return (x+1,y)
        return (x,y+1)

    return None

def takeOneTurn(turn):
    for k,v in sorted(dict(pieces).items()):
        x = k[1]
        y = k[0]

        # Handle pieces killed this turn before we get to them
        if (y,x) not in pieces:
            continue

        #print("Taking turn for %s at %s" % (v[0], k))

        # First, move the piece if needed
        step = findNextStep((x,y), v, turn)
        step2 = dijkstra(k)
        if step2: step2 = (step2[1], step2[0]) # TEMPORARY
        if step != step2:
            print("Different step results for round %d piece %s from the two methods: %s, %s" % (turn, k, step, step2))

        if step != None:
            print("Moving piece %s from %s to %s" % ( v[0], (x,y), step2 ))
            lines[y] = lines[y][:x] + '.' + lines[y][x+1:]
            x, y = step2[0], step2[1]
            lines[y] = lines[y][:x] + v[0] + lines[y][x+1:]  
            pieces[(y,x)] = pieces.pop(k)

        #print("x,y = %d,%d" % (x,y))

        # Second, attack if possible

        p1 = pieces.get((y-1,x), None)
        p2 = pieces.get((y,x-1), None)
        p3 = pieces.get((y,x+1), None)
        p4 = pieces.get((y+1,x), None)

        attackingPiece = pieces[(y,x)][0]
        if p1 != None and p1[0] == attackingPiece:  p1 = None
        if p2 != None and p2[0] == attackingPiece:  p2 = None
        if p3 != None and p3[0] == attackingPiece:  p3 = None
        if p4 != None and p4[0] == attackingPiece:  p4 = None

        minHP = 9999
        if p1 != None:  minHP = min(minHP, p1[1])
        if p2 != None:  minHP = min(minHP, p2[1])
        if p3 != None:  minHP = min(minHP, p3[1])
        if p4 != None:  minHP = min(minHP, p4[1])

        def attack(p):
            vv = pieces[p]
            #print("attacking %s - %s" % (p,vv))
            #print("old hitpoints = %d" % (pieces[p][1]))
            attackPower = 3 if vv[0] == 'E' else 25
            pieces[p] = (vv[0], vv[1] - attackPower)
            #print("new hitpoints = %d" % (pieces[p][1]))
            if pieces[p][1] <= 0:
                print("Piece died at %d,%d" % ( p[1],p[0] ))
                del pieces[p]
                lines[p[0]] = lines[p[0]][:p[1]] + '.' + lines[p[0]][p[1]+1:]  

        if minHP != 9999:
            if p1 != None and p1[1] == minHP: attack((y-1,x))
            elif p2 != None and p2[1] == minHP: attack((y,x-1))
            elif p3 != None and p3[1] == minHP: attack((y,x+1))
            else: attack((y+1,x))
            counts = countPieces()
            if counts['E'] == 0 or counts['G'] == 0:
                return True

    return False

originalCounts = countPieces()

for i in range(0, 100):
#for i in range(0, 1):
    print()
    print("     === ROUND %d ===" % (i))
    print()
    printBoard()
    printPieces()
    if takeOneTurn(i):
        score = 0
        for k,v in sorted(pieces.items()):
            score += v[1]
        print("Game over after %d turns with score %d - outcome = %d or %d" % (i+1, score, (i+1)*score, i*score))
        printBoard()
        printPieces()
        break

finalCounts = countPieces()

print("Number of elf deaths: %d" % ( originalCounts['E'] - finalCounts['E'] ))

