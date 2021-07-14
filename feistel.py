def fmt_bin(number, bits):
    fmt = "{:0%db}" % bits
    return fmt.format(number)


def feistel_one_step(block, m, n, fn):
    block_in = fmt_bin(block, m+n)
    a = int(block_in[:m], 2)
    b = int(block_in[m:], 2)

    a_new = b
    b_new = a ^ fn[b]

    return int(fmt_bin(a_new, m) + fmt_bin(b_new, m), 2)


def feistel(block, m, n, functions):
    blocks = []

    for fn in functions:
        block = feistel_one_step(block, m, n, fn)
        blocks.append(block)

    return blocks


functions = [
    # f1
    [
        0b00, 0b10, 0b11, 0b11, 0b01, 0b01, 0b01, 0b10,
        0b10, 0b01, 0b10, 0b11, 0b00, 0b00, 0b00, 0b00,
    ],
    # f2
    [
        0b10, 0b11, 0b00, 0b11, 0b10, 0b11, 0b01, 0b01,
        0b01, 0b11, 0b10, 0b00, 0b10, 0b11, 0b01, 0b00,
    ],
    # f3
    [
        0b10, 0b00, 0b00, 0b01, 0b01, 0b10, 0b10, 0b11,
        0b01, 0b11, 0b00, 0b10, 0b11, 0b10, 0b11, 0b01,
    ],
    # f4
    [
        0b11, 0b10, 0b01, 0b10, 0b00, 0b10, 0b00, 0b00,
        0b10, 0b01, 0b00, 0b10, 0b01, 0b11, 0b10, 0b11,
    ],
]

for idx, block in enumerate(feistel(0b101101, 2, 4, functions)):
    print("block fn[%d] = %s" % (idx + 1, fmt_bin(block, 2 + 4)))
