import re

f = open("input21.txt", "r")
lines = f.read()
f.close()

m = re.match('^\s*Hit Points: (\d+)\s*Damage: (\d+)\s*Armor: (\d+)\s*$', lines)
boss_hp, boss_damage, boss_armor = int(m.group(1)), int(m.group(2)), int(m.group(3))

my_hp = 100
my_damage = 0
my_armor = 0

# Cost, Damage, Armor
weapons = {'Dagger': (8, 4, 0), 'Shortsword': (10, 5, 0), 'Warhammer': (25, 6, 0),
           'Longsword': (40, 7, 0), 'Greataxe': (74, 8, 0)}

armor = {'None': (0, 0, 0),
         'Leather': (13, 0, 1), 'Chainmail': (31, 0, 2), 'Splintmail': (53, 0, 3),
         'Bandedmail': (75, 0, 4), 'Platemail': (102, 0, 5)}

rings = {'None': (0, 0, 0),
         'Damage +1': (25, 1, 0), 'Damage +2': (50, 2, 0), 'Damage +3': (100, 3, 0),
         'Defense +1': (20, 0, 1), 'Defense +2': (40, 0, 2), 'Defense +3': (80, 0, 3)}

options = [(w, a, r1, r2,
            weapons[w][0]+armor[a][0]+rings[r1][0]+rings[r2][0],
            weapons[w][1]+armor[a][1]+rings[r1][1]+rings[r2][1],
            weapons[w][2]+armor[a][2]+rings[r1][2]+rings[r2][2])
           for w in weapons  for a in armor  for r1 in rings  for r2 in rings
           if (r1 == 'None' and r2 == 'None') or (r1 != 'None' and r1 != r2)]
options.sort(key = lambda x: x[4])

def battle():
    bhp = boss_hp
    mhp = my_hp
    rounds = 0
    my_attack = my_damage - boss_armor
    if my_attack <= 0:
        my_attack = 1
    boss_attack = boss_damage - my_armor
    if boss_attack <= 0:
        boss_attack = 1
    #print('My Stats:  hp ' + str(mhp) + ', attack ' + str(my_attack) + ', damage ' + str(my_damage) + ', armor ' + str(my_armor))
    #print('Boss Stats:  hp ' + str(bhp) + ', attack ' + str(boss_attack) + ', damage ' + str(boss_damage) + ', armor ' + str(boss_armor))
    #print('My attack = ' + str(my_attack) + ' and the boss attack is ' + str(boss_attack))
    while True:
        # Player attacks
        bhp -= my_attack
        #print('After my attack, my hit points are ' + str(mhp) + ' and boss hp are ' + str(bhp))
        if bhp <= 0:
            #print('Player wins after ' + str(rounds) + ' rounds spending ' + str(gold) + ' gold for ' + armoir)
            return (True, rounds)
        mhp -= boss_attack
        #print('After boss attack, my hit points are ' + str(mhp) + ' and boss hp are ' + str(bhp))
        if mhp <= 0:
            #print('Boss wins after ' + str(rounds) + ' rounds spending ' + str(gold) + ' gold for ' + armoir)
            return (False, rounds)
        rounds += 1

# Part 1

for o in options:
    armoir, gold, my_damage, my_armor = o[0] + ' ' + o[1] + ' ' + o[2] + ' ' + o[3], o[4], o[5], o[6]
    player_wins, rounds = battle()
    if player_wins:
        print('Part 1 - Player wins after ' + str(rounds) + ' spending ' + str(gold) + ' gold for ' + armoir)
        break

# Part 2

for o in options[::-1]:
    armoir, gold, my_damage, my_armor = o[0] + ' ' + o[1] + ' ' + o[2] + ' ' + o[3], o[4], o[5], o[6]
    player_wins, rounds = battle()
    if not player_wins:
        print('Part 2 - Player loses after ' + str(rounds) + ' spending ' + str(gold) + ' gold for ' + armoir)
        break

