# -*- coding: utf-8 -*-
'''
Created on 2017-9-12

@author: jn_xyp
'''


def 计算差异(输入列表):
    if len(输入列表) <= 1:
        return []
    i = 0
    输出列表 = []
    while i < len(输入列表) - 1:
        输出列表.append(输入列表[i + 1] - 输入列表[i])
        i += 1
    return 输出列表


def 计算差异递归(输入二维列表):
    列表 = 输入二维列表[len(输入二维列表) - 1]
    i = 0
    while i < len(列表) - 1:
        if 列表[i] != 列表[i + 1]:
            输入二维列表.append(计算差异(列表))
            return 计算差异递归(输入二维列表)
        else:
            i += 1
    return 输入二维列表

输入Y值列表 = [input("Y values:").split(' ')]
输入Y值列表 = [[int(i) for i in 输入Y值列表[0]]]
结果 = 计算差异递归(输入Y值列表)
i = 0
while len(结果) > i:
    if (i == 0):
        print("y", end="")
    else:
        print(i, end="")
    j = 0
    while j < i:
        print("|\t", end="")
        j += 1
    for 值 in 结果[i]:
        print("|" + str(值) + "\t", end="")
    print("|")
    i += 1
input()