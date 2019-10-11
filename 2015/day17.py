import itertools

f = open("input17.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

containers = [int(l) for l in lines]

combinations = []
min_combinations = None
for i in range(1, len(containers)):
    newcombos = [x for x in itertools.combinations(containers, i) if sum(x) == 150]
    combinations += newcombos
    if min_combinations == None and len(newcombos) > 0:
        print('The shortest length is ' + str(i))
        min_combinations = newcombos

print('There are ' + str(len(combinations)) + ' combinations')
print('There are ' + str(len(min_combinations)) + ' combinations of shortest length')

