
f = open("input09.txt", "r")
line = f.read().strip()
f.close()

def decompress(line):
    output = ''
    offset = 0
    while True:
        off = line[offset:].find('(')
        if off == -1:
            output = output + line[offset:]
            break

        output = output + line[offset:offset+off]
        offset += off + 1

        offset_x = line[offset:].find('x')
        offset_close = line[offset:].find(')')
        length = int(line[offset:offset+offset_x])
        copies = int(line[offset+offset_x+1:offset+offset_close])
        offset += offset_close + 1

        output = output + line[offset:offset+length] * copies
        offset += length

    return output

def test(s, output):
    d = decompress(s)
    assert d == output, 'Wrong output: ' + d + ' != ' + output
    print(s + ' decompresses to ' + d + ' of length ' + str(len(d)))

test('ADVENT', 'ADVENT')
test('A(1x5)BC', 'ABBBBBC')
test('(3x3)XYZ', 'XYZXYZXYZ')
test('A(2x2)BCD(2x2)EFG', 'ABCBCDEFEFG')
test('(6x1)(1x3)A', '(1x3)A')
test('X(8x2)(3x3)ABCY', 'X(3x3)ABC(3x3)ABCY')
print()

# Part 1

d = decompress(line)
print('Part 1 length is ' + str(len(d)))
print()

# Part 2

def decompress2(line):
    total_length = 0

    output = ''
    while True:
        #print('Number of opening parentheses remaining: ' + str(line.count('(')))
        off = line.find('(')
        if off == -1:
            total_length += len(line)
            break
        total_length += off
        line = line[off+1:]
        #print(off)

        offset_x = line.find('x')
        offset_close = line.find(')')
        length = int(line[:offset_x])
        copies = int(line[offset_x+1:offset_close])
        line = line[offset_close+1:]

        line = line[:length] * copies + line[length:]
        #print(line)

    return total_length

def test2(s, expected_len):
    l = decompress2(s)
    assert l == expected_len, 'Wrong length: ' + str(l) + ' != ' + str(expected_len)
    print(s + ' decompresses to length ' + str(l))

test2('(3x3)XYZ', 9)
test2('X(8x2)(3x3)ABCY', 20)
test2('(27x12)(20x12)(13x14)(7x10)(1x12)A', 241920)
test2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', 445)

d = decompress2(line)
print('Part 2 length is ' + str(d))

