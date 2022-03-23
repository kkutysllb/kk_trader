#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pandas as pd
import os

pd.set_option('display.max_rows', 1000)  # 最大显示1000行数据
pd.set_option('display.max_columns', 10)  # 最大显示10列数据

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
如何选取指定的行，列
"""
print(df['收盘价'])  # 根据指定的列名来选取
print(df[['收盘价', '开盘价', '最高价']])  # 同时选取多列数据，根据列名列表来选取

# loc操作，根据label（columns和index的名字）来读取数据
print(df.loc['1999-11-17'])  # 根据某一行的index来读取某一行的数据
print(df.loc[['1999-11-17', '1999-11-18']])  # 通过传入多行的index（列表），获取多行的数据
print(df.loc['1999-11-10': '1999-11-21'])  # 通过切片传参，可以获取连续多行数据
print(df.loc['1999-11-10':'1999-11-20', '开盘价':'收盘价'])  # 通过传入两个切片参数（逗号分隔），可以同时获取连续多行的指定列范围数据
print(df.loc['1999-11-11', '收盘价'])  # 通过loc操作可以获取某一个元素的值
# print(df.at['1999-11-11', '收盘价'])  # 上述操作也可以通过at()方法实现，而且是推荐使用的方法，但是at()方法不能传递index作为参数


# iloc操作，通过position来读取数据
# 读取第一行数据
print(df.iloc[0])
# 读取第二行至第四行的数据(不含第四行）
print(df.iloc[1:3])
