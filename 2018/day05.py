f = open("input5.txt", "r")
lines = f.readlines()
f.close()

letters = list(lines[0].rstrip())

print('Number of lines: ' + str(len(lines)) + '; length of line is ' + str(len(letters)))

def collapse(letters):
    while True:
        changed = False
        l = letters
        i = 0
        length = len(letters) - 1
        while i < length:
            if l[i].lower() == l[i+1].lower() and ((l[i].isupper() and l[i+1].islower()) or
                                                   (l[i].islower() and l[i+1].isupper())):
                changed = True
                del l[i:i+2]
                length -= 2
            else:
                i = i + 1
        if not changed:
            break
        letters = l
    return letters

def removeAndCollapse(letters, letter):
    letters = [l for l in letters if l.lower() != letter.lower()]
    letters = collapse(letters)
    print(letter + ' - ' + str(len(letters)))

letters = collapse(letters)
#print("Final list: ")
#print(''.join(letters))
print('Final length: ' + str(len(letters)))

for l in list("abcdefghijklmnopqrstuvwxyz"):
    removeAndCollapse(letters, l)

