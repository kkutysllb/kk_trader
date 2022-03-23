#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import numpy as np


"""
数组与矩阵的运算
"""
# 创建一个随机的数组
arr1 = np.random.randn(10)  # 创建一个长度为10的一维数组，元素符合正态分布
arr2 = np.random.randint(10)  # 创建一个1-10的随机整数，size参数不指定时
arr3 = np.random.randint(10, size=(2, 3))  # 通过size参数可以指定数组行列的数目
arr4 = np.random.randint(10, size=20)  # size参数指定一个数时，创建一个该长度的一维数组
arr5 = arr4.reshape(4, 5)  # 可以通过reshape()方法将一维数组变为多维，参数代表行列的数目

# 数组的运算
a = np.random.randint(1, 10, size=20).reshape(4, 5)
b = np.random.randint(1, 10, size=20).reshape(4, 5)

print(a + b)  # 加法
print(a - b)  # 减法
print(a * b)  # 点乘
print(a / b)  # 除法

# 矩阵的运算
A = np.mat(a)  # 将数组a转换为矩阵c,mat()方法创建矩阵，也可以将列表或数组转换为矩阵
B = np.mat(b)

print(A + B)  # 加法

# array常用的函数
print(np.unique(a))  # 返回数组a中的唯一的元素列表
print(sum(a))  # 对数组每一列求和，返回一个列表
print(sum(a[0]))  # 对数组第一行求和
print(sum(a[:, 1]))  # 对数组第二列求和
print(a.max())  # 取数组最大的值
print(max(a[0]))  # 取数组第一行的最大值
print(max(a[:, 1]))  # 取数组第二列的最大值


