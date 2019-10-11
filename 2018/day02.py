f = open("input2.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

twoLetters = 0
threeLetters = 0
for x in lines:
    for two in list("abcdefghijklmnopqrstuvwxyz"):
        if x.count(two) == 2:
            twoLetters = twoLetters + 1
            break

    for two in list("abcdefghijklmnopqrstuvwxyz"):
        if x.count(two) == 3:
            threeLetters = threeLetters + 1
            break

print("Words with identical letters:\n  2 - %d\n  3 - %d" % ( twoLetters, threeLetters) )
print("Checksum: %d" % ( twoLetters * threeLetters ) )

max1 = -1
max2 = -1
max = -1
index = 0
for x in range(0, len(lines)-1):
    letters1 = list(lines[x].rstrip())
    for y in range(x+1, len(lines)-1):
        letters2 = list(lines[y].rstrip())
        count = 0
        for z in range(0, len(letters1)-1):
            if letters1[z] == letters2[z]:    
                count = count + 1
        if count > max:
            print("New Max %d found at pos %d,%d, %s,%s" % (count, x, y, lines[x].rstrip(), lines[y].rstrip()))
            max = count
            max1 = x
            max2 = y

