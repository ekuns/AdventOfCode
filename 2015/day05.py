f = open("input05.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

nice = 0
for l in lines:
    l = l.strip().lower()
    if len(l) == 0: continue
    case1 = sum(map(l.count, 'aeiou')) >= 3
    case2 = any(l[i] == l[i+1] for i in range(len(l) - 1))
    case3 = sum(map(l.count, ['ab', 'cd', 'pq', 'xy'])) == 0
    if case1 and case2 and case3:
        nice += 1

print('Nice strings #1: ' + str(nice))

nice = 0
for l in lines:
    l = l.strip().lower()
    if len(l) == 0: continue
    case1 = any(l[i:i+2] in l[i+2:] for i in range(len(l) - 3))
    case2 = any(l[i] == l[i+2] for i in range(len(l) - 2))
    if case1 and case2:
        nice += 1

print('Nice strings #2: ' + str(nice))

