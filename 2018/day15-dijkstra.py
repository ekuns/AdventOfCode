#!/usr/bin/python3

# Round 0
lines0 = [
  '################################',
  '#######################.########',
  '######################....######',
  '#######################.....####',
  '##################..##......####',
  '###################.##.....#####',
  '###################....G...#####',
  '##################....G....#####',
  '############....G.G.G...#..#####',
  '##############...##....##.######',
  '############...#..G............#',
  '###########......E.............#',
  '###########...#####..E........##',
  '#...#######..#######.......#####',
  '#..#..G....G#########.........##',
  '#..#....G...#########..#....####',
  '##.....G....#########.E......###',
  '#####G.....G#########..E.....###',
  '#####.......#########....#.....#',
  '#####G#G....G#######.......#..E#',
  '###.....G.....#####....#.#######',
  '###......G.....G.G.......#######',
  '###..................#..########',
  '#####...................########',
  '#####..............#...#########',
  '####......G........#.E.#E..#####',
  '####.###.........E...#E...######',
  '####..##........#...##.....#####',
  '########.#......######.....#####',
  '########...E....#######....#####',
  '#########...##..########...#####',
  '################################'
]
#Round 17 with attack strength of 25 is where a piece takes a wrong move
lines17 = [
  '################################',
  '#######################.########',
  '######################....######',
  '#######################.....####',
  '##################..##......####',
  '###################.##.....#####',
  '###################........#####',
  '##################.........#####',
  '############......E.....#..#####',
  '##############...##....##.######',
  '############...#.G.E...........#',
  '###########......E.GE..........#',
  '###########...#####.E.........##',
  '#...#######..#######.......#####',
  '#..#........#########.........##',
  '#..#........#########..#....####',
  '##..........#########........###',
  '#####.......#########........###',
  '#####.......#########....#.....#',
  '#####.#......#######.......#...#',
  '###........G..#####....#.#######',
  '###...........GE.........#######',
  '###.........G.GE.....#..########', # <--- This Goblin (22,12) moves to the left instead of down
  '#####........GE.........########',
  '#####........GE....#...#########',
  '####...............#...#...#####',
  '####.###.............#....######',
  '####..##..GE....#...##.....#####',
  '########.#.G....######.....#####',
  '########........#######....#####',
  '#########...##..########...#####',
  '################################']

lines = lines0

pieces = {}
for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        p = lines[y][x]
        if p == 'G' or p == 'E':
            pieces[(y,x)] = (p, 200)

def printBoard():
    iii = 0
    for l in lines:
        zzz = [v[1] for k,v in sorted(pieces.items()) if k[0] == iii]
        print(l + ' ' + ','.join(map(str,zzz)))
        iii += 1

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

    # Sorting puts the destination pieces in reading order, then take the first
    #print("Piece %s can move to %d closest enemies: %s" % (p, len(found), found))
    # Compute reverse path from chosen node
    dist, prev = dijkstraCore(sorted(found)[0], mindist)
    ppp = [(p[0]+dy,p[1]+dx) for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)]]
    print(dist)

    if p == (8,18):
        board = lines[:]
        for y in range(0, len(board)):
            for x in range(0, len(board[y])):
               if (y,x) in dist and dist[(y,x)] <= 9 and board[y][x] == '.':
                   board[y] = board[y][:x] + str(dist[(y,x)]) + board[y][x+1:]
        for b in board:
            print(b)

    ll = []
    for pp in ppp:
        if pp[0] >= 0 and pp[1] >= 0 and pp[0] < len(lines) and pp[1] < len(lines[0]):
            if lines[pp[0]][pp[1]] == '.' and pp in dist and dist[pp] <= mindist:
                ll += [(dist[pp], pp)]
    if len(ll) == 0: print("Different: len = 0")
    return sorted(ll)[0][1]
    #return sorted([pp for pp in ppp if pp in dist and dist[pp] <= mindist])[0]

    #while node:
    #    if prev[node] == p: break
    #    node = prev[node]
    #print("Running algo again returns %s" % (dj))
    #return node

print("There are %d nodes total" % (len(pieces)))
for k,v in pieces.items():
    #print("Looking at %s - %s" % (k1,v1))
    node = dijkstra(k)
    if node:
        print("The next step is from %s -> %s" % (k, node))
    #else:
    #    print("Node %s has no next move %d" % (k, 0))

