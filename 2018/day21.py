#!/usr/bin/python3

import re

f = open("input21.txt", "r")
lines = f.readlines()
f.close()

lines = [l.rstrip('\r\n') for l in lines]

registers = [ 0, 0, 0, 0, 0, 0 ]
instructions = 0
ip = 0
ipregister = -1
linesNotCounted = 0

def doStep(line):
    global ip, registers, instructions, ipregister, linesNotCounted

    if ipregister >= 0: registers[ipregister] = ip

    m = re.search('^(([^ ]+) (\d+) (\d+) (\d+))|(#ip (\d+))$', line) 
    if m.group(1):
        opcode, A, B, C = [m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))]
    elif m.group(6):
        ipregister = int(m.group(7))
        linesNotCounted += 1
        return "Set ipregister to %d" % (ipregister)
    else:
        print("Nothing detected on line '%s'" % (line))
        return None

    printout = "ip=" + str(ip) + " " + str(registers) + " " + line + " "
    instructions += 1

    if   opcode == 'addr':  registers[C] = registers[A] + registers[B]
    elif opcode == 'addi':  registers[C] = registers[A] + B
    elif opcode == 'mulr':  registers[C] = registers[A] * registers[B]
    elif opcode == 'muli':  registers[C] = registers[A] * B
    elif opcode == 'banr':  registers[C] = registers[A] & registers[B]
    elif opcode == 'bani':  registers[C] = registers[A] & B
    elif opcode == 'borr':  registers[C] = registers[A] | registers[B]
    elif opcode == 'bori':  registers[C] = registers[A] | B
    elif opcode == 'setr':  registers[C] = registers[A]
    elif opcode == 'seti':  registers[C] = A
    elif opcode == 'gtir':  registers[C] = 1 if A > registers[B] else 0
    elif opcode == 'gtri':  registers[C] = 1 if registers[A] > B else 0
    elif opcode == 'gtrr':  registers[C] = 1 if registers[A] > registers[B] else 0
    elif opcode == 'eqir':  registers[C] = 1 if A == registers[B] else 0
    elif opcode == 'eqri':  registers[C] = 1 if registers[A] == B else 0
    elif opcode == 'eqrr':  registers[C] = 1 if registers[A] == registers[B] else 0
    else:
        print("WHOOPS - UNKNOWN INSTRUCTION %s" % ( opcode ))
        return None

    if ipregister >= 0: ip = registers[ipregister]
    ip += 1

    return printout + str(registers)

def stepUntilDone():
    while True:
        nextip = ip + linesNotCounted
        if nextip >= len(lines):
            print("Instruction %d taken outside the bounds 0-%d" % ( ip, len(lines)-linesNotCounted-1))
            break
        output = doStep(lines[nextip])
        if not output:
            print("Unexpected condition - exiting:")
            break
        #print(output)
        #if ip == 28 or ip == 6 or ip == 13: print(output)
        if ip == 28: print(output)
        #if instructions % 100000 == 0:  print("%d instructions" % (instructions))
        #if instructions == 30: break

#stopAt = 15861151
stopAt = -1

def Program():
    lastValueSeen = 0
    valuesSeen = set()
    reg3 = 0
    while True:
        reg2 = reg3 | 0x10000
        reg3 = 1099159
        while True:
            reg3 = (((reg3 + (reg2 & 0xff)) & 0xFFFFFF) * 65899) & 0xFFFFFF
            if reg2 >= 256:
                reg2 = reg2 // 256
                continue
            if reg3 in valuesSeen:
                print("The first repeat is %d and the last value is %d" % ( reg3, lastValueSeen ))
                return
            valuesSeen.add(reg3)
            lastValueSeen = reg3
            if len(valuesSeen) % 1000 == 0:
                print("Number of values seen so far:  %d" % ( len(valuesSeen) ))
            if reg3 == stopAt: return
            break

Program()

registers[0] =  stopAt
stepUntilDone()

