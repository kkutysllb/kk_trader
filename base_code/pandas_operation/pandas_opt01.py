#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pandas as pd
import os
import datetime


pd.set_option('display.max_rows', 1000)  # 最大显示1000行数据
pd.set_option('display.max_columns', 10)  # 最大显示10列数据

"""
导入数据
"""
file_path = '../../test_data/sh600000.csv'

df = pd.read_csv(
    filepath_or_buffer=file_path,  # 导入文件的路径
    # sep=',',  # 数据之间的分隔符，导入csv文件时，默认"，"为分隔符，可以不写
    encoding='gbk',  # 解码方式，也是指文件编码格式
    # skiprows=1,  # 跳过第一行数据不读入
    nrows=15,  # 只读取前15行数据
    parse_dates=['交易日期'],  # 将指定列的数据识别为日期格式,
    index_col=['交易日期'],  # 将指定列设置为索引
    # usecols=['交易日期', '股票代码', '开盘价', '收盘价', '成交量'],  # 读取指定的这几列数据
    # error_bad_lines=False,  # 当某行数据有问题时，会报错，设置为False不报错，直接跳过
    # na_values='NULL'  # 将数据中的null识别为空值
)


"""
查看数据
"""
print(df.shape)  # shape属性表示输出df有多少行多少列，返回一个元组
print(df.columns)  # columns属性表示输出df的所有列名，返回一个列表，可以循环遍历
# for col in df.columns:
#     print(col)
print(df.index)  # index属性表示输出每一行的索引，返回一个列表，可以循环遍历
# for row in df.index:
#     print(row)
print(df.dtypes)  # dtypes属性表示输出每一列的数据类型，返回一个列表，可以循环遍历
# for obj in df.dtypes:
#     print(obj)
print(df.head(3))  # head()方法表示输出前n行数据，默认是5
print(df.tail())  # tail()方法表述输出后n行数据，默认是5
print(df.sample())  # sample()方法表示输出随机n行数据，默认是1
print(df.describe())  # describe()方法表示针对列输出整个数据的统计，行索引变为各项统计值，列索引不变
