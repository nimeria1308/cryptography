from itertools import permutations
from textwrap import wrap
from tqdm import tqdm


def playfair_get_character(coords, key):
    # get the row. instead of mod 5,
    # use row count to keep it generic
    row = key[coords[1] % len(key)]

    # same here, but return the character
    character = row[coords[0] % len(row)]

    return character


def playfair_get_coordinates(character, key):
    for y, row in enumerate(key):
        if character in row:
            # found y, find x
            x = row.find(character)
            return x, y


def playfair_get_pair(input_pair, key, encode):
    # extract pair into two separate characters a and b
    a, b = input_pair

    if a == b:
        raise Exception("Characters must differ")

    # move down the column/row if encoding
    # move up the column/row if decoding
    # rectangle rule is the same in both cases
    x = 1 if encode else -1

    # find coordinates for each character
    a = playfair_get_coordinates(a, key)
    b = playfair_get_coordinates(b, key)

    if not a or not b:
        return "??"

    # same column
    if a[0] == b[0]:
        # return characters down the column
        c = (a[0], a[1] + x)
        d = (b[0], b[1] + x)
    elif a[1] == b[1]:
        # return characters down the row
        c = (a[0] + x, a[1])
        d = (b[0] + x, b[1])
    else:
        # use rectangle rule
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


def playfair_try_decript(crypt_text, key):
    # create a list of all letters
    letters = [chr(x) for x in range(ord('A'), ord('Z') + 1) if x != ord('J')]
    key_letters = "".join(key)

    missing_letters = [x for x in letters if x not in key_letters]

    all_permutations = list(permutations(missing_letters))
    results = {}

    for p in tqdm(all_permutations):
        new_key = "".join(KEY)
        for l in p:
            new_key = new_key.replace('_', l, 1)
        new_key = wrap(new_key, 5)

        decrypted = playfair(crypt_text, new_key, False)
        if "CRYPTOGRAPHY" in decrypted:
            results["".join(new_key)] = decrypted

    return results


KEY = [
    "NTWZE",
    "A_FOS",
    "DGHIR",
    "__U_B",
    "____C",
]

c = "EBQXZLHDLKIVQGOMALEBVBDOSGSFZRANDAMOLBSEELSOZLKDCOZFGSIN"
res = playfair_try_decript(c, KEY)
print(res)
