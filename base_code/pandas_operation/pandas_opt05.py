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
数据整理
"""
# 排序函数， sort_values()
print(df.sort_values(by=['交易日期'], ascending=0))  # 参数by指定基于哪列排序，ascending参数为0表示逆序，1表示顺序
print(df.sort_values(by=['股票代码', '交易日期'], ascending=[0, 1]))  # 基于多列同时排序，输入列表参数即可


# 两个df上下合并操作，append()函数
df1 = df.iloc[0:10][['股票代码', '交易日期', '开盘价', '收盘价', '成交量']]
print(df1)
df2 = df.iloc[5:15][['股票代码', '交易日期', '开盘价', '收盘价', '成交量']]
print(df2)
df3 = df1.append(df2, ignore_index=True)  # 参数ignore_index=True表示忽略原始索引，重新指定索引
print(df3)


# 数据去重，drop_duplicates()方法
df3.drop_duplicates(subset=['股票代码', '交易日期'],  # 参数subset表示按照哪几列去重，传入一个列表
                    keep='first',  # keep参数表示去重后保留上面还是下面一行的值，first表示上面一行，last表示下面一行，都不保留取值False
                    inplace=True)  # inplace=True表示去重后修改原数据，取值False表示去重后不修改原数据
print(df3)


# 其他方法
# reset_index()方法重置原来的数据的索引
df.reset_index(inplace=True,  # inplace表示是否替换原数据
               drop=True)  # drop参数表示是否删除原索引
# print(df)

# rename()方法重新对某些列命名
df.rename(columns={    # columns参数传入一个字典，字典的键是原列名，值是新命名的列名
    '收盘价': 'close',
    '开盘价': 'open',
    '最高价': 'high',
    '最低价': 'low',
    '成交量': 'volume',
    '成交额': 'money'
}, inplace=True)
print(df)


# 判断一个df是否为空，使用empty属性
print(df.empty)


# 将df数据转置，行变成列，使用T属性
print(df.T)


"""
字符串操作，与Python的字符串操作基本一致。后面通过.str属性引入Python字符串的基本方法及属性
"""
print(df['股票代码'].str[:2])  # 切片
print(df['股票代码'].str.upper())  # 全部转为大写
print(df['股票代码'].str.lower())  # 全部转为小写
print(df['股票代码'].str.strip())  # 字符串两边去空格
print(df['股票代码'].str.len())  # 求字符串的长度
print(df['股票代码'].str.replace('sh', 'XSHG'))  # 字符串替换
print(df['股票代码'].str.contains('kk'))  # 判断字符串中是否包含某个字符
