import re

f = open("input08.txt", "r")
lines = f.readlines()
f.close()

height = 6
width = 50
screen = ['.' * width for i in range(0, height)]

def printscreen():
    for s in screen:
        print(s)

def instruction(l):
    if l.startswith('rect'):
        m = re.match('^(\d+)x(\d+)', l[5:].strip())
        w, h = int(m.group(1)), int(m.group(2))
        for i in range(0, h):
            screen[i] = '#' * w + screen[i][w:]
    elif l.startswith('rotate row y='):
        m = re.match('^(\d+) by (\d+)$', l[13:].strip())
        row, dist = int(m.group(1)), int(m.group(2))
        screen[row] = screen[row][-dist:] + screen[row][0:width-dist]
    elif l.startswith('rotate column x='):
        m = re.match('^(\d+) by (\d+)$', l[16:].strip())
        col, dist = int(m.group(1)), int(m.group(2))
        slice_taken = [screen[(row - dist + height) % height][col:col+1] for row in range(0, height)]
        for row in range(0, height):
            screen[row] = screen[row][0:col] + slice_taken[row] + screen[row][col+1:]
    else:
        print('Bad instruction: ' + l)
        raise Exceptoin('Bad instruction ' + l)

def run_program():
    for l in lines:
        instruction(l.strip())

def count_pixels():
    sum = 0
    for row in range(0, height):
        sum += screen[row].count('#')
    return sum

run_program()
printscreen()
print('There are ' + str(count_pixels()) + ' pixels lit')

