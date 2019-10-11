import hashlib

f = open("input04.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

base = lines[0].strip()
#base = 'abcdef'
#base = 'pqrstuv'

stop = False
for i in range(0, 100000000):
    d = hashlib.md5((base + str(i)).encode('utf-8')).hexdigest()
    if not stop and d.startswith('00000'):
        print(str(i) + ' - results in 5-zero hash ' + d + ' for ' + base + str(i))
        stop = True

    if d.startswith('000000'):
        print(str(i) + ' - results in 6-zero hash ' + d + ' for ' + base + str(i))
        break

