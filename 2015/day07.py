import re

f = open("input07.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

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
            v1,v2 = (m.group(1), m.group(2))
            chart[v2] = (v1,)
        else:
            print('ERROR')

# First assign all purely-numeric values
def init():
    for key,value in list(chart.items()):
        if len(value) == 1 and value[0].isdigit():
            items[key] = int(value[0])
            del chart[key]
        elif len(value) == 2 and value[1].isdigit():
            items[key] = ~ int(value[1])
            del chart[key]

def oneLoop():
    ret = False
    for key,value in list(chart.items()):
        if len(value) == 1 and value[0] in items:
            items[key] = items[value[0]]
            del chart[key]
            ret = True
        elif len(value) == 2 and value[1] in items:
            items[key] = ~ items[value[1]]
            del chart[key]
            ret = True
        elif len(value) == 3:
            op = value[0]
            v1 = value[1]
            v2 = value[2]
            if v1.isdigit() and v2 in items:
                v1 = int(v1)
                v2 = items[v2]
                if op == 'AND': items[key] = v1 & v2
                elif op == 'OR': items[key] = v1 | v2
                elif op == 'LSHIFT': items[key] = v1 << v2
                elif op == 'RSHIFT': items[key] = v1 >> v2
                del chart[key]
                ret = True
            elif v1 in items and v2.isdigit():
                v1 = items[v1]
                v2 = int(v2)
                if op == 'AND': items[key] = v1 & v2
                elif op == 'OR': items[key] = v1 | v2
                elif op == 'LSHIFT': items[key] = v1 << v2
                elif op == 'RSHIFT': items[key] = v1 >> v2
                del chart[key]
                ret = True
            elif v1 in items and v2 in items:
                v1 = items[v1]
                v2 = items[v2]
                if op == 'AND': items[key] = v1 & v2
                elif op == 'OR': items[key] = v1 | v2
                elif op == 'LSHIFT': items[key] = v1 << v2
                elif op == 'RSHIFT': items[key] = v1 >> v2
                del chart[key]
                ret = True
    return ret

# Part 1

chart = {}
for l in lines:
    parse(l)

items = {}
init()
while oneLoop():
    pass

#for key in sorted(items.keys()):
#    print(key + ' = ' + str(items[key]))

a = items['a']
print('Value of a is ' + str(a))

# Part 2

chart = {}
for l in lines:
    parse(l)

items = {}
init()
items['b'] = a    # Here's the part 2 override
while oneLoop():
    pass

#for key in sorted(items.keys()):
#    print(key + ' = ' + str(items[key]))

a = items['a']
print('Value of a is ' + str(a))

