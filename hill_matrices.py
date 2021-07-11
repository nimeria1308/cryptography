count = 0

for a in range(26):
    for b in range(26):
        for c in range(26):
            for d in range(26):
                bc = b * c
                if (((((a * a) + bc) % 26) == 1) and
                        (((bc + (d * d)) % 26) == 1) and
                        ((((a * b) + (b * d)) % 26) == 0) and
                        ((((a * c) + (c * d)) % 26) == 0)):
                    count += 1

print(count)
