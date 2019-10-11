
f = open("input18.txt", "r")
puzzleinput = f.read().strip()
f.close()

print('Puzzle input ' + puzzleinput)


def isTrap(line, pos):
    l = '^' == (line[pos-1] if pos > 0 else '.')
    c = '^' ==  line[pos]
    r = '^' == (line[pos+1] if pos < len(line)-1 else '.')

    return l ^ r
    #return (l and not r) or (r and not l)
    #return (l and c and not r) or (c and r and not l) or (l and not r and not c) or (r and not l and not c)

def newline(line):
    return ''.join(['^' if isTrap(line, i) else '.' for i in range(0, len(line))])

def safe_tile_count(firstline, rows, printit=False):
    count = firstline.count('.')

    line = firstline
    if printit: print(line)
    for i in range(0, rows-1):
        line = newline(line)
        if printit: print(line)
        count += line.count('.')

    return count

print(safe_tile_count('..^^.', 2, True))
print()

print(safe_tile_count('.^^.^.^^^^', 10, True))
print('Above should be 38')
print()

# Part 1

print('Part 1 has ' + str(safe_tile_count(puzzleinput, 40, True)) + ' safe tiles')

# Part 2

print('Part 2 has ' + str(safe_tile_count(puzzleinput, 400000, False)) + ' safe tiles')
