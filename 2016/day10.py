import re
from collections import defaultdict

f = open("input10.txt", "r")
lines = f.readlines()
f.close()

bots = defaultdict(list)
highlow = {}
outputs = {}
for l in lines:
    if l.startswith('value '):
        m = re.match('^value (\d+) goes to bot (\d+)$', l.strip())
        bot, value = int(m.group(2)), int(m.group(1))
        bots[bot] += [value]
    elif l.startswith('bot '):
        m = re.match('^bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)$', l.strip())
        bot, whichlow, low, whichhigh, high = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4), int(m.group(5))
        highlow[bot] = (whichlow, low, whichhigh, high)
    else:
        raise Exception('Invalid line: ' + l)

foundit = False
def onepass():
    global foundit

    count = 0
    for bot, values in list(bots.items()):
        if len(values) == 2:
            #print('Found two values for ' + str(bot))
            del bots[bot]
            count += 1

            l, h = min(values), max(values)

            if l == 17 and h == 61:
                print('PART 1 - FOUND OUR BOT as ' + str(bot))
                #foundit = True

            whichlow, low, whichhigh, high = highlow[bot]

            if whichlow == 'bot':
                #print('For bot ' + str(low) + ' which is ' + str(bots[low]) + ' add ' + str(l))
                bots[low] += [l]
            else:
                outputs[low] = l

            if whichhigh == 'bot':
                #print('For bot ' + str(high) + ' which is ' + str(bots[high]) + ' add ' + str(h))
                bots[high] += [h]
            else:
                outputs[high] = h
    #print('Processed ' + str(count) + ' items')
    if count == 0:
        foundit = True


while not foundit:
    onepass()

print('Part 2 - ' + str(outputs[0] * outputs[1] * outputs[2]))

