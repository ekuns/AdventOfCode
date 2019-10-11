from itertools import groupby

f = open("input10.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

value = lines[0].strip()

print('Starting value is ' + value)

def look_and_say(value):
    groups = groupby(value)
    result = [(label, sum(1 for _ in group)) for label, group in groups]
    return("".join('{}{}'.format(count, label) for label, count in result))

itercount = 40
for i in range(0,itercount):
    value = look_and_say(value)

print('After ' + str(itercount) + ' iterations, the length is ' + str(len(value)))

moreiters = 10
for i in range(0,moreiters):
    value = look_and_say(value)


print('After ' + str(itercount + moreiters) + ' iterations, the length is ' + str(len(value)))

