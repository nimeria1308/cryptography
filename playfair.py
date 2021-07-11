from itertools import permutations
from textwrap import wrap


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

    # move down the column/row if encoding
    # move up the column/row if decoding
    # rectangle rule is the same in both cases
    x = 1 if encode else -1

    # find coordinates for each character
    a = playfair_get_coordinates(a, key)
    b = playfair_get_coordinates(b, key)

    # handle encoding/decoding with partial keys
    if not a or not b:
        return "??"

    # same column
    if a[0] == b[0]:
        # return characters down/up the column
        c = (a[0], a[1] + x)
        d = (b[0], b[1] + x)
    elif a[1] == b[1]:
        # return characters right/left the row
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
    # split the text into pairs of characters
    pairs = wrap(plain_text, 2)

    # encode / decode
    cypher_text = [playfair_get_pair(pair, key, encode) for pair in pairs]

    # join the pairs back into a string
    return "".join(cypher_text)


def playfair_try_decript(crypt_text, key, output_file):
    # create a list of all letters, except for J
    letters = [chr(x) for x in range(ord('A'), ord('Z') + 1) if x != ord('J')]
    key_letters = "".join(key)

    # filter out all letters that are missing in the key
    missing_letters = [x for x in letters if x not in key_letters]

    # iterate over all permutations of the missing letters
    for p in permutations(missing_letters):
        new_key = "".join(key)
        # replace placeholders in key "_" with the letter from the permutation
        for l in p:
            new_key = new_key.replace('_', l, 1)

        # wrap the key as 5-letter rows
        new_key_wrapped = wrap(new_key, 5)

        # decrypt and save to output
        decrypted = playfair(crypt_text, new_key_wrapped, False)
        output_file.write("%s %s\n" % (new_key, decrypted))


KEYS = [
    [
        "ZENTW",
        "_B__U",
        "OSA_F",
        "IRDGH",
        "_C___",
    ],
    [
        "ZENTW",
        "OSA_F",
        "IRDGH",
        "_B__U",
        "_C___",
    ],
]

cipher_text = "EBQXZLHDLKIVQGOMALEBVBDOSGSFZRANDAMOLBSEELSOZLKDCOZFGSIN"
with open("playfair_output.txt", "w") as f:
    for key in KEYS:
        playfair_try_decript(cipher_text, key, f)
