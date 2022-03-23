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
筛选数据，根据指定的条件，筛选出相关的数据
"""
print(df['股票代码'] == 'sh600000')
print(df[df['股票代码'] == 'sh600000'])  # 将满足条件的相关dataFrame输出
print(df[df['股票代码'] == 'sz000001'])
print(df[df['股票代码'] == 'sh600000'].index)
print(df[df['股票代码'].isin(['sh600000', 'sh600004', 'sz000001'])])  # isin()可以判断满足多个条件为真的结果
print(df[df['收盘价'] < 10])  # 输出收盘价小于10的行
print(df[(df['收盘价'] < 10) & (df['股票代码'] == 'sz300641')])  # 输出300641收盘价小于10的行


"""
空缺值处理
"""
# 创建缺失值
index = df[df['交易日期'] == '2019-03-01'].index  # 筛选出交易日期为2019-03-01的索引index
df.loc[index, '月标记'] = df['交易日期']  # 按照找出的索引index创建一列月标记，并且将相关交易日期值进行填充


# 删除缺失值
print(df.dropna(how='any'))  # 将带有空值的行删除，how='any'表示该行只要有一个值为空就删除
print(df.dropna(subset=['月标记', '收盘价'], how='all'))  # 只删除月标记和收盘价两列同时为空的行，all是与逻辑，any是或逻辑


# 补全缺失值
print(df.fillna(value=0))  # fillna()方法用于补全缺失值，value参数通过指定值进行补全
print(df.fillna(method='ffill'))  # method参数指定填充取值方向，ffill表示向上寻找最近的一个非空值替换，bfill表示向下寻找


# 找出缺失值
print(df.notnull())  # notnull()方法找出非空值，非空返回True，空返回False，反向函数isnull()
print(df[df['月标记'].notnull()])  # 找出月标记非空的行
