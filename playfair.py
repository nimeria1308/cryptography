from textwrap import wrap


def playfair_get_character(coords, key):
    # get the line. instead of mod 5,
    # use line count to keep it generic
    line = key[coords[1] % len(key)]

    # same here, but return the character
    character = line[coords[0] % len(line)]

    return character


def playfair_get_coordinates(character, key):
    for y, line in enumerate(key):
        if character in line:
            # found y, find x
            x = line.find(character)
            return x, y


def playfair_get_pair(input_pair, key, encode):
    # extract pair into two separate characters a and b
    a, b = input_pair

    if a == b:
        raise Exception("Characters must differ")

    # move down the column/line if encoding
    # move up the column/line if decoding
    # rectangle rule is the same in both cases
    x = 1 if encode else -1

    # find coordinates for each character
    a = playfair_get_coordinates(a, key)
    b = playfair_get_coordinates(b, key)

    # same column
    if a[0] == b[0]:
        # return characters down the column
        c = (a[0], a[1] + x)
        d = (b[0], b[1] + x)
    elif a[1] == b[1]:
        # return characters down the line
        c = (a[0] + x, a[1])
        d = (b[0] + x, b[1])
    else:
        # use rectangle rule
        # RW -> US
        c = (b[0], a[1])
        d = (a[0], b[1])

    # now find the characters
    c_ = playfair_get_character(c, key)
    d_ = playfair_get_character(d, key)

    # and return as a string
    return "".join([c_, d_])


def playfair(plain_text, key, encode):
    if len(plain_text) % 2 != 0:
        raise Exception("Text needs to be in pairs")

    # split the text into pairs of characters
    pairs = wrap(plain_text.upper(), 2)

    # encode / decode
    cypher_text = [playfair_get_pair(pair, key, encode) for pair in pairs]

    # back to a string
    return "".join(cypher_text)


KEY = (
    "OGETN",
    "MQVBK",
    "DWZSY",
    "PULRI",
    "AXFHC",
)

p = "CRYPTOGRAPHY"
# p = "RWSUXBTL"
c = playfair(p, KEY, True)
p2 = playfair(c, KEY, False)
print("%s -> %s -> %s" % (p, c, p2))
