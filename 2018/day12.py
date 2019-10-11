#!/usr/bin/python3

f = open("input12.txt", "r")
lines = f.readlines()
f.close()

generations = 500
beforeCount = 10
before = '.' * beforeCount
after = '.' * 10
state = list(before + lines[0][15:].strip() + after)

rules = {}
for l in lines:
    if not " => " in l:
        continue
    rules[l[0:5]] = l[9]

def stepForward(state):
    global beforeCount
    #print(''.join(state))
    next = state[:]
    for i in range(0, len(state)-5):
        next[i+2] = rules[''.join(state[i:i+5])]
    if ''.join(next[0:10]) == '..........':
        next = next[7:]
        beforeCount -= 7
    elif not ''.join(next[0:5]) == '.....':
        next.insert(0, '.')
        beforeCount += 1
    if ''.join(next[-5:]) == '.....':
        next = next[0:-2]
    else:
        next += ['.']
    return(next)

def getSum(state):
    sum = 0
    for i in range(0, len(state)):
        if state[i] == '#':
            sum += -beforeCount + i
    return sum

#########################

for gen in range(0, 20):
    state = stepForward(state)

print("Part 1")
print(getSum(state))
print("Ending offset after %d steps is %d" % ( 20, beforeCount ))

print()
print("part 2")
for gen in range(0, generations-20):
    state = stepForward(state)

start = getSum(state)
print(start)
print("Ending offset after %d steps is %d" % ( generations, beforeCount ))
#print(''.join(state))

state = stepForward(state)
delta = getSum(state) - start

print("Predicted score after 50000000000 generations:")
print((50000000000 - 500 - 1) * delta + getSum(state))

