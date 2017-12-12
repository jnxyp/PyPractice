# If only using if......
def _to_word(_in:int):
    _first = _in // 100
    _third = _in % 10
    _second = (_in % 100 - _third) / 10
    _out = ''
    if _first != 0:
        _out += _parse_single(_first) + ' hundred '
        if _second != 0 or _third != 0:
            _out += 'and '
    # xxxteen
    if _second == 1 and _third != 0:
        if _third == 1:
            _out += 'eleven'
        elif _third == 2:
            _out += 'twelve'
        elif _third == 3:
            _out += 'thirteen'
        elif _third == 4:
            _out += 'fourteen'
        elif _third == 5:
            _out += 'fifteen'
        elif _third == 6:
            _out += 'sixteen'
        elif _third == 7:
            _out += 'seventeen'
        elif _third == 8:
            _out += 'eighteen'
        elif _third == 9:
            _out += 'nineteen'
    elif _second == 1 and _third != 0:
        if _third == 1:
            _out += 'eleven'
        elif _third == 2:
            _out += 'twelve'
        elif _third == 3:
            _out += 'thirteen'
        elif _third == 4:
            _out += 'fourteen'
        elif _third == 5:
            _out += 'fifteen'
        elif _third == 6:
            _out += 'sixteen'
        elif _third == 7:
            _out += 'seventeen'
        elif _third == 8:
            _out += 'eighteen'
        elif _third == 9:
            _out += 'nineteen'

def _parse_single(_in:int):
    if _in == 1:
        return 'one'
    elif _in == 2:
        return 'two'
    elif _in == 3:
        return 'three'
    elif _in == 4:
        return 'four'
    elif _in == 5:
        return 'five'
    elif _in == 6:
        return 'six'
    elif _in == 7:
        return 'seven'
    elif _in == 8:
        return 'eight'
    elif _in == 9:
        return 'nine'