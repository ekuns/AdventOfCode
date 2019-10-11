from collections import deque

f = open("input13.txt", "r")
puzzleinput = int(f.read().strip())
f.close()

print('Puzzle input ' + str(puzzleinput))


def isWall(point, puzzleinput):
    x = point[0]
    y = point[1]
    return False if bin(x*x + 3*x + 2*x*y + y + y*y + puzzleinput).count("1") % 2 == 0 else True


def get_unvisited_neighbors(pos, visited, puzzleinput):
    toadd = []
    for point in [(pos[0]+1,pos[1]), (pos[0]-1,pos[1]), (pos[0],pos[1]+1), (pos[0],pos[1]-1)]:
        if point[0] >= 0 and point[1] >= 0 and not point in visited and not isWall(point, puzzleinput):
            toadd += [point]
    return toadd

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


for y in range(0, 7):
    s = ''
    for x in range(0, 10):
        s += '#' if isWall((x,y),10) else '.'
    print(s)

print()
print(get_unvisited_neighbors((1,1), set(), 10))
print()
path = get_shortest_path((1,1), (7,4), 10)
print('The shortest path for the test is ' + str(len(path)) + ': ' + str(path))
print('The number of steps for the test is ' + str(len(path)-1))
print()

# Part 1

startingpos = (1,1)
destination = (31,39)

path = get_shortest_path(startingpos, destination, puzzleinput)
print('The number of steps for Part 1 is ' + str(len(path)-1))
print()

# Part 2

def get_visited_points(startingpos, distance, puzzleinput):
    visited = set()
    queue = deque([[startingpos]])
    # We don't want to count the starting point in our distance
    # as we're counting STEPS from the starting point
    goal_distance = distance + 1

    while queue:
        path = queue.popleft()

        node = path[-1]
        if node not in visited:
            neighbors = get_unvisited_neighbors(node, visited, puzzleinput)
            visited.add(node)
            if len(path) == goal_distance:
                continue
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return visited

def dump_map(visited, puzzleinput):
    max_x = max([p[0] for p in visited])
    max_y = max([p[1] for p in visited])

    for y in range(0, max_y+2):
        s = ''
        for x in range(0, max_x+2):
            s += 'O' if (x,y) in visited else '#' if isWall((x,y),puzzleinput) else '.'
        print(s)

print()
print(get_unvisited_neighbors((1,1), set(), puzzleinput))
print()

distance = 50
visited = get_visited_points(startingpos, distance, puzzleinput)
dump_map(visited, puzzleinput)
print()
print('For a distance of ' + str(distance) + ' steps, ' + str(len(visited)) + ' locations are visiable')

