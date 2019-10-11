import re

f = open("input15.txt", "r")
lines = f.readlines()
f.close()

slots = {}
for l in lines:
    m = re.match('^Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).$', l.strip())
    d, cnt, pos = int(m.group(1)), int(m.group(2)), int(m.group(3))
    print(str(d) + ' ' + str(cnt) + ' ' + str(pos))
    slots[d] = (cnt, pos)

print(slots)

def pressButton(t):
    #print(sum([1 for key,s in slots.items() if (s[1] + t + key) % s[0] == 0]) )
    if sum([1 for key,s in slots.items() if (s[1] + t + key) % s[0] == 0]) == len(slots):
        return True
    return False

def findFirst():
    for i in range(0, 10000000):
        if pressButton(i):
            print('Found it at ' + str(i))
            break

# Part 1
findFirst()

# Part 2
new = len(slots) + 1
slots[new] = (11, 0)

findFirst()

