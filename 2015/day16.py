import re
from collections import defaultdict

f = open("input16.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

list_of_sue = {}
for l in lines:
    m = re.match('^Sue (\d+): ([^:]+): (\d+), ([^:]+): (\d+), ([^:]+): (\d+)$', l.strip())
    if m == None:
        print('No match')
        continue
    index, item1, count1, item2, count2, item3, count3  = (m.group(1),
                                                           m.group(2), int(m.group(3)),
                                                           m.group(4), int(m.group(5)),
                                                           m.group(6), int(m.group(7)))
    list_of_sue[index] = {item1: count1, item2: count2, item3: count3}

#print(list_of_sue)

# Part 1

for index,sue in list_of_sue.items():
    if 'children' in sue and sue['children'] != 3: continue
    if 'cats' in sue and sue['cats'] != 7: continue
    if 'samoyeds' in sue and sue['samoyeds'] != 2: continue
    if 'pomeranians' in sue and sue['pomeranians'] != 3: continue
    if 'akitas' in sue and sue['akitas'] != 0: continue
    if 'vizslas' in sue and sue['vizslas'] != 0: continue
    if 'goldfish' in sue and sue['goldfish'] != 5: continue
    if 'trees' in sue and sue['trees'] != 3: continue
    if 'cars' in sue and sue['cars'] != 2: continue
    if 'perfumes' in sue and sue['perfumes'] != 1: continue
    print('Part 1 Aunt Sue index is ' + index)

# Part 2

for index,sue in list_of_sue.items():
    if 'children' in sue and sue['children'] != 3: continue
    if 'samoyeds' in sue and sue['samoyeds'] != 2: continue
    if 'akitas' in sue and sue['akitas'] != 0: continue
    if 'vizslas' in sue and sue['vizslas'] != 0: continue
    if 'cars' in sue and sue['cars'] != 2: continue
    if 'perfumes' in sue and sue['perfumes'] != 1: continue

    if 'cats' in sue and sue['cats'] <= 7: continue
    if 'trees' in sue and sue['trees'] <= 3: continue

    if 'pomeranians' in sue and sue['pomeranians'] >= 3: continue
    if 'goldfish' in sue and sue['goldfish'] >= 5: continue

    print('Part 2 Aunt Sue index is ' + index)

