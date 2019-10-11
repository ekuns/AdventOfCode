from itertools import chain, combinations, permutations
from collections import Counter
import pickle
import os.path
from functools import reduce

f = open("input24.txt", "r")
lines = f.readlines()
f.close()

packages = [int(l) for l in lines]
#packages = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
print(packages)

total = sum(packages)
print('Total weight of all packages = ' + str(total))
print('Weight goal for part 1: ' + str(total//3))
print()

# Get a list of all possible subsets of the provided list that sum up to 1/3 of the sum
# of the list.  Order doesn't matter.  We'll divide the list into p partitions, so we
# must always leave at least p-1 elements in the list unused to allow for other
# partitions.
def subsets(l, partitions):
    goal = sum(l) // partitions
    possibles = chain(*[combinations(l, i+1) for i in range(0, len(l)-partitions+1)])
    return [p for p in possibles if sum(p) == goal]

def find_solution(p):
    filename = 'test24-' + str(p) + '.obj'
    if not os.path.exists(filename):
        x = list(subsets(packages, p))
        f = open(filename, 'wb')
        pickle.dump(x, f)
        f.close()
    else:
        f = open(filename, 'rb')
        x = pickle.load(f)
        f.close()

    counters = Counter([len(i) for i in x])

    smallest = min(counters.keys())
    minqe = 999999999999999999999999999999
    minqeitem = None
    print('The smallest collection for ' + str(p) + ' partitions has ' + str(smallest) + ' packages')
    for i in x:
        if len(i) != smallest:
            continue
        qe = reduce((lambda x, y: x * y), i)
        if qe < minqe:
            minqe = qe
            minqeitem = i

    return minqe, minqeitem

# Part 1

minqe, minqeitem = find_solution(3)
print('Part 1 - Minimum QE = ' + str(minqe) + ' for ' + str(minqeitem))
print()

# Part 2

minqe, minqeitem = find_solution(4)
print('Part 2 - Minimum QE = ' + str(minqe) + ' for ' + str(minqeitem))

