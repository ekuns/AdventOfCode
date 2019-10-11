#!/usr/bin/python3

import sys

regex = None
#regex = '^WNE$' # 3
#regex = '^ENWWW(NEEE|SSE(EE|N))$' # 10
#regex = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$' # 18
#regex = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$' # 23
#regex = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$' # 31
#regex = '^WSSEESWWWNW(S|NENNESEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$' 

#regex = '^N((E|W)S|N|E|(W(S|)N))E$'
#regex = '^NE(W|SNEWS(NEWS|)NEWS)SNEW$'
#regex = '^WWWNENESEEESEEENNWNWS(SEWN|)WWNW(S|NNNWNNEES(W|EENNEESWSESESESSW(NW(S|WN(E|WN(E|WWSSE(N|S|E))))|SSESSEENEESWSSWNWWWN(WSSSSEESESWWSSWSSEEEEENEENWWNEEENENWNNESESSSSENNNESSEESSESSEEEESSEENWNNNNNESSEESSW(NWSNES|)SESENENNNW(NWNW(S|NWWWWNNESENESEEEESEESSW(WN(WNWESE|)E|SEEESSESSEESWSWWWSESWSWWWNENE(NNEE(NNWNWW(NEEWWS|)SES(WSW(WSS(ENEWSW|)WSWWNENWWSWSWWNENWNNE(SE(EEE(ESNW|)N|S)|NWWSWNWNNWNNWSWSSSSWSSSWNNNWWSWSWSWNWNENNWWS(E|WSESSSE(EEENENE(SSSW(SEESEEESWWSESWWSWNWWSESWSESENESEESWWSSENESSENESEESSWSSWSESESESENNENNNWSSW(WNNE(NNNNESENEESWSS(WWNEWSEE|)SSSSSWSSWWWNWNWWSWSWWSSENESSSSWWWNEN(ESNW|)WWNNWWSWWWNWNNEENEESENNESEES(ENENNWNNWNWSSESW(SEEWWN|)WNNNWWNWSWSSWNWSSWNNWWWSSWSEESWSSSESWWSEESWSSEEN(EENWNW(S|NNNE(SSESESSEENWNEEE(SWSESSEN(NN|EEEES(WWW|EENWNNESESSENNNESSES(EEENNESENEENNNNWNWNNWSSSWNW(NENNEENESSSENNNESSEENWNEEEENNNNWWWNNWNENWWNNENNWNWWSES(SSWSSE(SWWNW(SSEEESEN(NN|ESSWSWNWWN(E|WSW(N|SSSENNEES(EEENESEENWN(E|W)|W))))|NWWS(WWNNE(S|NENNNWSWNNWNNEEESS(WNWESE|)ESSEE(SS(ENSW|)WS(ESNW|)W(NNEWSS|)W|NNW)))))))))))))))))))))))))))))))))$'
#regex = '^WS(WE(S|NESS(WNSE|)EE(SS(ESW|)WS(ESNW|)W(NNSS|)W|NNW)))$'
#regex = '^E(S(E|W)W(E|S)W(N|S)W|N)$'
#regex = '^E(S(E|W)WW(N|S)W|N)$'
#regex = '^S(E(W|)(E|N)|W)$'

if not regex:
    f = open("input20.txt", "r")
    lines = f.readlines()
    f.close()

    lines = [l.rstrip('\r\n') for l in lines]
    regex = lines[0]

