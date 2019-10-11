import re
from collections import Counter
from itertools import groupby
from operator import itemgetter

f = open("input04.txt", "r")
lines = f.readlines()
f.close()

sectorSum = 0

def decrypt(s, count):
    a = ord('a')
    return ''.join([chr((ord(c)-a+count) % 26 + a) if c.isalpha() else ' ' for c in s])

rooms = {}
for l in lines:
    m = re.match('^([-a-z]+)-(\d+)\[([a-z]+)\]$', l.strip())
    enc_name, sectorID, checksum = m.group(1).replace('-', ''), int(m.group(2)), m.group(3)

    # Get a sorted list of (letter, count), descending by count
    c = [(x,y) for x,y in Counter(enc_name).most_common()]

    # Collect into a list of lists where each list has letters with the same frequency (frequency sorted list)
    fsl = [[x for x,y in g] for k,g in groupby(c, itemgetter(1))]
    full_checksum = ''.join([''.join(sorted(i)) for i in fsl])

    if full_checksum.startswith(checksum):
        sectorSum += sectorID
        decrypted = decrypt(m.group(1), sectorID)
        rooms[decrypted] = sectorID

north_pole_objects = None
for k in rooms.keys():
    if 'north' in k and 'pole' in k:
        north_pole_objects = k

print('Part 1 - Sector ID sum of good rooms = ' + str(sectorSum))
print('Part 2 - Sector ID of "' + north_pole_objects + '" = ' + str(rooms[north_pole_objects]))

