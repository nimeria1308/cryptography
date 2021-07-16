def get_pair(num):
    return (num % 26, num // 26)

def to_string(numbers):
    result = []
    for num in numbers:
        a, b = get_pair(num)
        result.append(a)
        result.append(b)

    return "".join([chr(ord('A') + n) for n in result])

print(to_string([375, 91, 352]))
