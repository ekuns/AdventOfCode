import re

f = open("input07.txt", "r")
lines = f.readlines()
f.close()

def hasAbba(s):
    hypernet = False
    foundit = False
    for i in range(0, len(s)-3):
        c = s[i]
        if hypernet and c == ']':
            hypernet = False
            continue
        if not hypernet and c == '[':
            hypernet = True
            continue

        if c != s[i+1] and c == s[i+3] and s[i+1] == s[i+2]:
            if hypernet:
                return False
            foundit = True

    # No ABBA found anywhere means False
    return foundit

def hasSsl(s):
    hypernet = False
    for i in range(0, len(s)-2):
        c = s[i]
        if hypernet and c == ']':
            hypernet = False
            continue
        if not hypernet and c == '[':
            hypernet = True
            continue
        if not hypernet and c != s[i+1] and c == s[i+2]:
            m = s[i+1] + c + s[i+1]
            h = re.findall('\[[^\]]+', s)
            for hh in h:
                if m in hh:
                    return True
    return False

print(hasAbba('abba[mnop]qrst'))
print(hasAbba('abcd[bddb]xyyx'))
print(hasAbba('aaaa[qwer]tyui'))
print(hasAbba('ioxxoj[asdfgh]zxcvbn'))

count = 0
for l in lines:
    if hasAbba(l.strip()):
        count += 1

print('Count = ' + str(count))

count = 0
for l in lines:
    if hasSsl(l.strip()):
        count += 1

print('Count = ' + str(count))

