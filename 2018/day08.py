#!/usr/bin/python3

f = open("input08.txt", "r")
lines = f.readlines()
f.close()

numbers = list(map(int, lines[0].split()))

#print("List of numbers: %s" % (numbers))

nodenumber = 0

class Node:
    def __init__(self, numbers):
        global nodenumber
        self.node = nodenumber
        self.childCount, self.metadataCount = numbers[0:2]
        nodenumber += 1

        offset = 2
        self.children = []
        for i in range(0, self.childCount):
            child = Node(numbers[offset:])
            offset += child.consumed
            self.children += [child]

        self.metadata = numbers[offset:offset+self.metadataCount]
        self.consumed = offset + self.metadataCount

    def print(self):
        print("Node %d has %d children (%s) and %d metadata: %s" % (self.node, self.childCount,
                                                                    [c.node for c in self.children],
                                                                    self.metadataCount, self.metadata))
        for c in self.children:
            c.print()

    def sumMetadata(self):
        return sum(self.metadata) + sum([c.sumMetadata() for c in self.children])

    def value(self):
        return sum(self.metadata) if self.childCount == 0 else sum([self.children[i-1].value()
                                                                   for i in self.metadata if i-1 < len(self.children)])

root = Node(numbers)
#root.print()
print("There are %d nodes" % (nodenumber))
print("The sum of all metadata is %d" % (root.sumMetadata()))
print("The value of the root node is %d" % (root.value()))

