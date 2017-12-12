'''def get_input():
    str_in = ''
    temp = ''
    while '''
a = '12222 212112  212     21'

def split(str:str,sep:str = ' ',no_empty: bool = True):
    l = []
    temp = ''
    for s in str:
        print(s,temp)
        if s == sep:
            if not no_empty or temp != '':
                l.append(temp)
                temp = ''
        else:
            temp += s
    l.append(temp)
    return l

print(split(a))