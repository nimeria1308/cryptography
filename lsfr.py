def pop_count(x):
    c = 0
    while x:
        if (x & 1):
            c += 1

        x >>= 1

    return c


def lsfr(coeffs, value, size):
    # generate mask
    mask = (1 << size) - 1

    # shift left
    new_value = (value << 1) & mask

    # find new bit
    new_value |= (pop_count(value & coeffs) % 2)

    return new_value


def find_period(coeffs, start_value, size):
    current = start_value
    t = 0
    previous = set([start_value])

    while True:
        current = lsfr(coeffs, current, size)
        t += 1

        if current in previous:
            break

        previous.add(current)

    return t


def find_coeffs_with_period(size):
    max_value = (1 << size) - 1
    results = {}

    for coeffs in range(1, max_value + 1):
        found_period = True
        period = find_period(coeffs, 1, size)

        if period:
            for start_value in range(2, max_value+1):
                p = find_period(coeffs, start_value, size)
                if p != period:
                    found_period = False
                    break
        else:
            found_period = False

        if found_period:
            results[coeffs] = period

    return results


def print_lsfr(coeffs, start_value, size):
    current = start_value
    period = find_period(coeffs, start_value, size)
    fmt = "period={:d} coeffs={:0%db}" % size
    print(fmt.format(period, coeffs))

    print("t  S")
    fmt = "{:2d} {:0%db}" % size
    for t in range(period + 1):
        print(fmt.format(t, current))
        current = lsfr(coeffs, current, size)
    print("")


all_coeffs = find_coeffs_with_period(6)
for coeffs, period in all_coeffs.items():
    print("coeffs={:06b} period={}".format(coeffs, period))

coeffs_21 = [coeffs for coeffs, period in all_coeffs.items() if period == 21]

for coeffs in coeffs_21:
    print_lsfr(coeffs, 1, 6)
