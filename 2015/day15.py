import re
from collections import defaultdict
from itertools import combinations_with_replacement

f = open("input15.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

ingredients = {}
for l in lines:
    m = re.match('^([^:]+): capacity ([-\d]+), durability ([-\d]+), flavor ([-\d]+), texture ([-\d]+), calories ([-\d]+)$', l.strip())
    if m == None:
        print('No match')
        continue
    name, capacity, durability, flavor, texture, calories = (m.group(1), int(m.group(2)), int(m.group(3)),
                                                             int(m.group(4)), int(m.group(5)), int(m.group(6)))
    ingredients[name] = (capacity, durability, flavor, texture, calories)


print(ingredients)

all_combos = list(combinations_with_replacement('ABCD', 100))
print(len(all_combos))

maxscore = 0
items = list(ingredients.keys())
for a in all_combos:
    As = a.count('A')
    Bs = a.count('B')
    Cs = a.count('C')
    Ds = a.count('D')

    capacity = 0
    durability = 0
    flavor = 0
    texture = 0

    if As > 0:
        capacity   += ingredients[items[0]][0] * As
        durability += ingredients[items[0]][1] * As
        flavor     += ingredients[items[0]][2] * As
        texture    += ingredients[items[0]][3] * As

    if Bs > 0:
        capacity   += ingredients[items[1]][0] * Bs
        durability += ingredients[items[1]][1] * Bs
        flavor     += ingredients[items[1]][2] * Bs
        texture    += ingredients[items[1]][3] * Bs

    if Cs > 0:
        capacity   += ingredients[items[2]][0] * Cs
        durability += ingredients[items[2]][1] * Cs
        flavor     += ingredients[items[2]][2] * Cs
        texture    += ingredients[items[2]][3] * Cs

    if Ds > 0:
        capacity   += ingredients[items[3]][0] * Ds
        durability += ingredients[items[3]][1] * Ds
        flavor     += ingredients[items[3]][2] * Ds
        texture    += ingredients[items[3]][3] * Ds

    if capacity   < 0: capacity   = 0
    if durability < 0: durability = 0
    if flavor     < 0: flavor     = 0
    if texture    < 0: texture    = 0

    score = capacity * durability * flavor * texture
    if score > maxscore:
        maxscore = score

print('Maxkimum score is ' + str(maxscore))

# Part 2

maxscore = 0
items = list(ingredients.keys())
for a in all_combos:
    As = a.count('A')
    Bs = a.count('B')
    Cs = a.count('C')
    Ds = a.count('D')

    capacity = 0
    durability = 0
    flavor = 0
    texture = 0
    calories = 0

    if As > 0:
        capacity   += ingredients[items[0]][0] * As
        durability += ingredients[items[0]][1] * As
        flavor     += ingredients[items[0]][2] * As
        texture    += ingredients[items[0]][3] * As
        calories   += ingredients[items[0]][4] * As

    if Bs > 0:
        capacity   += ingredients[items[1]][0] * Bs
        durability += ingredients[items[1]][1] * Bs
        flavor     += ingredients[items[1]][2] * Bs
        texture    += ingredients[items[1]][3] * Bs
        calories   += ingredients[items[1]][4] * Bs

    if Cs > 0:
        capacity   += ingredients[items[2]][0] * Cs
        durability += ingredients[items[2]][1] * Cs
        flavor     += ingredients[items[2]][2] * Cs
        texture    += ingredients[items[2]][3] * Cs
        calories   += ingredients[items[2]][4] * Cs

    if Ds > 0:
        capacity   += ingredients[items[3]][0] * Ds
        durability += ingredients[items[3]][1] * Ds
        flavor     += ingredients[items[3]][2] * Ds
        texture    += ingredients[items[3]][3] * Ds
        calories   += ingredients[items[3]][4] * Ds

    if calories != 500:
        continue

    if capacity   < 0: capacity   = 0
    if durability < 0: durability = 0
    if flavor     < 0: flavor     = 0
    if texture    < 0: texture    = 0

    score = capacity * durability * flavor * texture
    if score > maxscore:
        maxscore = score

print('Maxkimum score with 500 caliries is ' + str(maxscore))

