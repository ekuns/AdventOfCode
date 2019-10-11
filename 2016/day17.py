from collections import deque
from hashlib import md5

f = open("input17.txt", "r")
puzzleinput = f.read().strip()
f.close()

print('Puzzle input ' + puzzleinput)

def dohash(s):
    return(md5(s.encode('utf-8')).hexdigest())

def get_unvisited_neighbors(node, visited, puzzleinput):
    path = node[1]
    h = dohash(puzzleinput+path)
    hh = [False if h[i].isdigit() or h[i] == 'a' else True for i in range(0, 4)]

    toadd = []
    pos = node[0]
    for step in [('R',(pos[0]+1,pos[1]), hh[3]), ('L', (pos[0]-1,pos[1]), hh[2]),
                 ('D',(pos[0],pos[1]+1), hh[1]), ('U', (pos[0],pos[1]-1), hh[0])]:
        direction = step[0]
        point = step[1]
        isunlocked = step[2]
        if point[0] >= 0 and point[1] >= 0 and point[0] < 4 and point[1] < 4 \
                and not point in visited and isunlocked:
            toadd += [(point,path+direction)]
    return toadd

def get_shortest_path(startingpos, destination, puzzleinput):
    visited = set()
    queue = deque([[(startingpos,'')]])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            neighbors = get_unvisited_neighbors(node, visited, puzzleinput)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor[0] == destination:
                    return new_path
                visited.add(node)

    return None

startingpos = (0,0)
destination = (3,3)

def run_part1(test):
    path = get_shortest_path(startingpos, destination, test)
    if not path:
        print('No solution found for ' + test)
    else:
        print('The shortest path for ' + test + ' is ' + path[-1][1])

#print(get_unvisited_neighbors(((0,0), ''), set(), 'ihgpwlah'))
#print(get_unvisited_neighbors(((0,1), 'D'), set(), 'ihgpwlah'))

run_part1('ihgpwlah')
run_part1('kglvqrro')
run_part1('ulqzkmiv')

# Part 1 

print()
print('Part 1 answer:')
run_part1(puzzleinput)

# Part 2

def get_longest_path(startingpos, destination, puzzleinput):
    visited = set()
    queue = deque([[(startingpos,'')]])

    maxlen = 0
    while queue:
        path = queue.popleft()
        node = path[-1]

        if node not in visited:
            neighbors = get_unvisited_neighbors(node, visited, puzzleinput)
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                if neighbor[0] == destination:
                    maxlen = max(maxlen, len(neighbor[1]))
                else:
                    queue.append(new_path)
                visited.add(node)

    return maxlen

def run_part2(test):
    length = get_longest_path(startingpos, destination, test)
    print('The max length is ' + str(length) + ' for ' + test)

run_part2('ihgpwlah')
run_part2('kglvqrro')
run_part2('ulqzkmiv')

print()
print('Part 2 answer:')
run_part2(puzzleinput)

