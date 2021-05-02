import csv

s = 50

data = []
with open('./store_data.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        data.append(row)

# print(data[0])

# C1
C1 = {}
for j in data:
    for i in j:
        if i not in list(C1.keys()):
            C1[i] = 1
        else:
            C1[i] += 1

# L1
for i in list(C1.keys()):
    if C1[i] < s:
        del C1[i]

# C2
C2 = {}
for i in list(C1.keys()):
    for j in list(C1.keys()):
        if i == j:
            continue
        if frozenset([i, j]) not in C2.keys():
            C2[frozenset([i, j])] = 0

# L2
for i in list(C2.keys()):
    for j in data:
        if len(i - set(j))==0:
            C2[i] += 1

for i in list(C2.keys()):
    if C2[i] < s:
        del C2[i]

# C3
C3 = {}
for i in list(C2.keys()):
    for j in list(C2.keys()):
        if i == j:
            continue
        if len(set(list(i) + list(j))) == 4:
            continue
        C3[frozenset(list(i) + list(j))] = 0

# L3
for i in list(C3.keys()):
    for j in data:
        if len(i - set(j))==0:
            C3[i] += 1

for i in list(C3.keys()):
    if C3[i] < s:
        del C3[i]

print(C3)