#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import numpy as np


"""
数组的创建，元素的访问，数组的基本属性
"""
# 从list创建array
lst_1 = [1, 2, 3, 4]
print(np.array(lst_1))  # 创建一维数组
lst_2 = [5, 6, 7, 8]
print(np.array([lst_1, lst_2]))  # 创建二维数组
arr1 = np.array([lst_1, lst_2])
print(arr1.shape)  # shape属性表示数组的形状，输出（2，4）表示2行4列
print(arr1.size)  # size属性表示数组的元素个数
print(arr1.dtype)  # dtype属性表示数组元素的数据类型
arr2 = np.array([['a', 'b', 'c'], [1, 2, 3]])
print(arr2.dtype)
arr3 = np.array([[1.0, 2, 3.0], [2.0, 4, 5.6]])
print(arr3.dtype)

# 通过numpy的方法创建array
arr4 = np.arange(1, 10, 2)
arr5 = np.zeros(5)  # 创建一维全零矩阵
arr6 = np.zeros([2, 3])  # 创建二维全零矩阵
arr7 = np.eye(5)  # 创建单位矩阵

# 数组元素访问
print(arr4[2])  # 一维数组访问类似列表操作，通过下标访问
print(arr4[2:])
print(arr1[0][2])  # 二维数组访问通过双下标操作，第一个下标表示行，第二个下标表示列
print(arr1[1][:])
print(arr1[0, 2])  # 也可以通过一个两个元素的列表访问，第一个元素表示行，第二个元素表示列
print(arr1[1, :])

