import re
import queue
from itertools import combinations
import copy
import time

start_time = time.time()

f = open("input11.txt", "r")
lines = f.readlines()
f.close()

#floors = []
#floors += [['Tm-M', 'Pu-M' ]]
#floors += [['Tm-G']]
#floors += [['Pu-G']]
#floors += [[]]

floors = []
floors += [['Tm-G', 'Tm-M', 'Pu-G', 'Sr-G']]
floors += [['Pu-M', 'Sr-M']]
floors += [['Pm-G', 'Pm-M', 'Ru-G', 'Ru-M']]
floors += [[]]

elevator = 0
def dump(fl, current):
    for i in range(3, -1, -1):
        e = ' E ' if current == i else '   '
        tmg = ' Tm-G ' if 'Tm-G' in fl[i] else '      '
        tmm = ' Tm-M ' if 'Tm-M' in fl[i] else '      '
        pug = ' Pu-G ' if 'Pu-G' in fl[i] else '      '
        pum = ' Pu-M ' if 'Pu-M' in fl[i] else '      '
        srg = ' Sr-G ' if 'Sr-G' in fl[i] else '      '
        srm = ' Sr-M ' if 'Sr-M' in fl[i] else '      '
        pmg = ' Pm-G ' if 'Pm-G' in fl[i] else '      '
        pmm = ' Pm-M ' if 'Pm-M' in fl[i] else '      '
        rug = ' Ru-G ' if 'Ru-G' in fl[i] else '      '
        rum = ' Ru-M ' if 'Ru-M' in fl[i] else '      '
        print('F' + str(i+1) + e + tmg + tmm + pug + pum + srg + srm + pmg + pmm + rug + rum)

dump(floors, elevator)

q = queue.Queue()
q.put((0, elevator, None, floors))

# If any generators on are a floor, and any chips are on that same floor that aren't
# connected to their corresponding generator, then the game is over.
def gameLost(fl, current):
    generators = any([i for i in fl[current] if i.endswith('-G')])
    unpairedchips = any([i for i in fl[current] if i.endswith('-M') and
                                                   i.replace('-M', '-G') not in fl[current]])
    return generators and unpairedchips


def gameWon(fl, current):
    return not fl[0] and not fl[1] and not fl[2]


# Change this to apply to this day
def get_unvisited_neighbors(pos, visited, puzzleinput):
    # Don't want to move one generator and a different chip
    # If I have multiple pairs on the current floor, there's no reason to try
    # to move both pairs.
    toadd = []
    for point in [(pos[0]+1,pos[1]), (pos[0]-1,pos[1]), (pos[0],pos[1]+1), (pos[0],pos[1]-1)]:
        if point[0] >= 0 and point[1] >= 0 and not point in visited and not isWall(point, puzzleinput):
            toadd += [point]
    return toadd

# Change this to apply to this day
def get_shortest_path(startingpos, destination, puzzleinput):
    visited = set()
    queue = deque([[startingpos]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            neighbors = get_unvisited_neighbors(node, visited, puzzleinput)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor == destination:
                    return new_path
            visited.add(node)

    return 'No path exists'

print('Time taken is ' + str(time.time() - start_time))

