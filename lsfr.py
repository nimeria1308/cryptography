def pop_count(x):
    c = 0
    while x:
        if (x & 1):
            c += 1

        x >>= 1

    return c


def lsfr(taps, value, size):
    # generate mask
    mask = (1 << size) - 1

    # shift left
    new_value = (value << 1) & mask

    # find new bit
    new_value |= (pop_count(value & taps) % 2)

    return new_value


def find_period(taps, start_value, size):
    current = start_value
    t = 0
    previous = set([start_value])

    while True:
        current = lsfr(taps, current, size)
        t += 1

        if current in previous:
            break

        previous.add(current)

    return t


def find_taps_with_period(size):
    max_value = (1 << size) - 1
    results = {}

    for taps in range(1, max_value + 1):
        found_period = True
        period = find_period(taps, 1, size)

        if period:
            for start_value in range(2, max_value+1):
                p = find_period(taps, start_value, size)
                if p != period:
                    found_period = False
                    break
        else:
            found_period = False

        if found_period:
            results[taps] = period

    return results


def print_lsfr(taps, start_value, size):
    current = start_value
    period = find_period(taps, start_value, size)
    fmt = "period={:d} taps={:0%db}" % size
    print(fmt.format(period, taps))

    print("t  S")
    fmt = "{:2d} {:0%db}" % size
    for t in range(period + 1):
        print(fmt.format(t, current))
        current = lsfr(taps, current, size)
    print("")


taps = find_taps_with_period(6)
for tap, period in taps.items():
    print("taps={:06b} period={}".format(tap, period))

taps_21 = [tap for tap, period in taps.items() if period == 21]

for tap in taps_21:
    print("taps={:06b}".format(tap))
    print_lsfr(tap, 1, 6)
