import re

f = open("input22.txt", "r")
lines = f.read()
f.close()

m = re.match('^\s*Hit Points: (\d+)\s*Damage: (\d+)\s*$', lines)
boss_hp, boss_damage = int(m.group(1)), int(m.group(2))

my_hp = 50
my_mana = 500
my_armor = 0
my_damage = 0

boss, me = (boss_hp, boss_damage), (my_hp, my_damage, my_armor, my_mana)

# Cost, Instant Damage, Instant Heal, Rounds, Effect Size, Name
spells = {'M': (53,  4, 0,  0,    0, 'Magic Missile'),
          'D': (73,  2, 2,  0,    0, 'Drain'),
          'S': (113, 0, 0,  6,    7, 'Shield'),
          'P': (173, 0, 0,  6,    3, 'Poison'),
          'R': (229, 0, 0,  5,  101, 'Recharge')}
minSpellCost = min([spells[spl][0] for spl in 'MDSPR'])

activespells = {}

print('Initial Stats:')
print('My HP ' + str(my_hp) + ', damage ' + str(my_damage) + ', mana ' + str(my_mana))
print('Boss HP ' + str(boss_hp) + ', damage ' + str(boss_damage))

def make_active(spell):
    activespells[spell] = spells[spell][3]

def handleActiveSpells(debug=False):
    global my_hp, boss_hp, my_mana, my_armor
    for s,timer in dict(activespells).items():
        timer -= 1
        activespells[s] = timer
        if s == 'S':
            if debug: print("Shield's timer is now " + str(timer))
        elif s == 'P':
            if debug: print('Poison deals ' + str(spells['P'][4]) + ' damage; its timer is now ' + str(timer) + '.')
            boss_hp -= spells['P'][4]
        elif s == 'R':
            if debug: print('Recharge provides ' + str(spells['R'][4]) + ' mana; its timer is now ' + str(timer) + '.')
            my_mana += spells['R'][4]
        else:
            print('************ Bad spell ***********')

        if timer == 0:
            if s == 'S':
                if debug: print('Shield wears off, decreasing armor by 7.')
                my_armor -= spells['S'][4]
            else:
                if debug: print(s + ' wears off')
            del activespells[s]

def turn(spell, debug=False, autoDamage=False):
    global my_hp, my_armor, my_mana, boss_hp

    if debug:
        print()
        print('-- Player turn --')
        print('- Player has ' + str(my_hp) + ' hit points, ' + str(my_armor) + ' armor, ' + str(my_mana) + ' mana')
        print('- Boss has ' + str(boss_hp) + ' hit points')

    if autoDamage:
        my_hp -= 1
        if my_hp < 1:
            if debug: print('Auto-damage kills the player, and the boss wins.')
            return True

    handleActiveSpells(debug)
    if boss_hp < 1:
        if debug: print('This kills the boss, and the player wins.')
        return True

    # Player Attack
    if spell == 'M':
        if debug: print('Player casts Magic Missile, dealing 4 damage.')
        my_mana -= spells['M'][0]
        boss_hp -= spells['M'][1]
    elif spell == 'D':
        if debug: print('Player casts Drain, dealing 2 damage, and healing 2 hit points.')
        my_mana -= spells['D'][0]
        boss_hp -= spells['D'][1]
        my_hp += spells['D'][2]
    elif spell == 'S':
        if debug: print('Player casts Shield, increasing armor by 7.')
        my_mana -= spells['S'][0]
        my_armor += spells['S'][4]
        make_active('S')
    elif spell == 'P':
        if debug: print('Player casts Poison.')
        my_mana -= spells['P'][0]
        make_active('P')
    elif spell == 'R':
        if debug: print('Player casts Recharge.')
        my_mana -= spells['R'][0]
        make_active('R')

    if my_mana < 0:
        if debug: print('The player does not have enough mana and loses.')
        return True

    if boss_hp < 1:
        if debug: print('This kills the boss, and the player wins.')
        return True

    # Boss attack
    if debug:
        print()
        print('-- Boss turn --')
        print('- Player has ' + str(my_hp) + ' hit points, ' + str(my_armor) + ' armor, ' + str(my_mana) + ' mana')
        print('- Boss has ' + str(boss_hp) + ' hit points')

    handleActiveSpells(debug)
    if boss_hp < 1:
        if debug: print('This kills the boss, and the player wins.')
        return True

    damage = boss_damage - my_armor
    if damage < 1: damage = 1
    if debug: print('Boss attacks for ' + str(damage) + ' damage!')
    my_hp -= damage
    if my_hp < 1:
        if debug: print('This kills the player, and the boss wins.')
        return True

    return False

