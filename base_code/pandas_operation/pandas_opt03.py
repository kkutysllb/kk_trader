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
    # parse_dates=['交易日期'],  # 将指定列的数据识别为日期格式,
    # index_col=['交易日期'],  # 将指定列设置为索引
    # usecols=['交易日期', '股票代码', '开盘价', '收盘价', '成交量'],  # 读取指定的这几列数据
    # error_bad_lines=False,  # 当某行数据有问题时，会报错，设置为False不报错，直接跳过
    # na_values='NULL'  # 将数据中的null识别为空值
)


"""
列操作
"""
# 行列的加减乘除操作
print(df['交易日期'] + ' 15:00:00')  # 字符串列可以直接加上字符串，对整列进行操作
print(df['收盘价'] * 100)  # 数字列可以直接加上或乘以数字，对整列进行操作
print(df['收盘价'] * df['成交量'])  # 两列之间可以直接操作
# 新增一列
df['交易日期new'] = df['交易日期'] + ' 15:00:00'
df['交易所'] = '中国A股沪深交易所'
print(df[['交易日期new', '交易所']])

# 统计函数
print(df['收盘价'].mean())  # mean()函数求取某列的平均值
print(df[['收盘价', '开盘价']].mean(axis=1))  # 也可以求取某几列的平均值, axis=1表示对整几列操作，axis=0表示对整几行操作
print(df[['最高价', '最低价']].mean(axis=1))
print(df['最高价'].max())  # max()方法求取某数字列的最大值
print(df['最低价'].min())  # min()函数求取某数字列的最小值
print(df['收盘价'].std())  # std()函数求取某数字列的标准差
print(df['收盘价'].count())  # count()方法求取某数字列中非空数值的个数
print(df['收盘价'].median())  # median()方法求取某数字列的中位数
print(df['收盘价'].quantile(0.5))  # quantline()方法求取某数字列的分为数，参数0.5表示50%分为数，也就是中位数


# shift类函数，删除列的方式
df['下周期收盘价'] = df['收盘价'].shift(-1)  # 通过shift()方法获取上移或下移的数据，参数为正表示下移，参数为负表示上移
print(df[['交易日期', '收盘价', '下周期收盘价']])
df['上周期收盘价'] = df['收盘价'].shift(1)
print(df[['交易日期', '收盘价', '上周期收盘价', '下周期收盘价']])
df['涨跌值'] = df['收盘价'].diff(1)  # diff()方法求取同列任意两行之间的差值，参数为正表示本行减去上面某行的值，参数为负则相反
print(df[['交易日期', '收盘价', '涨跌值']])
df.drop(['涨跌值', '交易所'], axis=1, inplace=True)  # drop()方法删除列操作，axis=1表示删除一整列，inplace=True表示替换原数据
print(df)
df['涨跌幅'] = df['收盘价'].pct_change(1)  # pc_change()自动计算涨跌幅方法
print(df[['收盘价', '涨跌幅']])


# cum类函数
df['累计成交量'] = df['成交量'].cumsum()  # cumsum()方法针对某数据列进行逐行累加
print(df[['成交量', '累计成交量']])
df['净值'] = (df['涨跌幅'] + 1).cumprod()  # cumprod()方法针对某数据列进行逐行累乘
print(df[['涨跌幅', '净值']])


# 其他列函数
# rank()方法进行排序
# ascending参数：排序方向选择，True从小到大，False从大到小
# pct参数：表示排名百分比，False表示不显示排名百分比，True表示显示排名百分比
df['涨跌幅排名'] = df['涨跌幅'].rank(ascending=True, pct=True)
print(df[['涨跌幅', '涨跌幅排名']])
