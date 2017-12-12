# ============================================================
#
# Student Name (as it appears on cuLearn): Robert Collier
# Student ID (9 digits in angle brackets): <123456789>
# Course Code (for this current semester): COMP1405A
#
# ============================================================

# Give every person an index:
# Kyle = 0, Emery = 1 ... Jules = 15

# Generate a string for each trait:
# Kyle(i=0) has no earring, so the character of string named earring at index 0 is '0'
# Emery(i=1) has earring, so the character of string named earring at index 1 is '1'
# earring = '0'+'1'+...+'1' = '0101110011001111'


from comp1405_f17_assistant_a4 import *

avaliable = '1111111111111111'

earring = '0101110011001111'
eyepatch = '1001110111101101'
glasses = '1101010111101101'
hair = '1000101101100011'
moustache = '1000010000000001'
pipe = '1101110011101101'
tatto = '1100110101110101'
tie = '0001010000000000'

def _get_char_at (_str:str, _index:int):
    i = 0
    c = None
    if i >= len(_str):
        return c
    for c in _str:
        if i =
        i+=1


def _inspect_trait (_trait:str, _id:int):
    pass

def _parse_id_to_name(_id:int):
    name = None
    if _id == 0:
        name = 'Kyle'
    elif _id == 1:
        name = 'Emery'
    elif _id == 2:
        name = 'Addison'
    elif _id == 3:
        name = 'Quinn'
    elif _id ==4:
        name = 'Shawn'
    elif _id ==5:
        name = 'Hunter'
    elif _id ==6:
        name = 'Monroe'
    elif _id ==7:
        name = 'Alex'
    elif _id ==8:
        name = 'Karter'
    elif _id ==9:
        name = 'Dakota'
    elif _id ==10:
        name = 'Chris'
    elif _id ==11:
        name = 'Kai'
    elif _id ==12:
        name = 'Harper'
    elif _id ==13:
        name = 'Gray'
    elif _id ==14:
        name = 'River'
    elif _id ==15:
        name = 'Jules'
    return name