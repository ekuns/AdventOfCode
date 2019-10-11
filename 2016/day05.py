import hashlib

f = open("input05.txt", "r")
lines = f.read()
f.close()

doorid = lines.strip()
print('Door ID is ' + doorid)

password1 = ''
for i in range(0, 100000000):
    h = hashlib.md5((doorid + str(i)).encode('utf-8')).hexdigest()
    if h.startswith('00000'):
        password1 += h[5:6]
        print('Password so far at i=' + str(i) + ' is ' + password1)
        if len(password1) == 8:
            break

print('Part 1 password = ' + password1)

print()
password2 = '________'
for i in range(0, 100000000):
    h = hashlib.md5((doorid + str(i)).encode('utf-8')).hexdigest()
    if h.startswith('00000'):
        offset = h[5:6]
        if offset >= '0' and offset <= '7':
            offset = int(offset)
            if password2[offset:offset+1] == '_':
                password2 = password2[0:offset] + h[6:7] + password2[offset+1:]
                print('Password so far at i=' + str(i) + ' is ' + password2)
                if not '_' in password2:
                    break

print('Part 2 password = ' + password2)
