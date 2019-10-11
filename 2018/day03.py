import re

f = open("input3.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

maxx = 0
maxy = 0
claims = []
for x in lines:
    m = re.search('^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)\s*$', x)
    newclaim = (int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)))
    claims = claims + [newclaim]
    claim_maxx = newclaim[1] + newclaim[3]
    claim_maxy = newclaim[2] + newclaim[4]
    if (claim_maxx > maxx):
        maxx = claim_maxx
    if (claim_maxy > maxy):
        maxy = claim_maxy

print("Dimensions:  %dx%d" % ( maxx, maxy ))

counts = []
for i in range(0, maxx+1):
    counts.append([0] * (maxy+1))

for claim in claims:
    # Claim ID == claim[0]
    x = claim[1]
    y = claim[2]
    width = claim[3]
    height = claim[4]
    for xat in range(x, x+width):
        for yat in range(y, y+height):
            counts[xat][yat] = counts[xat][yat] + 1

shared = 0
private = 0
unused = 0
for x in range(0, maxx):
    for y in range(0, maxy):
        cnt = counts[x][y]
        if cnt == 0:
            unused = unused + 1
        elif cnt == 1:
            private = private + 1
        else:
            shared = shared + 1

print("Unused square inches:  %d" % ( unused ) )
print("Private square inches: %d" % ( private ) )
print("Shared square inches:  %d" % ( shared ) )
print("Total area:            %d" % ( unused + private + shared ) )

#for x in range(0, len(counts)):
#    for y in range(0, len(counts[x])):
#        print(counts[x][y], end=" ")
#    print()


for claim in claims:
    claimID = claim[0]
    x = claim[1]
    y = claim[2]
    width = claim[3]
    height = claim[4]
    overlapping = 0
    for xat in range(x, x+width):
        for yat in range(y, y+height):
            if counts[xat][yat] > 1:
                overlapping = overlapping + 1
                break
    if overlapping == 0:
        print("Claim %d does not overlap any other claims" % ( claimID ))

