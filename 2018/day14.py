#!/usr/bin/python3

length = 0

class Node:
    def __init__(self, score, previous=None):
        global length
        length += 1
        self.score = score
        self.next = None
        if previous:
            previous.next = self

recipes = Node(3)
elf1 = recipes
elf2 = Node(7, elf1)
tail = elf2

def mix():
    global tail, elf1, elf2
    new = elf1.score + elf2.score
    if new >= 10:
        tail = Node(new // 10, tail)
    tail = Node(new % 10, tail)
    # Step elf1 forward
    for i in range(0, elf1.score + 1):
        elf1 = elf1.next
        if elf1 == None:  elf1 = recipes
    # Step elf2 forward
    for i in range(0, elf2.score + 1):
        elf2 = elf2.next
        if elf2 == None:  elf2 = recipes

def dumpList():
    global recipes, elf1, elf2
    n = recipes
    while n != None:
        if n == elf1:
            print("(" + str(n.score) + ")", end=" ")
        elif n == elf2:
            print("[" + str(n.score) + "]", end=" ")
        else:
            print(n.score, end=" ")
        n = n.next
    print()

def dumpLastN(count):
    global recipes
    n = recipes
    pos = length
    ret = ""
    while n != None:
        pos -= 1
        if pos < count:
            ret += str(n.score)
        n = n.next
    return ret

# PART 1

#input = 5
#input = 9
#input = 2018
input = 190221

#dumpList()
while length < input+10:
    mix()
    #dumpList()
print(dumpLastN(10))

# Part 2 - Linked List was vastly too slow, and normal list is far faster

#input = '51589' # 9
#input = '01245' # 5
#input = '92510' # 18
#input = '59414' # 2018
#input = '22159414' # My own test  ... 2015
input = '190221' # ???

recipes = [3, 7]
e1 = 0
e2 = 1

def mix2():
    global recipes, e1, e2
    new = recipes[e1] + recipes[e2]
    if new >= 10:
        recipes += [new // 10]
    recipes += [new % 10]
    e1 = (e1 + recipes[e1] + 1) % len(recipes)
    e2 = (e2 + recipes[e2] + 1) % len(recipes)

def dumpList2():
    global recipes, e1, e2
    for i in range(0, len(recipes)):
        if i == e1:
            print("(" + str(recipes[i]) + ")", end=" ")
        elif i == e2:
            print("[" + str(recipes[i]) + "]", end=" ")
        else:
            print(recipes[i], end=" ")
    print()

# Gotta be careful in our while ... could have added 1 or 2 digits on the previous mix round
strlen = len(input)
#dumpList2()
while input not in ''.join(map(str,recipes[-strlen-1:])):
    mix2()
    #dumpList2()

print(len(recipes) + ''.join(map(str,recipes[-strlen-1:])).index(input) - strlen - 1)

