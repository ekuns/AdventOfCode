from collections import deque
from itertools import permutations

f = open("input24.txt", "r")
lines = f.readlines()
f.close()

numbers = {}
for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if lines[y][x].isdigit():
            numbers[lines[y][x]] = (x,y)

print(numbers)

openspots = sum([l.count('.') for l in lines])
print('There are ' + str(openspots) + ' open spots and ' + str(len(numbers)) + ' numbers')

# Now find the path from each number to each other number
def get_unvisited_neighbors(pos, visited, puzzleinput):
    toadd = []
    for point in [(pos[0]+1,pos[1]), (pos[0]-1,pos[1]), (pos[0],pos[1]+1), (pos[0],pos[1]-1)]:
        c = puzzleinput[point[1]][point[0]]
        if c != '#' and not point in visited:
            toadd += [point]
    return toadd

def get_shortest_path(startingpos, puzzleinput):
    startingdigit = puzzleinput[startingpos[1]][startingpos[0]]
    visited = set()
    queue = deque([[startingpos]])

    paths = {}
    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            neighbors = get_unvisited_neighbors(node, visited, puzzleinput)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                c = puzzleinput[neighbor[1]][neighbor[0]]
                if c.isdigit():# and c != '0':
                    if c not in paths.keys():
                        #print('Found path from ' + startingdigit + ' to ' + c + ': ' + str(len(new_path)) + ' steps long')
                        paths[c] = new_path
                        if len(paths) == len(numbers) - 1:
                            return paths
                else:
                    queue.append(new_path)
            visited.add(node)

    return paths

foundpaths = {}
for i in numbers.keys():
    foundpaths[i] = get_shortest_path(numbers[i], lines)


def runProgram(part1=True):
    minlength = 99999999999999999999
    minpath = None

    allbutzero = list(numbers.keys())
    allbutzero.remove('0')
    perm = permutations(allbutzero)
    for p in perm:
        last = '0'
        length = 0
        found = True
        if not part1: p += ('0',)
        for nxt in p:
            if nxt not in foundpaths[last].keys():
                found = False
                break
            length += len(foundpaths[last][nxt]) - 1
            last = nxt
        if found and length < minlength:
            minlength = length
            minpath = p

    return (minlength, minpath)

# Part 1

minlength, minpath = runProgram(True)
print('Minimum path length is ' + str(minlength) + ' for ' + str(minpath))

# Part 2

minlength, minpath = runProgram(False)
print('Minimum path length is ' + str(minlength) + ' for ' + str(minpath))

