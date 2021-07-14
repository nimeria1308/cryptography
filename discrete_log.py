def log2_discrete(value, period):
    n = 0
    while True:
        if (1 << n) % period == value:
            return n
        n += 1


print(log2_discrete(66, 101))
