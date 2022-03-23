#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pandas as pd
import os

# pd.set_option('display.max_rows', 1000)  # 最大显示1000行数据
# pd.set_option('display.max_columns', 10)  # 最大显示10列数据
pd.set_option('expand_frame_repr', False)

file_path = '../../test_data/sh600000.csv'

df = pd.read_csv(
    filepath_or_buffer=file_path,  # 导入文件的路径
    # sep=',',  # 数据之间的分隔符，导入csv文件时，默认"，"为分隔符，可以不写
    encoding='gbk',  # 解码方式，也是指文件编码格式
    # skiprows=1,  # 跳过第一行数据不读入
    nrows=30,  # 只读取前30行数据
    parse_dates=['交易日期'],  # 将指定列的数据识别为日期格式,
    # index_col=['交易日期'],  # 将指定列设置为索引
    # usecols=['交易日期', '股票代码', '开盘价', '收盘价', '成交量'],  # 读取指定的这几列数据
    # error_bad_lines=False,  # 当某行数据有问题时，会报错，设置为False不报错，直接跳过
    # na_values='NULL'  # 将数据中的null识别为空值
)


"""
滚动操作
"""
# rolling(n)操作即为取值最近n行数据进行计算
# mean()平均值
# max()最大值
# min()最小值
# std()标准差，也就是方差
df['收盘价5天平均值'] = df['收盘价'].rolling(5).mean()
df['收盘价5天最大值'] = df['收盘价'].rolling(5).max()
df['收盘价5天最小值'] = df['收盘价'].rolling(5).min()
df['收盘价5天标准差'] = df['收盘价'].rolling(5).std()
print(df[['收盘价', '收盘价5天平均值', '收盘价5天最大值', '收盘价5天最小值', '收盘价5天标准差']])


# expanding()方法计算从第一行开始至最当前行的相关操作
# mean()平均值
# max()最大值
# min()最小值
# std()标准差，也就是方差
df['收盘价_至今平均值'] = df['收盘价'].expanding().mean()
df['收盘价_至今最大值'] = df['收盘价'].expanding().max()
df['收盘价_至今最小值'] = df['收盘价'].expanding().min()
df['收盘价_至今标准差'] = df['收盘价'].expanding().std()
print(df[['收盘价', '收盘价_至今平均值', '收盘价_至今最大值', '收盘价_至今最小值', '收盘价_至今标准差']])


"""
保存文件
"""
df.to_csv(file_path,  # 保存文件的路径
          encoding='utf-8',  # 保存文件格式编码设定
          index=False  # 保存文件时是否保留索引
          )