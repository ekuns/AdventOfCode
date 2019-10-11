
f = open("input20.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

target = int(lines[0])
print('Target = ' + str(target))

# It turns out countgifts and the search using it is too slow...

def countgifts(n):
    gifts = 0
    for j in range(1,n+1):
        if n % j == 0:
            gifts += j
    return gifts * 10

def getrange():
    # https://oeis.org/A002182
    numberlist = [ 50400, 55440, 83160, 110880, 166320, 221760, 277200, 332640, 498960,
                   554400, 665280, 720720, 1081080, 1441440, 2162160  ]
    last = 0
    stopat = 0
    for n in numberlist:
        gifts = countgifts(n)
        print('The number of gifts for ' + str(n) + ' is ' + str(gifts))
        if gifts < target:
            last = n
        elif stopat == 0:
            stopat = n

    print('Look between ' + str(last) + ' and ' + str(stopat))
    print()
    return (last, stopat)

def look_in_range(start,stop,skip):
    maxfound = 0
    maxfoundat = 0
    for i in range(last+2, stopat, 2):
        if i % 10000 == 0:
            print('Max seen up to ' + str(i) + ' is ' + str(maxfound) + ' at ' + str(maxfoundat))
        gifts = countgifts(i)
        if gifts > maxfound:
            maxfound = gifts
            maxfoundat = i
        if gifts >= target:
            print('Found it at ' + str(i))
            return maxfound, maxfoundat

#last, stopat = getrange()
#look_in_range(1240000, 1240000+10000, 1)
#maxfound, maxfoundat = look_in_range(last+2, stopat, 2)
#
#print('Max found is ' + str(maxfound) + ' at ' + str(maxfoundat))

def sieve(target):
    # Make a huge array for the sieve ... initialize for having elf #1 visit every house
    target //= 10
    giftcount = [10] * target
    for i in range(2, target):
        toadd = i * 10
        for j in range(i, target, i):
            giftcount[j] += toadd
    return giftcount

arr = sieve(target)
index = next(x for x, val in enumerate(arr) if val >= target)
print('Part 1 - The first house found is ' + str(index) + ' with ' + str(arr[index]) + ' gifts')

# Part 2

def sieve2(target):
    target //= 11
    giftcount = [0] * target
    for i in range(1, target):
        toadd = i * 11
        for j in range(i, min(i*50+1, target), i):
            giftcount[j] += toadd
    return giftcount

arr = sieve2(target)
index = next(x for x, val in enumerate(arr) if val >= target)
print('Part 2 - The first house found is ' + str(index) + ' with ' + str(arr[index]) + ' gifts')

