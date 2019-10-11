from collections import Counter

f = open("input06.txt", "r")
lines = f.readlines()
f.close()

message = ''
for i in range(0, 8):
    message += Counter(''.join([l[i:i+1] for l in lines])).most_common(1)[0][0]

print('Part 1 message = ' + message)

message = ''
for i in range(0, 8):
    c = Counter(''.join([l[i:i+1] for l in lines])).most_common()
    message += c[len(c)-1][0]

print('Part 2 message = ' + message)

