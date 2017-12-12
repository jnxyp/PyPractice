# coding=utf-8
import random
import sys
import time

width = 75
height = 50
str_min_len = 5
str_max_len = 40
str_gen_min = 1
str_gen_max = 3
file_path = r'matrix.py'
space = ' '
output_mode = 'Std'
fps = 20

def shift_down(l1: list, space: str):
    l2 = [[space] * len(l1[0])] * len(l1)
    i = 1
    while i < len(l2):
        l2[i] = l1[i - 1]
        i += 1
    return l2


def gen_random_string(min_len: int, max_len: int, symbols: list):
    length = random.randint(min_len, max_len)
    s = ''
    while len(s) < length:
        s += random.choice(symbols)
    return s[0:length + 1]


def add_string(s: str, l: list):
    col = random.randint(0, len(l[0]) - 1)
    row = 0
    while row < len(s):
        l[row][col] = s[row]
        row += 1

with open(file_path, mode='r', encoding='utf-8') as f:
    symbols = f.read().replace(' ', '').split('\n')

matrix = [[space for y in range(width)] for x in range(height + str_max_len)]
while True:
    # Move down
    matrix = shift_down(matrix, space)
    # Add new strings
    for i in range(1, random.randint(str_gen_min, str_gen_max)):
        add_string(gen_random_string(str_min_len, str_max_len, symbols), matrix)
    s = ''
    for row in matrix:
        for c in row:
            s += c + ' '
        s += '\n'
    if output_mode == 'Std':
        sys.stdout.write(s + '\r')
    else:
        print(s)
    time.sleep(1 / fps)
