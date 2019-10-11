import re

f = open("input25.txt", "r")
lines = f.readlines()
f.close()

m = re.match('^To continue, please consult the code grid in the manual.  Enter the code at row (\d+), column (\d+).$',
             lines[0].strip())
row, col = int(m.group(1)), int(m.group(2))

print("We're looking for row " + str(row) + ', column ' + str(col))
ntriangle = row + col - 1
print('This is close to the ' + str(ntriangle) + 'th triangle number')
back = ntriangle - col
print('But we are ' + str(back) + ' rows back')
number = ntriangle * (ntriangle + 1) // 2 - back
print('So we are looking for the ' + str(number) + 'th value')

code = 20151125
for i in range(0, number-1):
    code = (code * 252533) % 33554393

print('Part 1 - Final code is ' + str(code))

