# -*- coding: utf-8 -*-
'''
Created on 2017-9-19

@author: jn_xyp
'''

from sympy import *

exp_str = input('Expression:')

x,y = symbols('x y')
exp = expand(exp_str.replace('y=','').replace('^', '**'))

deg = str(exp)
deg = deg.split('+')[0].split('-')
deg = deg[0].split('**')[-1]

print('Parent Function:y=x^' + deg)