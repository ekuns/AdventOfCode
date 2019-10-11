import re

f = open("input09.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

routes = {}
for l in lines:
    m = re.match('^(\S+) to (\S+) = (\d+)$', l.strip())
    if m == None:
        continue

    l1, l2, dist = (m.group(1), m.group(2), int(m.group(3)))
    if not l1 in routes.keys(): routes[l1] = {}
    routes[l1][l2] = dist
    if not l2 in routes.keys(): routes[l2] = {}
    routes[l2][l1] = dist

cities = list(routes.keys())

#print(routes)
#print()
#print(cities)
#print()

paths = {}
for c in cities:
    newlist = list(cities)
    newlist.remove(c)
    paths[(c,)] = (newlist, 0)

#print('Paths;')
#print(paths)
#print()

def one_iterate(paths):
    new_paths = {}
    for key,r in paths.items():
        route = key
        remaining_cities = r[0]
        current_distance = r[1]
        #print('Route ' + str(route) + ' remaining = ' + str(remaining_cities) + ' ' + str(current_distance))
        for c in remaining_cities:
            newlist = list(remaining_cities)
            newlist.remove(c)
            new_paths[route + (c,)] = (newlist, current_distance + routes[route[-1]][c])
    return new_paths

while True:
    paths = one_iterate(paths)
    if len(paths[next(iter(paths))][0]) == 0:
        break

mindist = 9999999999
best_route = None
maxdist = 0
worst_route = None
for key,r in paths.items():
    route = key
    remaining_cities = r[0]
    current_distance = r[1]
    #print('Looking at ' + str(key) + ' ' + str(current_distance))
    if current_distance < mindist:
        mindist = current_distance
        best_route = key
    if current_distance > maxdist:
        maxdist = current_distance
        worst_route = key

# Part 1
print('Best route = ' + str(best_route))
print('Best distance = ' + str(mindist))

# Part 2
print()
print('Worst route = ' + str(worst_route))
print('Worst distance = ' + str(maxdist))
