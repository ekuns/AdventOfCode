import re
import queue
from itertools import combinations
import copy

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


visited = set()
newTurnProcessed = 0

# FIXME Need to keep track of visited nodes to prune the list of choices
def processQueue(item):
    global q, newTurnProcessed, visited

    turn, current, items, fl = item

    #print('Turn ' + str(turn) + ', floor ' + str(current) + ', items on elevator = ' + str(items))
    if turn > newTurnProcessed:
        newTurnProcessed = turn
        print('Starting ' + str(turn) + ' with ' + str(q.qsize()) + ' items in the queue')

    # Take items from elevator and put them on this floor
    fl = copy.deepcopy(fl)
    if items: fl[current] += items
    if gameLost(fl, current):
        #print('GAME LOST')
        return

    if gameWon(fl, current):
        print('GAME WON after ' + str(turn) + ' turns')
        q = queue.Queue()
        return

    visited.add(tuple([tuple(x) for x in fl]))

    down = current > 0
    up = current < 3

    # Make a new turn, get all 1 and 2 item combos of what is on the current floor
    ones = [(i,) for i in fl[current]]
    twos = list(combinations(fl[current], 2))

    if up:
        upcombos = twos if twos else ones
        for c in upcombos:
            fl2 = copy.deepcopy(fl)
            for x in c:
                fl2[current].remove(x)
            v = copy.deepcopy(fl2)
            v[current+1] += c
            v = tuple([tuple(x) for x in v])
            if not v in visited:
                q.put((turn+1, current+1, c, fl2))

    if down:
        downcombos = ones
        for c in downcombos:
            fl2 = copy.deepcopy(fl)
            for x in c:
                fl2[current].remove(x)
            v = copy.deepcopy(fl2)
            v[current-1] += c
            v = tuple([tuple(x) for x in v])
            if not v in visited:
                q.put((turn+1, current-1, c, fl2))

    #for c in combos:
    #    fl2 = copy.deepcopy(fl)
    #    for x in c:
    #        fl2[current].remove(x)
    #    if up:
    #        v = copy.deepcopy(fl2)
    #        v[current+1] += c
    #        v = tuple([tuple(x) for x in v])
    #        if not v in visited:
    #            q.put((turn+1, current+1, c, fl2))
    #    if down:
    #        v = copy.deepcopy(fl2)
    #        v[current-1] += c
    #        v = tuple([tuple(x) for x in v])
    #        if not v in visited:
    #            q.put((turn+1, current-1, c, fl2))

while not q.empty():
    processQueue(q.get())

