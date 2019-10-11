import bisect
import re

f = open("input20.txt", "r")
lines = f.readlines()
f.close()

class sorted_range_list(list):
    def addrange(self, newrange):
        if not self:
            self.append(newrange)
            return

        offset = bisect.bisect_left(self, newrange)
        bisect.insort(self, newrange)

        while True:
            changed = False
            # Merge with the previous entry?
            if offset > 0 and self[offset][0] <= self[offset-1][1]+1:
                if self[offset-1][0] > self[offset][0]:
                    asdf
                self[offset-1] = (self[offset-1][0], max(self[offset-1][1], self[offset][1]))
                del self[offset]
                offset -= 1
                changed = True
            # Merge with the following entry?
            if offset+1 < len(self) and self[offset][1]+1 >= self[offset+1][0]:
                self[offset] = (self[offset][0], max(self[offset][1],self[offset+1][1]))
                del self[offset+1]
                changed = True
            if not changed:
                break


excluded = sorted_range_list()

for l in lines:
    m = re.match('^(\d+)-(\d+)$', l.strip())
    start, end = int(m.group(1)), int(m.group(2))
    excluded.addrange((start, end))

#print(excluded)

# Part 1

print('The first available IP Address is ' + str(excluded[0][1]+1))

# Part 2

count = 0
# Account for available items at the beginning or end of the list
count += excluded[0][0]
count += 4294967295 - excluded[-1][1]
# Add all available items inside the list
for i in range(0, len(excluded)-1):
    available = excluded[i+1][0] - excluded[i][1] - 1
    #print(str(available) + ' between ' + str(excluded[i]) + ' and ' + str(excluded[i+1]))
    count += available

print('There are ' + str(count) + ' unused IP Addresses')

