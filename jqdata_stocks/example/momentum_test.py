#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_strategy.momentum_strategy as mmt
import matplotlib.pyplot as plt

"""
作业：计算持股超过两个月的投资组合收益率
"""
stocks = ['600111.XSHG', '000831.XSHE', '600392.XSHG']
df = mmt.get_stocks_data(stocks=stocks, start_date='2021-01-01', end_date='2022-01-01', col_index=['date', 'close'])
returns_one = mmt.momentum(data_concat=df, shift_n=1)
returns_two = mmt.momentum(data_concat=df, shift_n=2)

print(returns_one, returns_two)

returns_one.plot()
returns_two.plot()
plt.legend(['returns_one', 'returns_two'])
plt.show()
