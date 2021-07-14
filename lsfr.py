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


def print_periods(size):
    max_value = (1 << size) - 1

    print("Periods for %d taps" % size)

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
            print("taps: %s period: %s" % (bin(taps)[2:], period))


for p in range(1, 8):
    print_periods(p)
