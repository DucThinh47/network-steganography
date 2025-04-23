def text_to_bit_groups(message):
    bitstream = ''.join(format(ord(c), '08b') for c in message)
    groups = [bitstream[i:i+3] for i in range(0, len(bitstream), 3)]
    if len(groups[-1]) < 3:
        groups[-1] = groups[-1].ljust(3, '0')
    return groups


groups = text_to_bit_groups("hi")
print(groups)

