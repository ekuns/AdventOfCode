from collections import deque

f = open("input19.txt", "r")
puzzleinput = int(f.read().strip())
f.close()

print('Puzzle input ' + str(puzzleinput))

def run_game_1(length):
    elves = deque()
    for i in range(0, length):
        elves.append((i+1,1))

    while len(elves) > 1:
        elves[0] = (elves[0][0], elves[0][1] + elves[1][1])
        if elves[0][1] == length:
            print('Elf ' + str(elves[0][0]) + ' gets all game 1 presents when starting with ' + str(length) + ' elves')
            return
        elves.rotate(-1)
        elves.popleft()

run_game_1(5)

# Part 1

run_game_1(puzzleinput)

# Part 2

def run_game_2(length):
    elves1 = deque()
    elves2 = deque()
    for i in range(0, length):
        if i < length//2:
            elves1.append(i+1)
        else:
            elves2.append(i+1)

    # len(elves2) == len(elves1) or len(elves2) == len(elves1) + 1
    # We're donw when there is only one left in each list
    while True:
        if len(elves1) == 1 and len(elves2) == 1:
            break
        # Remove the elf stolen from
        elves2.popleft()
        # Rotate
        elves2.append(elves1.popleft())
        # Balance
        if len(elves2) > len(elves1) + 1:
            elves1.append(elves2.popleft())

    print('Elf ' + str(elves1[0]) + ' gets all game 2 presents when starting with ' + str(length) + ' elves')


run_game_2(5)

run_game_2(puzzleinput)

