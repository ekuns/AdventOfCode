import re
from collections import defaultdict

f = open("input14.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

reindeer = {}
for l in lines:
    m = re.match('^(\S+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$', l.strip())
    if m == None:
        continue
    name, speed, flying, resting = (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    reindeer[name] = (speed, flying, resting, flying+resting)

race_time = 2503

def getdistance(name, time):
    speed, flying, resting, cycle = reindeer[name]
    totalcycles = time // cycle
    #print(name + ' flew for ' + str(totalcycles) + ' total cycles of ' + str(cycle) + ' seconds')

    remaining_time = time - totalcycles * cycle
    flyingtime = flying if remaining_time > flying else remaining_time
    #print('Total flying time is ' + str(flyingtime + totalcycles * cycle))

    distance = (totalcycles * flying + flyingtime) * speed
    return distance
 
def getwinner(time):
    names = list(reindeer.keys())
    maxdist = (0, None)
    for n in names:
        d = getdistance(n, time)
        if d > maxdist[0]:
            maxdist = (d, n)
    return maxdist

# Part 1

winner = getwinner(race_time)
print('The winner is ' + winner[1] + ' with a distance of ' + str(winner[0]) + ' km')

# Part 2

scores = defaultdict(int)
for time in range(1, race_time):
    winner = getwinner(time)
    scores[winner[1]] += 1

print(scores)

winner = max(scores, key=scores.get)
print('The winner is ' + winner + ' with ' + str(scores[winner]) + ' points')

