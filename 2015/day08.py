import re

f = open("input08.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

totalcharlit = 0
totalcharval = 0
totalskip = 0
for l in lines:
    l = l.strip()
    if len(l) == 0:
        continue

    o = ''
    skip = 0
    totalskip += 2 # Quotes
    for i in range(1, len(l)-1):
        if skip > 0:
            skip -= 1
            continue
        if l[i] == '\\':
            if l[i+1] == '\\':
                o += '\\'
                skip = 1
                totalskip += 1
            elif l[i+1] == '"':
                o += '"'
                skip = 1
                totalskip += 1
            elif l[i+1] == 'x':
                o += chr(int(l[i+2:i+4],16))
                skip = 3
                totalskip += 3
        else:
            o += l[i]
    totalcharlit += len(l)
    totalcharval += len(o)
    #print(l + '    ' + o)

print('Total chars of string literals: ' + str(totalcharlit))
print('Total chars of string values:   ' + str(totalcharval))
print('Difference: ' + str(totalcharlit - totalcharval))
print('Total Skipped: ' + str(totalskip))

# Part 2

added = 0
for l in lines:
    l = l.strip()
    if len(l) == 0:
        continue

    added += 2 + sum(map(l.count, '"\\'))


print('Part 2 difference = ' + str(added))

