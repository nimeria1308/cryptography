A_POS = ord("A")


def convert_char_to_int(c):
    return ord(c) - A_POS


def convert_int_to_char(i):
    return chr(i + A_POS)


def autokey(key, input_text, encode):
    output = []

    # convert key to range 0..25
    local_key = [convert_char_to_int(c) for c in key]

    # go over the input
    key_index = 0
    for c_in in input_text:
        # convert input to range 0..25
        c_in = convert_char_to_int(c_in)

        # key already in range 0..25
        z = local_key[key_index]

        # compute output
        c_out = (c_in + z if encode else c_in + 26 - z) % 26

        # write output
        output.append(convert_int_to_char(c_out))

        # store plain_text into key
        local_key[key_index] = c_in if encode else c_out

        # update current key position
        key_index = (key_index + 1) % len(key)

    return "".join(output)


key = "MAY"
plain_text = "THEPATHOFTHERIGHTEOUS"
cipher_text = autokey(key, plain_text, True)
plain_text_reconstructed = autokey(key, cipher_text, False)

print("%s -> %s -> %s" % (plain_text, cipher_text, plain_text_reconstructed))

print(autokey("GLAUBE", "GXILBGLQQJAIPWBMRKAZBWYKKKUCRKG", False))
