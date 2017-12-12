# coding=utf-8

def a(b:int):
    pass

import inspect

print(inspect.getfullargspec(a))