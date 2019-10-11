f = open("input1.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

sum = 0
for x in lines:
    sum = sum + int(x)
print("Total sum of all entries: %s" % ( sum ) )

def findDupeSum(arr):
    sum = 0
    sumlist = []
    loopCount = 0
    while True:
        for x in lines:
            sum = sum + int(x)
            if sum in sumlist:
                print("First duplicate: %d after %d complete loops" % ( sum, loopCount ) )
                return
            sumlist = sumlist + [sum]
        loopCount = loopCount + 1


findDupeSum(lines)

