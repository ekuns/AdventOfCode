import re
from collections import defaultdict

f = open("input13.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

usermap = defaultdict(dict)
for l in lines:
    m = re.match('^(\S+) would (gain|lose) (\d+) happiness units by sitting next to ([^\.]+).$', l.strip())
    if m == None:
        continue
    name1, action, count, name2 = (m.group(1), m.group(2), int(m.group(3)), m.group(4))
    if action == 'lose':
        count = -count
    usermap[name1][name2] = count

users = list(usermap.keys())

def one_iteration(routes):
    new_routes = {}
    for path,remaining_users in routes.items():
        for u in remaining_users:
            new_routes[path + (u,)] = list(remaining_users)
            new_routes[path + (u,)].remove(u)
    return new_routes

def make_base_routes():
    routes = {}
    for u in users:
        routes[(u,)] = list(users)
        routes[(u,)].remove(u)
    return routes

def compute_happiness(path):
    score = 0
    usercount = len(users)
    for i in range(0,usercount):
        score += usermap[path[i]][path[(i-1+usercount) % usercount]]
        score += usermap[path[i]][path[(i+1) % usercount]]
    return score

def get_best_path():
    routes = make_base_routes()
    while True:
        routes = one_iteration(routes)
        if len(next(iter(routes))) == len(users):
            break

    bestpath = (0, None)
    for path,value in routes.items():
        routes[path] = compute_happiness(path)
        if routes[path] > bestpath[0]:
            bestpath = (routes[path], path)
    return bestpath

# Part 1
bestpath = get_best_path()
print('The best table arrangement is ' + str(bestpath[1]) + ' with happiness change ' + str(bestpath[0]))

# Part 2
for u in users:
    usermap[u]['Me'] = 0
for u in users:
    usermap['Me'][u] = 0

users = list(usermap.keys())

bestpath = get_best_path()
print('The best table arrangement with me is ' + str(bestpath[1]) + ' with happiness change ' + str(bestpath[0]))

