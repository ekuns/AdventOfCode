#!/usr/bin/python3

import re
import copy

f = open("input07.txt", "r")
lines = f.readlines()
f.close()

#maxworkers = 2
#extrawork = 0

maxworkers = 5
extrawork = 60

allsteps = []
dependencies = {}
for l in lines:
    m = re.search('Step (.) must be finished before step (.) can begin.', l)
    first = m.group(1)
    last = m.group(2)

    if first not in allsteps:
        allsteps += [first]
    if last not in allsteps:
        allsteps += [last]

    if last in dependencies:
        dependencies[last] += [first]
    else:
        dependencies[last] = [first]

allsteps = sorted(allsteps)

dd = copy.deepcopy(dependencies)

allStepCounts = {}
for a in allsteps:
    allStepCounts[a] = ord(a.lower()) - ord('a') + 1 + extrawork

print("The list contains steps: %s" % ( allsteps ))
for k,v in dependencies.items():
    print("%s: %s" % (k, v))

stepOrder = []
while len(allsteps) > 0:
    nextsteps = sorted([s for s in allsteps if s not in dependencies])

    nextStep = nextsteps[0]
    stepOrder += [nextStep]
    toremove = []
    for k,v in dependencies.items():
        if nextStep in v:
            v.remove(nextStep)
            if len(v) == 0:
                toremove += [k]
    for k in toremove:
        del dependencies[k]
    allsteps.remove(nextStep)


print("The correct order is: %s" % ( stepOrder ))
print("Short form: %s" % ( ''.join(stepOrder) ))

dependencies = dd
stepOrder = []
workers = [None] * maxworkers

time = 0
while len(allStepCounts) > 0:
    nextsteps = sorted([s for s in allStepCounts.keys() if s not in dependencies])

    # Assign work to any idle workers, if any is available
    xx = 0
    for i in range(0, maxworkers):
        if workers[i] != None: continue

        # We found an idle worker -- look for work for this worker
        while (nextsteps[xx] in workers):
            xx += 1
            if xx >= len(nextsteps): break
        if xx >= len(nextsteps): break
        workers[i] = nextsteps[xx]
        xx += 1
        if xx >= len(nextsteps): break

    #print("%s" % ( [s + str(allStepCounts[s]) for s in workers if s in allStepCounts]))

    # Figure out how many units of time we can safely step forward
    maxWork = 9999999
    for i in range(0, maxworkers):
        if workers[i] != None and allStepCounts[workers[i]] < maxWork:
            maxWork = allStepCounts[workers[i]]

    # Work the workers the minimum safe unit of time.  Remove completed work from workers.
    # This frees up those workers to take new work if any is available.
    time += maxWork
    for i in range(0, maxworkers):
        s = workers[i]
        if s == None:
            continue
        allStepCounts[s] -= maxWork
        if (allStepCounts[s] == 0):
            workers[i] = None
            stepOrder += [s]
            toremove = []
            for k,v in dependencies.items():
                if s in v:
                    v.remove(s)
                    if len(v) == 0:
                        toremove += [k]
            for k in toremove:
                del dependencies[k]
            del allStepCounts[s]

print("The correct order is: %s" % ( stepOrder ))
print("Short form: %s" % ( ''.join(stepOrder) ))
print("Total time taken is %d seconds" % (time))

