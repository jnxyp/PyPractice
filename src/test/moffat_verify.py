def add_digits (num:str):
    sum = 0
    for d in num:
        sum += int(d)
    return sum

def verify (num:int):
    div5,div7 = True, True
    num = str(num)
    i = 0
    while i + 5 <= len(num):
        if add_digits(num[i:i+5]) % 5 != 0:
            div5 = False
            break
        i += 1
    i = 0
    while i + 7 <= len(num):
        if add_digits(num[i:i + 7]) % 4 != 0:
            div7 = False
            break
        i += 1
    return div5 and div7

nums = open('all_nums.txt').read().split(' ')
verified = []
for n in nums:
    if verify(int(n)):
        verified.append(n)

print(*verified, file=open('moffat.txt', 'w'))