#!/usr/bin/python3

import re

f = open("input19.txt", "r")
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
        #if ip == 1: print(output)
        #if instructions % 100000 == 0:  print("%d instructions" % (instructions))
        #if instructions == 30: break

stepUntilDone()
print("After %d instructions the registers contain: %s" % ( instructions, registers ))

# Part 1 the fast way

flag = 0
limit = 947
if flag == 1:
    limit += 10550400

sums = 0
for i in range(1, limit+1):
    for j in range(1, limit+1):
        if i * j == limit: sums += i

print("sums = %d" % (sums))

# PART 2 the super fast way

limit = 947 + 10550400
sums = 0
for i in range(1, limit+1):
    if limit % i == 0: sums += i

print("sums (aka register 0) = %d" % (sums))

# part 2 the slow way -- this would take forever
#registers = [ 1, 0, 0, 0, 0, 0 ]
#instructions = 0
#ip = 0
#ipregister = -1
#linesNotCounted = 0
#
#stepUntilDone()
#print("After %d instructions the registers contain: %s" % ( instructions, registers ))

