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

    t = 0
    current = starter
    while t < max_period:
        t += 1
        current = lsfr_next(coeffs, current)
        if current == starter:
            print("%s <> %s -> %d" % (coeffs, starter, t))
            return t

    return 0

def find_period(coeffs):
    periods = set()

    for starter in product((0, 1), repeat=len(coeffs)):
        # skip (0,0,0, ...) input
        if any(starter):
            periods.add(_find_period(coeffs, starter))

    print(periods)
    return periods.pop() if (len(periods) == 1) else 0

def make_lsfr(period, all_results=True):
    results = []
    lsfr_length = ceil(log2(period))

    for coeffs in product((0, 1), repeat=lsfr_length):
        new_period = find_period(coeffs)
        print("%s -> %d" % (coeffs, new_period))
        if new_period == period:
            results.append(coeffs)
        if not all_results:
            break

    return results

# print(find_period((1, 1, 0, 0)))
print(make_lsfr(21))
