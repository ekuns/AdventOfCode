import hashlib
from collections import deque

f = open("input14.txt", "r")
salt = f.read().strip()
f.close()

#salt = 'abc'
print('Salt is ' + salt)

def dohash(s):
    return(hashlib.md5(s.encode('utf-8')).hexdigest())

def dostretchedhash(s):
    h = hashlib.md5(s.encode('utf-8')).hexdigest()
    for i in range(0, 2016):
        h = hashlib.md5(h.encode('utf-8')).hexdigest()
    return h

def hasQuintuple(s, q):
    for x in q:
        if s in x:
            return True
    return False

def hasTriple(s):
    for i in range(0, len(s)-2):
        if s[i] == s[i+1] and s[i] == s[i+2]:
            return s[i]
    return None

def findlastindex(count, hashfunc):
    q = deque(maxlen=1000)
    for i in range(0, 1000):
        q.append(hashfunc(salt + str(i)))

    keycount = 0
    for i in range(0, 100000):
        x = q.popleft()
        q.append(hashfunc(salt + str(i+1000)))
        t = hasTriple(x)
        if t and hasQuintuple(t*5, q):
            keycount += 1
            #print('Found #' + str(keycount) + ' at ' + str(i))
            if keycount == count:
                print('Found the last one at index ' + str(i))
                return(i)

    return(-1)

# Part 1

findlastindex(64, dohash)

# Part 2

print()
findlastindex(64, dostretchedhash)

