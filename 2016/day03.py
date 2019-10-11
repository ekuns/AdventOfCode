import re

f = open("input03.txt", "r")
lines = f.readlines()
f.close()

possible = 0
impossible = 0
for l in lines:
    m = re.match('^\s*(\d+)\s+(\d+)\s+(\d+)\s*$', l.strip())
    s1, s2, s3 = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not (s1+s2 > s3 and s2+s3 > s1 and s1+s3 > s2):
        impossible += 1
    else:
        possible += 1

print('Part 1 ' + str(possible) + ' trinagles are possible and ' + str(impossible) + ' are impossible')

sides = []
for l in lines:
    m = re.match('^\s*(\d+)\s+(\d+)\s+(\d+)\s*$', l.strip())
    s1, s2, s3 = int(m.group(1)), int(m.group(2)), int(m.group(3))
    sides += [(s1, s2, s3)]

possible = 0
impossible = 0
for i in range(0, len(lines), 3):
    for j in range(0, 3):
        s1, s2, s3 = sides[i][j], sides[i+1][j], sides[i+2][j]
        if not (s1+s2 > s3 and s2+s3 > s1 and s1+s3 > s2):
            impossible += 1
        else:
            possible += 1

print('Part 2 ' + str(possible) + ' trinagles are possible and ' + str(impossible) + ' are impossible')
