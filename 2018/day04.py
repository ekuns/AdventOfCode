import re

f = open("input4.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

guards = {}

state = 0
guardNum = 0
start = 0
stop = 0
for x in lines:
    m = re.search('^\[\d{4}-\d\d-\d\d \d\d:(\d\d)\] (Guard #(\d+) begins shift|falls asleep|wakes up)$', x)
    if "begins shift" in x:
        guardNum = m.group(3)
        if state != 0 and state != 1 and state != 3:
            print("Unexpected switch to beginning shift")
        state = 1
    elif "falls asleep" in x:
        start = int(m.group(1))
        if state != 1 and state != 3:
            print("Unexpected switch to falling asleep")
        state = 2
#        print("Guard %s Asleep" % ( guardNum ) )
    elif "wakes up" in x:
        stop = int(m.group(1))
        if state != 2:
            print("Unexpected switch to waking up")
        state = 3
#        print("Guard %s Awake, slept from %d - %d" % ( guardNum, start, stop ) )
        if not guardNum in guards:
            guards[guardNum] = [0] * 60
        asleepCount = guards[guardNum]
        for i in range(start, stop):
            asleepCount[i] = asleepCount[i] + 1

#for guardName, asleepCount in guards.items():
#    print(guardName, end=" - ")
#    for i in asleepCount:
#        print(i, end=" ")
#    print()

maxGuard = ''
maxGuardCount = -1
maxSleepTime = -1
for guardName, asleepCount in guards.items():
    minutesAsleep = sum(asleepCount)
    if minutesAsleep > maxGuardCount:
        maxGuardCount = minutesAsleep
        maxGuard = guardName
        maxSleepTime = asleepCount.index(max(asleepCount))

print("The guard who slept the most is %s at %d minutes" % (maxGuard, maxGuardCount))
print("The time most slept at is %d after the hour" % ( maxSleepTime ))
print("The guard slept this many times for %d minutes" % ( guards[maxGuard].count(guards[maxGuard][maxSleepTime]) ) )
print("ID times time = %d" % ( int(maxGuard) * maxSleepTime))

maxGuard = ''
maxAsleep = 0
maxSleepTime = -1
for guardName, asleepCount in guards.items():
    if max(asleepCount) > maxAsleep:
        maxAsleep = max(asleepCount)
        maxGuard = guardName
        maxSleepTime = asleepCount.index(maxAsleep)

print()
print("The guard who slept the most times in a minute was %s" % ( maxGuard ))
print("The minute most slept was %d for %d times" % ( maxSleepTime, maxAsleep ))
print("ID times time = %d" % ( int(maxGuard) * maxSleepTime))

