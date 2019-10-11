f = open("input03.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

santa = (0,0)
visited = {}
visited[santa] = 1  # Add the default first visit
for d in lines[0]:
    if d == '^':   santa = (santa[0], santa[1]-1)
    elif d == 'v': santa = (santa[0], santa[1]+1)
    elif d == '<': santa = (santa[0]-1, santa[1])
    elif d == '>': santa = (santa[0]+1, santa[1])

    if santa in visited.keys(): visited[santa] += 1
    else:                       visited[santa] = 1

print(len(visited))

santa = (0,0)
rsanta = (0,0)
visited = {}
visited[santa] = 2  # Add the default first two visits
counter = 0
for d in lines[0]:
    if counter % 2 == 0:
        if d == '^':   santa = (santa[0], santa[1]-1)
        elif d == 'v': santa = (santa[0], santa[1]+1)
        elif d == '<': santa = (santa[0]-1, santa[1])
        elif d == '>': santa = (santa[0]+1, santa[1])

        if santa in visited.keys(): visited[santa] += 1
        else:                       visited[santa] = 1
    else:
        if d == '^':   rsanta = (rsanta[0], rsanta[1]-1)
        elif d == 'v': rsanta = (rsanta[0], rsanta[1]+1)
        elif d == '<': rsanta = (rsanta[0]-1, rsanta[1])
        elif d == '>': rsanta = (rsanta[0]+1, rsanta[1])

        if rsanta in visited.keys(): visited[rsanta] += 1
        else:                        visited[rsanta] = 1
    counter += 1


print(len(visited))

