
f = open("input16.txt", "r")
puzzleinput = f.read().strip()
f.close()

print('Puzzle input ' + puzzleinput)

def step(a):
    b = a[::-1]
    b = b.replace('0', '2')
    b = b.replace('1', '0')
    b = b.replace('2', '1')

    return a + '0' + b

def checksum(s):
    c = ''.join(['1' if s[i] == s[i+1] else '0' for i in range(0, len(s), 2)])
    return c if len(c) % 2 != 0 else checksum(c)

#print(step(puzzleinput))
def runProgram(data, length):
    while len(data) < length:
        data = step(data)

    if len(data) > length:
        data = data[0:length]
    return data

# Part 1

data = runProgram(puzzleinput, 272)
#print(data)
print('The checksum is: ' + checksum(data))

# Part 2

data = runProgram(puzzleinput, 35651584)
print('The checksum is: ' + checksum(data))

