from math import ceil, log2
from itertools import product


def lsfr_next(coeffs, current):
    # shift left by one
    result = current[1:]

    # compute next number
    new_number = sum([coeffs[c] * current[c] for c in range(len(coeffs))]) % 2

    return result + (new_number, )


def _find_period(coeffs, starter):
    max_period = 2 ** len(coeffs)

    period = 0
    current = starter

    # get data of size max_period * 2
    for _ in range(max_period * 2 -1):
        current = lsfr_next(coeffs, current)
        if current == starter:
            break
        period += 1

    return period

def find_period(coeffs):
    periods = set()

    for starter in product((0, 1), repeat=len(coeffs)):
        # skip (0,0,0, ...) input
        if any(starter):
            periods.add(_find_period(coeffs, starter))

    return periods.pop() if (len(periods) == 1) else 0

def make_lsfr(period):
    results = {}
    lsfr_length = ceil(log2(period)) + 1

    # try all coeffients
    for coeffs in product((0, 1), repeat=lsfr_length):
        # skip (0,0,0, ...) ceoffs
        if any(coeffs):
            new_period = find_period(coeffs)
            if new_period:
                results[coeffs] = new_period

    return results

def print_coeffs(coeffs):
    for c in coeffs:
        print(coeffs)
        max_period = 2 ** len(c)
        starter = (1,) + ((0,) * (len(c) - 1))
        data = [starter]
        current = starter

        # get data of size max_period * 2
        for _ in range(max_period * 2 -1):
            current = lsfr_next(c, current)
            data.append(current)

        for i in range(max_period):
            print("%s %s" % (data[i], data[i+(max_period - 1)]))

        print("")

coeffs = make_lsfr(21)
print(coeffs)
# print_coeffs(coeffs)
