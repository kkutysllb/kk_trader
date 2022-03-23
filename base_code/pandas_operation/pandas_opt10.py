#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pandas as pd
import os

# pd.set_option('display.max_rows', 1000)  # 最大显示1000行数据
# pd.set_option('display.max_columns', 10)  # 最大显示10列数据
pd.set_option('expand_frame_repr', False)

file_path = '../../test_data/a_stock_201903.csv'

df = pd.read_csv(
    filepath_or_buffer=file_path,  # 导入文件的路径
    # sep=',',  # 数据之间的分隔符，导入csv文件时，默认"，"为分隔符，可以不写
    encoding='gbk',  # 解码方式，也是指文件编码格式
    # skiprows=1,  # 跳过第一行数据不读入
    # nrows=15,  # 只读取前15行数据
    # parse_dates=['交易日期'],  # 将指定列的数据识别为日期格式,
    # index_col=['交易日期'],  # 将指定列设置为索引
    # usecols=['交易日期', '股票代码', '开盘价', '收盘价', '成交量'],  # 读取指定的这几列数据
    # error_bad_lines=False,  # 当某行数据有问题时，会报错，设置为False不报错，直接跳过
    # na_values='NULL'  # 将数据中的null识别为空值
)


"""
分组操作
"""
# groupby()方法，根据交易日期进行group，将相同的交易日期的行放入同一个group
print(df.groupby('交易日期'))  # 生成一个group对象，不会做实质性的操作
print(df.groupby('交易日期').size())  # size()方法统计同一个group中的数据量大小，也就是行数

# 获取其中某一个group，通过get_group()方式实现
print(df.groupby('交易日期').get_group('2019-03-25'))
print(df.groupby('股票代码').get_group('sh600031'))

# 其他常见函数
print(df.groupby('股票代码').get_group('sh600031').describe())  # 针对分组进行统计
print(df.groupby('股票代码').head(3))  # 针对每一组取前三行
print(df.groupby('股票代码').tail(3))  # 针对每一组取后三行
print(df.groupby('股票代码').first())  # 针对每一组取第一行
print(df.groupby('股票代码').last())  # 针对每一组取最后一行
print(df.groupby('股票代码', as_index=False).nth(2))  # 针对每一组取任意一行，参数2表示取第二行, as_index表示是否采用分组作为index

# 分组计算
print(df.groupby('股票代码')['收盘价', '成交量'].mean())  # 对分组的收盘价和成交量计算平均值
print(df.groupby('股票代码')['收盘价', '成交量'].max())  # 对分组的收盘价和成交量计算最大值

# 遍历分组，通过遍历分组可以同时获取股票代码和其相关的所有数据
for code, group in df.groupby('股票代码'):
    print(code)
    print(group)
    exit()
