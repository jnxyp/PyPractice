# coding=utf-8
import math as m
from functools import reduce

f, x_coord = lambda x:m.cos(x/5)*10,range(-100,100);y_coord = [f(v) for v in x_coord];g = [' ' * m.floor((y - min(y_coord)) // 1) + '#' + ' ' * m.ceil(max(y_coord) - y) + '\n' for y in y_coord];print(*g)

# f_s, x_coord = [lambda x: m.cos(x / 5) * 10], range(-100, 100);
# y_coords = [f(v) for f in f_s for v in x_coord];
# g = [[False] * len(x_coord)] * reduce(m.max, y_coords)
#
#
# print(*g)