# Test the scenario on the page....
my_hp, my_mana = 10, 250
boss_hp, boss_damage = 14, 8
spell_list = 'RSDPM'
for t in spell_list:
    if turn(t, debug=True):
        break

# Worse case:
# Recharge, Shield, and Poison can be cast every 3 turns
# Cast Recharge, Shield, Poison, Recharge, Shield, Poison, ....
# Every six turns costs 229+173+113 = 515 mana
#                 Armor is 7 except for first time attacked
#                 Boss is damaged 3 each turn
#                 I am damaged 8 the first boss' turn, 1 every boss' turn after that
#                 If boss has 55 hit points, it will take 4 + 19 turns to kill the boss
# Therefore, 25 turns should be enough to win any game

def addFirstTurn(mana):
    return [(mana - spells[s][0], spells[s][0], s) for s in 'MDSPR']


def addturn(pg):
    newpg = []
    for p in pg:
        mana = p[0]
        total = p[1]
        spell = p[2]
        if len(spell) > 0 and spell[-1:] == 'R': mana += spells['R'][4]
        if len(spell) > 1 and spell[-2:-1] == 'R': mana += spells['R'][4] * 2
        if len(spell) > 2 and spell[-3:-2] == 'R': mana += spells['R'][4] * 2
        if mana < minSpellCost or total >= gamemax:
            newpg += [p]
        else:
            check_str = spell if len(spell) < 3 else spell[-2:]
            if mana >= spells['M'][0]:
                newpg += [(mana - spells['M'][0], total+spells['M'][0], spell + 'M')]
            if mana >= spells['D'][0]:
                newpg += [(mana - spells['D'][0], total+spells['D'][0], spell + 'D')]
            if not 'S' in check_str and mana >= spells['S'][0]:
                newpg += [(mana - spells['S'][0], total+spells['S'][0], spell + 'S')]
            if not 'P' in check_str and mana >= spells['P'][0]:
                newpg += [(mana - spells['P'][0], total+spells['P'][0], spell + 'P')]
            if not 'R' in check_str and mana >= spells['R'][0]:
                newpg += [(mana - spells['R'][0], total+spells['R'][0], spell + 'R')]
    return newpg

# Part 1 

# Get a list of all possible games we could play without running out of mana ... up to a certain length
gamemax = 1300
_, _, _, my_mana = me
possible_games = addFirstTurn(my_mana)
for i in range(0, 8):
    possible_games = addturn(possible_games)

#print(possible_games)
possible_games.sort(key = lambda x: x[1])
print(len(possible_games))

for i in range(0,50000):
    boss_hp, boss_damage = boss
    my_hp, my_damage, my_armor, my_mana = me
    spell_list = possible_games[i][2]
    activespells = {}

    for t in spell_list:
        if turn(t):
            break
    if boss_hp < 1 and my_hp > 0:
        print()
        print('------------------------ FOUND A WINNER for PART 1 ------------------------')
        print()
        print(possible_games[i])
        print('Mana spent: ' + str(possible_games[i][1]) + ' on the ' + str(i) + 'th cheapest game')
        print('- Player has ' + str(my_hp) + ' hit points, ' + str(my_armor) + ' armor, ' + str(my_mana) + ' mana')
        print('- Boss has ' + str(boss_hp) + ' hit points')
        print()
        break

# Part 2

# FIXME For part 2 have to run each game fully when generating the possible games so we can
# stop generating paths that end in a win or loss and not keep generating those paths.
# That's part of the problem.  We're looking at the total cost 
# FIXME Got lucky and length 8 is the magic number.  So don't have to do the above.

maxmana = 0
for i in range(0,4000000):
    boss_hp, boss_damage = boss
    my_hp, my_damage, my_armor, my_mana = me
    spell_list = possible_games[i][2]
    activespells = {}

    maxmana = possible_games[i][1]

    for t in spell_list:
        if turn(t, autoDamage=True):
            break
    if boss_hp < 1 and my_hp > 0:
        print()
        print('------------------------ FOUND A WINNER for PART 2 ------------------------')
        print()
        print(possible_games[i])
        print('Mana spent: ' + str(possible_games[i][1]) + ' on the ' + str(i) + 'th cheapest game')
        print('- Player has ' + str(my_hp) + ' hit points, ' + str(my_armor) + ' armor, ' + str(my_mana) + ' mana')
        print('- Boss has ' + str(boss_hp) + ' hit points')
        print()
        break

print('Maximum mana tried: ' + str(maxmana))

