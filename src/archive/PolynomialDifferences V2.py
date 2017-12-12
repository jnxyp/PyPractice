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


def 生成表格(表达式, 从, 到, 步进):
    x, y = [], []
    while 从 <= 到:
        x.append(从)
        y.append(eval(表达式.replace("x", "(" + str(从) + ")")))
        从 += 步进
    return [x, y]


输入表达式 = [input("Expression:"), input("From:"), input("To:"), input("Step:")]
结果 = 计算差异递归(生成表格(输入表达式[0].replace("y=", "").replace("^", "**"), int(输入表达式[1]),
                 int(输入表达式[2]), int(输入表达式[3])))
i = 0
while len(结果) > i:
    if i == 0:
        print("x", end="")
    elif (i == 1):
        print("y", end="")
    else:
        print(i - 1, end="")
    j = 0
    while j < i - 1:
        print("|\t", end="")
        j += 1
    for 值 in 结果[i]:
        print("|" + str(值) + "\t", end="")
    print("|")
    i += 1
input()