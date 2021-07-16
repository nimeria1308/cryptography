CODEWORDS = [
    [0, 1, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 1, 0, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
]

CW = []
for c in CODEWORDS:
    if c[-1] == 1:
        CW.append("".join([str(x) for x in c]))

CW_DEC = [int(c,2) for c in CW]

def is_minimal(c, codewords):
    for i in range(len(codewords)):
        c1 = codewords[i]
        for c2 in codewords[i+1:]:
            # print("%d vs %d: %d + %d" % (c, c1 + c2, c1, c2))
            if c1 + c2 == c:
                print("%d = %d + %d" % (c, c1, c2))
                return False
    return True

def find_minimal(codewords):
    minimal = set()

    for c in codewords:
        cc = list(codewords)
        cc.remove(c)
        if is_minimal(c, cc):
            minimal.add(c)

    return minimal


minimal = find_minimal(CW_DEC)
print(sorted(CW_DEC))
print(sorted(minimal))
