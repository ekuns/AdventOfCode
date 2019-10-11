#!/usr/bin/python3

import re
from queue import PriorityQueue

f = open("input23.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

points = {}
dist = {}
for l in lines:
    m = re.match('^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$', l)
    if m is None:
        print("No match for line %s" % ( l ))
        break
    p, r = (int(m.group(1)), int(m.group(2)), int(m.group(3))), int(m.group(4))
    points[p] = r
    dist[p] = ((p[0]-r, p[0]+r),  (p[1]-r, p[1]+r),  (p[2]-r, p[2]+r))

maxitem = max(points, key=points.get)
maxrange = points[maxitem]
#maxrange = max([points[p] for p in points])
print("maxitem = %s, maxrange = %d" % ( maxitem, maxrange ))

count = 0
for p,r in points.items():
    distance = abs(p[0]-maxitem[0]) + abs(p[1]-maxitem[1]) + abs(p[2]-maxitem[2])
    if distance <= maxrange:
        count += 1

print("Items in range: %d" % ( count ))

#### PART 2

scaleFactor = 20000000

xRange = (min([x[0] for x in points]), max([x[0] for x in points]))
yRange = (min([x[1] for x in points]), max([x[1] for x in points]))
zRange = (min([x[2] for x in points]), max([x[2] for x in points]))
print("x = %d to %d, y = %d to %d, z = %d to %d" % (xRange[0], xRange[1], yRange[0], yRange[1], zRange[0], zRange[1]))
print("Size of region: %d, %d, %d" % ( xRange[1]-xRange[0]+1, yRange[1]-yRange[0]+1, zRange[1]-zRange[0]+1))
print("Size of region: %d, %d, %d" % ( (xRange[1]-xRange[0]+1)/scaleFactor, (yRange[1]-yRange[0]+1)/scaleFactor, (zRange[1]-zRange[0]+1)/scaleFactor))

# Look to see how many points are within range of the cube defined by opposite
# corners: (p[0], p[1], p[2]) and (p[0]+scale, p[1]+scale, p[2]+scale)
def inRangeOf(p, scale):
    count = 0
    ccount = 0
    for pos,dst in dist.items():
        if not (p[0]+scale < dst[0][0] or p[0] > dst[0][1]) and \
           not (p[1]+scale < dst[1][0] or p[1] > dst[1][1]) and \
           not (p[2]+scale < dst[2][0] or p[2] > dst[2][1]):
            ccount += 1

        if p[0] > dst[0][0] and p[0] < dst[0][1] and \
           p[1] > dst[1][0] and p[1] < dst[1][1] and \
           p[2] > dst[2][0] and p[2] < dst[2][1]:
            count += 1
    return (count,ccount)

# Priority queue:  key = # points not in the region, value = x,y,z ranges plus scale of the cube
q = PriorityQueue()
q.put((0, abs(xRange[0])+abs(yRange[0])+abs(zRange[0]), (xRange, yRange, zRange), scaleFactor))

def scanOnce(qEntry):
    maxcount = 0
    within = []
    scannedCount = 0
    xRange,yRange,zRange,scale = qEntry[2][0],qEntry[2][1],qEntry[2][2],qEntry[3]
    for x in range(xRange[0], xRange[1]+1, scale):
        for y in range(yRange[0], yRange[1]+1, scale):
            for z in range(zRange[0], zRange[1]+1, scale):
               p = (x,y,z)
               scannedCount += 1
               count,ccount = inRangeOf(p, scale)
               newscale = scale // 10 if scale >= 10 else 1
               q.put((-count, abs(x)+abs(y)+abs(z), ((x,x+scale), (y,y+scale), (z,z+scale)), newscale))
               if count > maxcount:
                   maxcount = count
                   within = [p]
               elif count == maxcount:
                   within += [p]
    print("maxcount = %d of %d" % ( maxcount, len(points) ))
    print("len(Within) = %d of %d" % ( len(within), scannedCount ))
    if len(within) < 5: print("Within = %s - %s" % ( within, (within[0][0]+scale,within[0][1]+scale,within[0][2]+scale) ))
    print("len(q) = %d" % ( q.qsize()))

# Not 51513730 and not 39471676
# Probably 51429372
# probably best location: (18966929, 18036278, 14426165)
# probably bots in range: 976

for i in range(0, 40):
    nxt = q.get()
    print(nxt)
    scanOnce(nxt)

print(q.get())
print(q.get())
print(q.get())
print(q.get())
