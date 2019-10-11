#!/usr/bin/python3

import re

f = open("input16.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

threes = 0
tested = 0

registers = [ 0, 0, 0, 0 ]
opcodes = {}
skip = 0
collapsed = False
instructions = 0

for i in range(0, len(lines)):
    if skip > 0:
        skip -= 1
        continue
 
    l = lines[i]
    if l.startswith('Before: '):
        skip = 2
        tested += 1

        m1 = re.search('^Before: \[(\d+), (\d+), (\d+), (\d+)\]$', l)
        rBefore = [int(m1.group(1)), int(m1.group(2)), int(m1.group(3)), int(m1.group(4))]

        m2 = re.search('(\d+) (\d+) (\d+) (\d+)$', lines[i+1])
        operands = [int(m2.group(1)), int(m2.group(2)), int(m2.group(3)), int(m2.group(4))]

        m3 = re.search('^After:  \[(\d+), (\d+), (\d+), (\d+)\]$', lines[i+2])
        rAfter  = [int(m3.group(1)), int(m3.group(2)), int(m3.group(3)), int(m3.group(4))]

        A = operands[1]
        B = operands[2]
        C = operands[3]

        count = 0
        opcode = None
        opcodeList = set()

        #addr
        if rAfter[C] == rBefore[A] + rBefore[B]:
            opcode = "addr"
            opcodeList.add(opcode)
            count += 1

        #addi
        if rAfter[C] == rBefore[A] + B:
            opcode = "addi"
            opcodeList.add(opcode)
            count += 1

        #mulr
        if rAfter[C] == rBefore[A] * rBefore[B]:
            opcode = "mulr"
            opcodeList.add(opcode)
            count += 1

        #muli
        if rAfter[C] == rBefore[A] * B:
            opcode = "muli"
            opcodeList.add(opcode)
            count += 1

        #banr
        if rAfter[C] == rBefore[A] & rBefore[B]:
            opcode = "banr"
            opcodeList.add(opcode)
            count += 1

        #bani
        if rAfter[C] == rBefore[A] & B:
            opcode = "bani"
            opcodeList.add(opcode)
            count += 1

        #borr
        if rAfter[C] == rBefore[A] | rBefore[B]:
            opcode = "borr"
            opcodeList.add(opcode)
            count += 1

        #bori
        if rAfter[C] == rBefore[A] | B:
            opcode = "bori"
            opcodeList.add(opcode)
            count += 1

        #setr
        if rAfter[C] == rBefore[A]:
            opcode = "setr"
            opcodeList.add(opcode)
            count += 1

        #seti
        if rAfter[C] == A:
            opcode = "seti"
            opcodeList.add(opcode)
            count += 1

        #gtir
        if (rAfter[C] == 1 and A > rBefore[B]) or  (rAfter[C] == 0 and A <= rBefore[B]):
            opcode = "gtir"
            opcodeList.add(opcode)
            count += 1

        #gtri
        if (rAfter[C] == 1 and rBefore[A] > B) or  (rAfter[C] == 0 and rBefore[A] <= B):
            opcode = "gtri"
            opcodeList.add(opcode)
            count += 1

        #gtrr
        if (rAfter[C] == 1 and rBefore[A] > rBefore[B]) or  (rAfter[C] == 0 and rBefore[A] <= rBefore[B]):
            opcode = "gtrr"
            opcodeList.add(opcode)
            count += 1

        #eqir
        if (rAfter[C] == 1 and A == rBefore[B]) or  (rAfter[C] == 0 and A != rBefore[B]):
            opcode = "eqir"
            opcodeList.add(opcode)
            count += 1

        #eqri
        if (rAfter[C] == 1 and rBefore[A] == B) or  (rAfter[C] == 0 and rBefore[A] != B):
            opcode = "eqri"
            opcodeList.add(opcode)
            count += 1

        #eqrr
        if (rAfter[C] == 1 and rBefore[A] == rBefore[B]) or  (rAfter[C] == 0 and rBefore[A] != rBefore[B]):
            opcode = "eqrr"
            opcodeList.add(opcode)
            count += 1

        op = operands[0]
        if not op in opcodes:
            opcodes[op] = opcodeList
        else:
            opcodes[op] = opcodeList.intersection(opcodes[op])

        if count >= 3:
            threes += 1
    elif len(l) == 0:
        pass
    else:
        if not collapsed:
            changed = True
            while changed:
                changed = False
                for k,v in dict(opcodes).items():
                    if len(v) == 1:
                        item = next(iter(v))
                        for k2,v2 in dict(opcodes).items():
                            if k != k2 and item in v2:
                                #print("Removing %s from %s" % ( item, v2 ))
                                v2.remove(item)
                                changed = True
            for k,v in dict(opcodes).items():
                opcodes[k] = next(iter(v))
            collapsed = True

        #print("Looking at line %s" % ( l ))
        #for k,v in opcodes.items():
        #    print("%s - %s" % (k,v))
        m2 = re.search('(\d+) (\d+) (\d+) (\d+)$', l)
        if m2 != None:
            instructions += 1
            operands = [int(m2.group(1)), int(m2.group(2)), int(m2.group(3)), int(m2.group(4))]
            opcode = opcodes[operands[0]]
            A = operands[1]
            B = operands[2]
            C = operands[3]
            if opcode == 'addr':
                registers[C] = registers[A] + registers[B]
            elif opcode == 'addi':
                registers[C] = registers[A] + B
            elif opcode == 'mulr':
                registers[C] = registers[A] * registers[B]
            elif opcode == 'muli':
                registers[C] = registers[A] * B
            elif opcode == 'banr':
                registers[C] = registers[A] & registers[B]
            elif opcode == 'bani':
                registers[C] = registers[A] & B
            elif opcode == 'borr':
                registers[C] = registers[A] | registers[B]
            elif opcode == 'bori':
                registers[C] = registers[A] | B
            elif opcode == 'setr':
                registers[C] = registers[A]
            elif opcode == 'seti':
                registers[C] = A
            elif opcode == 'gtir':
                registers[C] = 1 if A > registers[B] else 0
            elif opcode == 'gtri':
                registers[C] = 1 if registers[A] > B else 0
            elif opcode == 'gtrr':
                registers[C] = 1 if registers[A] > registers[B] else 0
            elif opcode == 'eqir':
                registers[C] = 1 if A == registers[B] else 0
            elif opcode == 'eqri':
                registers[C] = 1 if registers[A] == B else 0
            elif opcode == 'eqrr':
                registers[C] = 1 if registers[A] == registers[B] else 0
            else:
                print("WHOOPS - UNKNOWN INSTRUCTION %s" % ( opcode ))

print("%d of %d lines act like three instructions" % (threes, tested))
print("After %d instructions the registers contain: %s" % ( instructions, registers ))

