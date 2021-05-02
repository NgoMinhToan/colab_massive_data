maxtrix = [[0, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0],
            [0,0,0,0,1,1,0],
            [1,0,1,0,1,0]]

permutation = [[2,3,7,6,1,5],
                [4,2,1,3,6,7],
                [3,4,7,2,6,1]]

sign = []
for m in maxtrix:
    temp_sign = []
    for p in  permutation:
        temp = []
        for i in range(len(m)):
            if m[i] == 1:
                temp.append(p[i])
        temp_sign.append(min(temp))
    sign.append(temp_sign)

pairs = []
for i in range(len(sign) - 1):
    for j in range(i + 1, len(sign)):
        pairs.append([i, j])

sigOSig = []
for pair in pairs:
    temp = 0
    for i in range(len(sign[0])):
        if sign[pair[0]][i] == sign[pair[1]][1]:
            temp += 1
    sigOSig.append(temp/len(sign[0]))

print('pairs: ', pairs)
for i in sigOSig:
    print(i)

for i in range(len(sign[0])):
    print (list(map(lambda a: a[i], sign)))