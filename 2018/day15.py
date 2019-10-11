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

printPieces()

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
    # Compute reverse path from chosen node to find the fastest reading order path to there
    dist, prev = dijkstraCore(sorted(found)[0], mindist)

    moves = [(p[0]+dy,p[1]+dx) for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)]
                                             if p[0]+dy >= 0 and p[1]+dx >= 0
                                             and p[0]+dy < len(lines) and p[1]+dx < len(lines[0])]
    return sorted([m for m in moves if lines[m[0]][m[1]] == '.' and m in dist and dist[m] <= mindist])[0]

def takeOneTurn(turn):
    for k,v in sorted(dict(pieces).items()):
        x = k[1]
        y = k[0]

        # Handle pieces killed this turn before we get to them
        if (y,x) not in pieces:
            continue

        #print("Taking turn for %s at %s" % (v[0], k))

        # First, move the piece if needed

        step = dijkstra(k)
        if step != None:
            step = (step[1], step[0]) # TEMPORARY
            #print("Moving piece %s from %s to %s" % ( v[0], (x,y), step ))
            lines[y] = lines[y][:x] + '.' + lines[y][x+1:]
            x, y = step[0], step[1]
            lines[y] = lines[y][:x] + v[0] + lines[y][x+1:]  
            pieces[(y,x)] = pieces.pop(k)

        #print("x,y = %d,%d" % (x,y))

        # Second, attack if possible

        attackingPiece = pieces[(y,x)][0]
        targets = [(pieces[(y+dy,x+dx)][1], (y+dy,x+dx)) for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)]
                   if (y+dy,x+dx) in pieces and pieces[(y+dy,x+dx)][0] != attackingPiece]
        targets = sorted(targets)
        if len(targets) > 0:
            pp = targets[0][1]
            vv = pieces[pp]
            xx, yy = pp[1], pp[0]
            #print("attacking %s - %s" % (p,vv))
            #print("old hitpoints = %d" % (pieces[p][1]))
            attackPower = 3 if vv[0] == 'E' else 25
            pieces[pp] = (vv[0], vv[1] - attackPower)
            #print("new hitpoints = %d" % (pieces[p][1]))
            if pieces[pp][1] <= 0:
                #print("Piece died at %d,%d" % ( yy,xx ))
                del pieces[pp]
                lines[yy] = lines[yy][:xx] + '.' + lines[yy][xx+1:]  
                counts = countPieces()
                if counts['E'] == 0 or counts['G'] == 0:
                    return True

    return False

originalCounts = countPieces()

for i in range(0, 100):
    print()
    print("     === ROUND %d ===" % (i))
    print()
    #printBoard()
    #printPieces()
    if takeOneTurn(i):
        score = 0
        for k,v in sorted(pieces.items()):
            score += v[1]
        print("Game over after %d turns with score %d - outcome = %d or %d" % (i+1, score, (i+1)*score, i*score))
        #printBoard()
        #printPieces()
        break

finalCounts = countPieces()

print("Number of elf deaths: %d" % ( originalCounts['E'] - finalCounts['E'] ))

