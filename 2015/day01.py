f = open("input01.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

print('Final floor: ' + str(lines[0].count('(') - lines[0].count(')')))

floor = 0
index = 1
for x in lines[0]:
    if x == '(':
        floor += 1
    else:
        floor -= 1
    if floor < 0:
        print("Entered the basement at item: " + str(index))
        break
    index += 1


