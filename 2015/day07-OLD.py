import re

f = open("input07.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

chart = {}

def parse(line):
    line = line.strip()
    if (len(line) == 0): return
    m = re.match('^(\S+) (AND|OR|LSHIFT|RSHIFT) (\S+) -> (\S+)$', line)
    if m != None:
        v1,op,v2,v3 = (m.group(1), m.group(2), m.group(3), m.group(4))
        chart[v3] = (op, v1, v2)
    elif line.startswith('NOT '):
        m = re.match('^NOT (\S+) -> (\S+)$', line)
        if m != None:
            v1,v2 = (m.group(1), m.group(2))
            chart[v2] = ('NOT', v1)
        else:
            print('ERROR')
    else:
        m = re.match('^(\S+) -> (\S+)$', line)
        if m != None:
            print('found ' + line)
            v1,v2 = (m.group(1), m.group(2))
            chart[v2] = (v1)
        else:
            print('ERROR')

for l in lines:
    parse(l)

items = {}

# First assign all purely-numeric values
for key,value in list(chart.items()):
    if key == 'b':
        print('found line ' + value)
    if len(value) == 1 and value[0].isdigit():
        items[key] = int(value[0])
        print('assign value ' + value[0] + " to " + key)
        #del chart[key]
    elif len(value) == 2 and value[1].isdigit():
        items[key] = ~ int(value[1])
        print('assign value ' + str(~ int(value[1])) + " to " + key)
        #del chart[key]


    