class Tree:

    nodeCount = 0

    def __init__(self, parent=None, asChild=True):
       self.value = ''
       self.parent = parent
       self.children = []
       self.following = None

       if parent is not None and asChild:
           parent.children.append(self)
       Tree.nodeCount += 1

    def append(self, value):
        if self.children:
            newnode = Tree(self, False)
            newnode.append(value)
            self.following = newnode
            return newnode
        else:
            self.value += value
            return self

    def __str__(self):
        retval = '^' if self.parent == None else ''
        retval += self.value
        if self.children:
            retval += "(" + '|'.join([str(c) for c in self.children]) + ")"
        if self.following:
            retval += str(self.following)
        if self.parent == None:
            retval += '$'
        return retval

    __repr__ = __str__

    def printNode(self, indent=0):
        print("%svalue = %s, %d children, text after = %s" % (' ' * indent, self.value, len(self.children),
                                                              self.following is not None))
        for n in self.children:
            n.printNode(indent+3)
        if self.following is not None:
            print("%sFollowing:" % (' ' * indent))
            self.following.printNode(indent)


rootNode = Tree()

def parseRegEx(regex):
    currentNode = rootNode
    prev = None
    for c in regex:
        if c in '^$':
            pass
        elif c in 'ESWN':
            currentNode = currentNode.append(c)
        elif c == '(':
            if prev == ')':
                newnode = Tree(currentNode, False)
                currentNode.following = newnode
                currentNode = newnode
            currentNode = Tree(currentNode)
        elif c == '|':
            n = currentNode
            while n.parent and n == n.parent.following:
                n = n.parent
            currentNode = Tree(n.parent)
        elif c == ')':
            n = currentNode
            while n.parent and n == n.parent.following:
                n = n.parent
            currentNode = n.parent
        else:
            print("Unexpected character: %s" % (c))
            break
        prev = c

parencount = regex.count('(')
if parencount > 500:
    sys.setrecursionlimit(regex.count('(') * 2)

parseRegEx(regex)

if str(rootNode) != regex:
    print("STRINGS ARE DIFFERENT AFTER PARSING")

print(regex)
print(rootNode)
#rootNode.printNode()
print("Total number of nodes = %d" % (Tree.nodeCount))

distance = 0
pos = (0,0)
rooms = {}

def followTree(n):
    global pos, distance, rooms

    for c in n.value:
        distance += 1
        if c == 'E':   pos = (pos[0]+1,pos[1])
        elif c == 'S': pos = (pos[0],pos[1]+1)
        elif c == 'N': pos = (pos[0],pos[1]-1)
        else:          pos = (pos[0]-1,pos[1])

        if pos in rooms and distance > rooms[pos]:
            distance = rooms[pos]
        else:
            rooms[pos] = distance

    start = pos
    dist = distance
    if n.children and len(n.children[-1].value) == 0:
        # If the last child is empty, short cut
        # Follow each child only to its end but not to end of regex
        for c in n.children:
            pos = start
            distance = dist
            followTree(c)
        # Then when done, pick up at the beginning and go to end of regex
        if n.following:
            pos = start
            distance = dist
            followTree(n.following)
    else:
        # Else folloe each dhild to the end of the regex
        for c in n.children:
            pos = start
            distance = dist
            followTree(c)
            if n.following:
                followTree(n.following)
        if not n.children:
            if n.following:
                followTree(n.following)

# Remove all options that have an empty last choice, as all of them are loops
def minimize(n):
    if n.children and len(n.children[-1].value) == 0:
        n.children = []
    for nn in n.children:
        minimize(nn)
    if n.following:
        minimize(n.following)

#minimize(rootNode)
#print(rootNode)
#rootNode.printNode()
followTree(rootNode)

print("There are %d rooms" % ( len(rooms) ))
#for k,v in rooms.items():
#    print("distance %s for room %s" % (v,k))

print("Furthest distance = %d" % ( max(rooms.values())))

def getLongest(n):
    l = len(n.value)
    if n.children:
        l += max([getLongest(c) for c in n.children])
    if n.following:
        l += getLongest(n.following)
    return l

print("Furthest distance = %d" % ( getLongest(rootNode) ))

# 7520 too low . 8186 too low
print("# rooms with distance > 0 = %d" % ( len([rooms[r] for r in rooms if rooms[r] > 0]) ))
print("# rooms with distance >= 1000 = %d" % ( len([rooms[r] for r in rooms if rooms[r] >= 1000]) ))

