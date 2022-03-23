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
时间方法pd.to_datetime()方法
"""
# pd.to_datetime()方法可以将字符串日期转换为时间格式，也可以通过导入数据的parse_dates参数直接完成转换
print(df.at[0, '交易日期'])
print(type(df.at[0, '交易日期']))
df['交易日期'] = pd.to_datetime(df['交易日期'])
print(df.at[0, '交易日期'])
print(type(df.at[0, '交易日期']))

# pd.to_datetime()转变为日期格式后的相关属性通过.dt引入
print(df['交易日期'].dt.year)  # 输出这一天的年份
print(df['交易日期'].dt.month)  # 输出这一天的月份
print(df['交易日期'].dt.week)  # 输出这一天是一年中的第几周
print(df['交易日期'].dt.dayofyear)  # 输出这一天是一年中的第几天
print(df['交易日期'].dt.dayofweek)  # 输出这一天是周几
print(df['交易日期'].dt.weekday)  # 和上面一样，更加常用
print(df['交易日期'].dt.days_in_month)  # 输出这一天所在月份有多少天
print(df['交易日期'].dt.is_month_start)  # 判断这一天是否是所在月的开头
print(df['交易日期'].dt.is_month_end)  # 判断这一天是否是所在月的最后一天
print(df['交易日期'] + pd.Timedelta(days=1))  # 对交易日期加上一天，通过pd.Timedelta()函数实现，参数days表示天
print(df['交易日期'] + pd.Timedelta(hours=15))  # 对交易日期加上15个小时，参数hours表示小时，也可以通过增加分，秒


