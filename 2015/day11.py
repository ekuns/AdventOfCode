from itertools import groupby

f = open("input11.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

value = lines[0].strip()

def isvalid(pw):
    test1 = len(pw) == 8
    test2 = any([ord(pw[i])+1 == ord(pw[i+1]) and ord(pw[i+1])+1 == ord(pw[i+2]) for i in range(0,6)])
    test3 = any([ord(pw[i]) == ord(pw[i+1]) and ord(pw[j]) == ord(pw[j+1]) and ord(pw[i]) != ord(pw[j])
                for i in range(0,5) for j in range(i+2,7)])
    test4 = not('i' in pw or 'o' in pw or 'l' in pw)
    return test1 and test2 and test3 and test4

def increment(value):
    pw = list(value)
    offset = 7
    while offset >= 0:
        if pw[offset] != 'z':
            increment = 1 if pw[offset] not in 'hnk' else 2
            pw[offset] = chr(ord(pw[offset])+increment)
            return ''.join(pw)
        else:
            pw[offset] = 'a'
            offset -= 1
    return ''.join(pw)

def findnext(value):
    x = increment(value)
    while not isvalid(x):
        x = increment(x)
    return x

print('abcdffaa is valid ' + str(isvalid('abcdffaa')))
print('ghjaabcc is valid ' + str(isvalid('ghjaabcc')))

print('Starting value is ' + value)
print('Starting password is valid: ' + str(isvalid(value)))

print('Next valid value after abcdefgh is ' + findnext('abcdefgh'))
print('Next valid value after ghijklmn is ' + findnext('ghijklmn'))

# Part 1
nextvalue = findnext(value)
print('Next valid value after ' + value + ' is ' + nextvalue)
# Part 2
print('Next valid value after ' + nextvalue + ' is ' + findnext(nextvalue))

