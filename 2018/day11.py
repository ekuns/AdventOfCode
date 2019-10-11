#!/usr/bin/python3

puzzleInput = 1788

def getPower(x, y, gridSerialNumber):
    rackId = x + 10
    power = (rackId * y + gridSerialNumber) * rackId
    power = (int(power / 100) % 10) - 5
    return power

def computeGrid(gridSerialNumber):
    grid = [[0 for _ in range(301)] for _ in range(301)]
    for x in range(0, 301):
        for y in range(0, 301):
            grid[x][y] = getPower(x, y, gridSerialNumber)
    return grid

def get3x3MaxPower(gridSerialNumber):
    return getDxDyMaxPower(gridSerialNumber, 3)

def getDxDyMaxPower(gridSerialNumber, maxDxDy, grid=None):
    if grid == None:
        grid = computeGrid(gridSerialNumber)
    maxPower = -9999
    maxLocation = (0, 0)
    for x in range(1, 300 - maxDxDy + 1):
        for y in range(1, 300 - maxDxDy + 1):
            totalPower = 0
            for dx in range(0, maxDxDy):
                for dy in range(0, maxDxDy):
                    totalPower += grid[x+dx][y+dy]
            if totalPower > maxPower:
                maxPower = totalPower
                maxLocation = (x, y)
    return (maxPower, maxLocation, maxDxDy)

def getMaxPower(gridSerialNumber):
    grid = computeGrid(gridSerialNumber)
    maxPower = (0, (0, 0), 0)
    for dx in range(1, 30):
        mp = getDxDyMaxPower(gridSerialNumber, dx, grid)
        if mp[0] > maxPower[0]:
            maxPower = mp
    return maxPower

print("TESTS")
print("=== Power Calculation ===")
print("Expect power =  4 - %s" % ( getPower(3, 5, 8) ))
print("Expect power = -5 - %s" % ( getPower(122, 79, 57) ))
print("Expect power =  0 - %s" % ( getPower(217, 196, 39) ))
print("Expect power =  4 - %s" % ( getPower(101, 153, 71) ))

print("=== 3x3 Max Power Calculation ===")
print("Expect to find power 29, location 33,45 - power %s, location %s, size %s" % ( get3x3MaxPower(18) ))
print("Expect to find power 30, location 21,61 - power %s, location %s, size %s" % ( get3x3MaxPower(42) ))

print()
print("==========================================")
print("Part 1 - 3x3 max power & location for puzzle input %d" % ( puzzleInput ))
print(get3x3MaxPower(puzzleInput))

print()
print("TESTS")
print("Expect to find power 113, location  90,269, size 16x16 - power %s, location %s, size %s" % ( getMaxPower(18) ))
print("Expect to find power 119, location 232,251, size 12x12 - power %s, location %s, size %s" % ( getMaxPower(42) ))
print("Part 2 - max power, location, dx/dy for puzzle input %d" % ( puzzleInput ))
print(getMaxPower(puzzleInput))

