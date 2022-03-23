#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pickle
import numpy as np


"""
使用pickle序列化numpy array
"""
x = np.arange(10)

# 将数组写入序列化文件
f = open('./x.pkl', 'wb')
pickle.dump(x, f)
f.close()

# 从序列化文件中读取数据
f = open('./x.pkl', 'rb')
a = pickle.load(f)
print(a)
f.close()

# numpy自身的序列化方法
np.save('./x_array', x)  # 写入x_array文件
b = np.load('./x_array.npy')   # 从x_array文件中读取数据
print(b)
np.savez('./multi_array.npz', a=x, b=x)  # 将多个数组压缩写入一个文件，savez()方法
c = np.load('./multi_array.npz')
print(c['a'])  # 读取时通过写入的key分别索引读取
print(c['b'])
