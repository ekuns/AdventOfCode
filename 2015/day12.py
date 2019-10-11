import json

f = open("input12.txt", "r")
lines = f.readlines()
f.close()
print('Number of lines: ' + str(len(lines)))

value = lines[0].strip()

# Part 1

x = json.loads(value)

def addnumbers(obj):
    if isinstance(obj, dict):
        return sum([addnumbers(value) for key, value in obj.items()])
    elif isinstance(obj, list):
        return(sum([addnumbers(i) for i in obj]))
    elif isinstance(obj, str):
        pass
    elif isinstance(obj, int):
        return obj
    else:
        print(type(obj))
    return 0

print(addnumbers(x))

# Part 2

def addNonRedNumbers(obj):
    if isinstance(obj, dict):
        return 0 if 'red' in obj.values() else sum([addNonRedNumbers(value) for key, value in obj.items()])
    elif isinstance(obj, list):
        return(sum([addNonRedNumbers(i) for i in obj]))
    elif isinstance(obj, str):
        pass
    elif isinstance(obj, int):
        return obj
    else:
        print(type(obj))
    return 0

print(addNonRedNumbers(x))

