import re
import itertools
from collections import defaultdict

f = open("input19.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

transforms = defaultdict(list)
transform = True
chemical = None
for l in lines:
    if transform:
        if len(l.strip()) == 0 and transform:
            transform = False
            continue
        m = re.match('^(\S+) => (\S+)$', l.strip())
        transforms[m.group(1)] += [m.group(2)]
    else:
        chemical = l.strip()
        break

print('Transforms: ' + str(transforms))
print()
print('Chemical: ' + chemical)

def all_possible_transforms(chem):
    newchemicals = []
    for key,trans in transforms.items():
        for t in trans:
            newchemicals += [chem[0:m.start()]+t+chem[m.end():] for m in re.finditer(key, chem)]
    return newchemicals

# Part 1

print()
print('The number of new chemicals is ' + str(len(set(all_possible_transforms(chemical)))))
print()

# Part 2

# Reverse the string
chem = chemical[::-1]

# Get all reversed patterns into a single dict:  transform: input
patterns = {t[::-1]: key[::-1] for key, trans in transforms.items() for t in trans}

# Turn all keys into a single search pattern
allpats = '(' + '|'.join(patterns.keys()) + ')'

count = 0
while chem != 'e':
    changed = False
    m = re.search(allpats, chem)
    if m == None:
        print('Not changed so giving up')
        break
    chem = chem.replace(m.group(), patterns[m.group()], 1)
    count += 1

print('It took this many replacements to get the desired string: ' + str(count))
print()
print('==================================')
print()

chem = chemical[::-1]

# Get all reversed patterns into a single dict:  transform: input
patterns = {t[::-1]: key[::-1] for key, trans in transforms.items() for t in trans}

# This function returns the replacement string based on what was matched
def repstr(x):
    return patterns[x.group()]

allpats = '|'.join(patterns.keys())

# Replace one pattern at a time until we're back to the starting string of 'e'
count = 0
while chem != 'e':
    chem = re.sub(allpats, repstr, chem, 1)
    count += 1

print('It took this many replacements to get the desired string: ' + str(count))

