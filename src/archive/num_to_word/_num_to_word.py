def _fmt_int (_int,_exp_len):
    _int = str(_int)
    while len(_int) != _exp_len:
        if len(_int) < _exp_len:
            _int = '0' + _int
        else:
            _int = _int[0:-1]
    return _int

# numin = _fmt_int(input('Number to convert (3-digit):'), 3)

def _num_to_word (_num_in):
    _num_in = _fmt_int(_num_in, 3)
    _word_out = ''
    # Words 0-9
    dict1 = {'0': '', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven',
             '8': 'eight', '9': 'nine'}
    # Words 11-19
    dict2 = {'11': 'eleven', '12': 'twelve', '13': 'thirteen', '14': 'fourteen', '15': 'fifteen', '16': 'sixteen',
             '17': 'seventeen', '18': 'eighteen', '19': 'nineteen'}
    # Words 10-90
    dict3 = {'10': 'ten', '20': 'twenty', '30': 'thirty', '40': 'forty', '50': 'fifty', '60': 'sixty', '70': 'seventy',
             '80': 'eighty','90': 'ninety'}
    # First digit
    if _num_in == '000':
        _word_out += 'zero'
    else:
        if _num_in[0] != '0':
            _word_out += dict1.get(_num_in[0])
            _word_out += ' hundred '
            if _num_in[1:] != '00':
                _word_out += 'and '
        # Second and third digits
        if _num_in[1:] in dict2:
            _word_out += dict2.get(_num_in[1:])
        elif _num_in[1:] in dict3:
            _word_out += dict3.get(_num_in[1:])
        else:
            if _num_in[1] + '0' in dict3:
                _word_out += dict3.get(_num_in[1] + '0')
                _word_out += '-'
            _word_out += dict1.get(_num_in[2])
    return 'if _in == ' + str(int(_num_in)) + ':\n    print(\''+_word_out + '\')'

i = 0
while i <1000:
    print(_num_to_word(i))
    i += 1

