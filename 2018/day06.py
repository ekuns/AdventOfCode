f = open("input6.txt", "r")
lines = f.readlines()
f.close()

minx = 9999
maxx = 0
miny = 9999
maxy = 0
points = []
for l in lines:
    xy = [x.strip() for x in l.split(",")]
    x = int(xy[0])
    if (x > maxx):  maxx = x
    if (x < minx):  minx = x
    y = int(xy[1])
    if (y > maxy):  maxy = y
    if (y < miny):  miny = y
    points = points + [(x, y)]

print("We have %d points" % ( len(points) ))
print("x ranges from %d to %d" % (minx, maxx))
print("y ranges from %d to %d" % (miny, maxy))

counts = {}
infinite = {}
for p in points:
    counts[p] = 0
    infinite[p] = False

def distance(p, x, y):
    return abs(p[0] - x) + abs(p[1] - y)

def closest(x, y):
    mindist = 9999
    item = None
    for p in points:
        dist = distance(p, x, y)
        if dist < mindist:
            mindist = dist
            item = p
        elif dist == mindist:
            item = None
    return item

# Count how many points are closest to each labelled point
for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
        item = closest(x, y)
        if item != None:
            counts[item] += 1

# Find which points have infinite range away from minx or maxx
for x in range(minx - 1, maxx + 2):
    item = closest(x, miny)
    if item != None:
        infinite[item] = True
    item = closest(x, maxy)
    if item != None:
        infinite[item] = True

# Find which points have infinite range away from miny or maxy
for y in range(miny - 1, maxy + 2):
    item = closest(minx, y)
    if item != None:
        infinite[item] = True
    item = closest(maxx, y)
    if item != None:
        infinite[item] = True

maxcount = 0
maxitem = None
for p in points:
    if not infinite[p]:
        #print("Count for %s is %d" % ( p, counts[p] ))
        if counts[p] > maxcount:
            maxcount = counts[p]
            maxitem = p

print("The item with the biggest area around it is %s with %d squares" % ( maxitem, maxcount ))

maxrange = 10000
region = 0
maxdistance = 1 + int(maxrange / len(points))
for x in range(minx - maxdistance, maxx + maxdistance):
    for y in range(miny - maxdistance, maxy + maxdistance):
        if sum([distance(p, x, y) for p in points]) < maxrange:
            region += 1

print("The size of the region is %d squares" % ( region ))

