from collections import OrderedDict
from pprint import pprint
from textwrap import wrap


def playfair_generate_pairs(plain_text, cipher_text):
    return {
        p: c for p, c in zip(wrap(plain_text, 2), wrap(cipher_text, 2))
    }


def playfair_best_sequence(pairs):
    result = OrderedDict()
    chars = set()
    pp = list(pairs.keys())

    # find pairs with a common letter
    for p in pp:
        c = pairs[p]
        if (p[0] in c) or (p[1] in c):
            # add to result
            result[p] = (c, 4)

            # add to found chars
            for x in (p + c):
                chars.add(x)

            # remove from list
            pp.remove(p)

    while pp:
        best_score = 0
        best_pair = None
        competitors = 0

        for p in pp:
            if p in result:
                pp.remove(p)
                continue

            c = pairs[p]

            # compute score
            # how many of the chars are already fixed
            score = sum([1 if x in chars else 0 for x in (p + c)])

            # found new candidate
            if score >= best_score:
                best_score = score
                best_pair = p
                competitors += 1

        if best_pair is not None:
            # add to result
            best_pair_c = pairs[best_pair]
            result[best_pair] = (best_pair_c, best_score)
            # print("Found %s -> %s score: %d competitors: %d" % (best_pair, best_pair_c, best_score, competitors))

            # add to found chars
            for x in (best_pair + best_pair_c):
                chars.add(x)

            # remove from list
            pp.remove(best_pair)

    return result


s = playfair_generate_pairs(
    "THEWINTEROFOURDISCONTENT", "WGNZDZWNISOSBHGRREAZWNTW")

bs = playfair_best_sequence(s)

# print pairs
for p, c in bs.items():
    print("%s %s %d" % (p, c[0], c[1]))
