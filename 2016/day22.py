from collections import deque
import re
import copy

f = open("input22.txt", "r")
lines = f.readlines()
f.close()

del lines[0] # root@ebhq-gridcenter# df -h
del lines[0] # Filesystem              Size  Used  Avail  Use%

nodes = {}
maxx, maxy = 0, 0
for l in lines:
    m = re.match('^/dev/grid/node-x(\d+)-y(\d+) +(\d+)T +(\d+)T +(\d+)T +(\d+)%$', l.strip())
    if not m:
        print('No match for ' + l)
    x, y, size, used, avail, usedpercent = int(m.group(1)), int(m.group(2)), int(m.group(3)), \
                                           int(m.group(4)), int(m.group(5)), int(m.group(6))
    nodes[(x,y)] = (size, used, avail, usedpercent)
    maxx = max(maxx, x)
    maxy = max(maxy, y)

SIZE = 0
USED = 1
AVAIL = 2

# Part 1

count = 0
for n_key,n_value in nodes.items():
    for m_key,m_value in nodes.items():
        if n_key != m_key and n_value[USED] != 0 and n_value[USED] <= m_value[AVAIL]:
            count += 1

print('Part 1 - The number of viable pairs of nodes is ' + str(count))

# Part 2

nodegrid = []
for y in range(0, maxy + 1):
    row = []
    for x in range(0, maxx + 1):
        n = nodes[(x,y)]
        row += [(n[SIZE], n[USED], n[AVAIL])] # size, used, available
    nodegrid += [row]

def get_next_moves(nodegrid):
    moves = []
    for x in range(0, maxx):
        for y in range(0, maxy):
            for diff in [(-1,0), (1,0), (0,-1), (0,1)]:
                xp, yp = x + diff[0], y + diff[1]
                if xp < 0 or yp < 0 or xp > maxx or yp > maxy:
                    continue
                if nodegrid[y][x][USED] > 0 and nodegrid[y][x][USED] <= nodegrid[yp][xp][AVAIL]:
                    #print(str(nodegrid[y][x]) + ' -> ' + str(nodegrid[yp][xp]))
                    moves += [((x,y),(xp,yp))] # We can move from (x,y) to (xp,yp)

    return moves

print('The number of neighbor viable pairs of nodes is ' + str(len(get_next_moves(nodegrid))))
print('The list of neighbor viable pairs of nodes is ' + str(get_next_moves(nodegrid)))
#print(nodegrid)

# NEED TO FINISH REWRITING THE BELOW TO HANDLE MOVES AND DETECTING END-OF-GAME
# Game is complete when data from y=0,x=max is in y=0,x=0
def get_shortest_path(nodegrid):
    visited = set()
    queue = deque()
    pos = (maxx, 0)

    # Add initial moves
    moves = get_next_moves(nodegrid)
    for move in moves:
        new_path = (move, pos, copy.deepcopy(nodegrid))
        queue.append(new_path)

    while queue:
        path = queue.popleft()
        node = path[0][-1]

        if node not in visited:
            moves = get_next_moves(nodegrid)
            for move in moves:
                new_path = list(path[0])
                new_path.append(move)
                pos = path[1]
                nodegrid = path[2]

                x, y, dx, dy = move[0][0], move[0][1], move[1][0], move[1][1]
                if (x,y) == (36,0): print('Found it')

                newgrid = copy.deepcopy(nodegrid)
                old = newgrid[y][x]
                new = newgrid[dy][dx]
                #print((x,y),(dx,dy))
                moveused = old[USED]
                newgrid[y][x] = (old[SIZE], old[USED]-moveused, old[AVAIL]+moveused)
                newgrid[dy][dx] = (new[SIZE], new[USED]+moveused, new[AVAIL]-moveused)

                new_item = (new_path, pos, newgrid)
                if (x,y) == pos:
                    print('moved the target')
                    pos = (xp,yp)
                    if pos == (0,0):
                        return new_path
                new_item = (new_path, pos, newgrid)
                queue.append(new_item)
            visited.add(node)

    return 'No path exists'

p = get_shortest_path(nodegrid)
print(p)

