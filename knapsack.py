from textwrap import wrap


def knapsack(plain_text, alphabet, a, m, t):
    n = len(a)
    b = [(x * t) % m for x in a]
    fmt = "{:0%db}{:0%db}" % (n // 2, n // 2)

    result = []

    for pair in wrap(plain_text, 2):
        p_a, p_b = pair
        p_a = alphabet[p_a]
        p_b = alphabet[p_b]
        a_mask = fmt.format(p_a, p_b)

        pair_sum = 0
        for bit, bit_mask in enumerate(a_mask):
            if bit_mask == "1":
                pair_sum += b[bit]

        result.append(pair_sum)

    return result


alphabet = {
    chr(ord("A") + c): c + 1 for c in range(26)
}

a = [103, 107, 211, 430, 863, 1718, 3449, 6907, 13807, 27610, ]

print(knapsack("CRYPTOGRAPHY", alphabet, a, 55207, 25236))


alphabet = {
    "A": 0b00011,
    "H": 0b01100,
    "O": 0b10100,
    "V": 0b11011,
    "B": 0b00101,
    "I": 0b01101,
    "P": 0b10101,
    "W": 0b11100,
    "C": 0b00110,
    "J": 0b01110,
    "Q": 0b10110,
    "X": 0b11101,
    "D": 0b00111,
    "K": 0b01111,
    "R": 0b10111,
    "Y": 0b11110,
    "E": 0b01001,
    "L": 0b10001,
    "S": 0b11000,
    "Z": 0b11111,
    "F": 0b01010,
    "M": 0b10010,
    "T": 0b11001,
    "G": 0b01011,
    "N": 0b10011,
    "U": 0b11010,
}

a = [2, 3, 7, 13, 27, 53, 106, 213, 425, 851]

print(knapsack("CRYPTOGRAPHY", alphabet, a, 1529, 64))
