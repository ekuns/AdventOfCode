f = open("input02.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

paper = 0
ribbon = 0
for line in lines:
    items = [int(i) for i in line.split('x') if 'x' in line]
    if len(items) < 3: break

    items.sort()
    l, w, h = items
    sides = (l*w, w*h, l*h)

    paper += sides[0]*2 + sides[1]*2 + sides[2]*2 + min(sides)
    ribbon += l*2 + w*2 + l*w*h

print('Total paper: ' + str(paper))
print('Total ribbon: ' + str(ribbon))

