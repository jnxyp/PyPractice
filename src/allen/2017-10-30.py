def add_spaces (s:str, length:int):
    length = length - len(s)
    return ' ' * (length - length // 2) + s + ' ' * (length // 2)

begin = 32
end = 127
line_len = 16
char_width = 4

for line_begin in range(begin, end, line_len):
    chrs, ascs = 'chr: ', 'asc: '
    for order in range(line_begin, line_begin + line_len):
        chrs = chrs + add_spaces(chr(order), char_width)
        ascs = ascs + add_spaces(str(order), char_width)
    print(chrs)
    print(ascs)