#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


from jqdatasdk import *
import pandas as pd
import os
import matplotlib.pyplot as plt

auth('13609247807', 'Imscfg_2252')
pd.set_option('expand_frame_repr', False)

"""
获取股票行情数据
"""
# 获取A股市场所有股票代码
# stock_list = list(get_all_securities(types=['stock']).index)

# 获取某只股票的日k行情数据
code = '600111.XSHG'
# daily_data = get_price(security=code,
#                        frequency='daily',
#                        start_date='2021-12-01',
#                        end_date='2021-12-31',
#                        panel=False  # 取值false表示输出一个dataframe数据
#                        )

# 通过日k行情数据转换为周k行情数据
# week_data = pd.DataFrame()
# rule = '1W'
#
# week_data['open'] = daily_data['open'].resample(rule=rule, closed='right', label='right').first()
# week_data['close'] = daily_data['close'].resample(rule=rule, closed='right', label='right').last()
# week_data['high'] = daily_data['high'].resample(rule=rule, closed='right', label='right').max()
# week_data['low'] = daily_data['low'].resample(rule=rule, closed='right', label='right').min()
# week_data['volume'] = daily_data['volume'].resample(rule=rule, closed='right', label='right').sum()
# week_data['money'] = daily_data['money'].resample(rule=rule, closed='right', label='right').sum()


"""
获取股票财务指标
"""
# df = get_fundamentals(query(indicator), statDate='2021q3')
# df.index = df['code']  # 设置股票代码为索引index

# 按照每股收益(eps)，净资产收益率(roe)，经营活动净收益(operating_profit)，营业利润同比增长率(inc_operation_profit_year_on_year)筛选
# df = df[(df['eps'] > 0.5) & (df['roe'] > 2) & (df['inc_operation_profit_year_on_year'] > 100) & (df['operating_profit'] > 2460984529)]
# df.to_csv('../../test_data/indicator_2021q3_stock.csv', encoding='utf-8')


"""
获取股票估值指标
"""
# df_valuation = get_fundamentals(query(valuation), statDate='2021q3')
# df_valuation.index = df_valuation['code']
# df['pe_ratio'] = df_valuation['pe_ratio']
# df = df[df['pe_ratio'] < 30]
# df.to_csv('../../test_data/indicator_2021q3_stock.csv', encoding='utf-8')


"""
获取其他周期股票行情数据
get_bars()方法
时间周期的行情数据（支持时间周期：'1m','5m', '15m', '30m', '60m', '120m', '1w', '1M'）
"""
period_df = get_bars(security=code,  # 股票代码
                     count=16,  # 获取的时间周期数据个数，本例取15分钟周期，所以一天就是16个周期
                     unit='15m',  # 时间周期单位，取值如上描述所示
                     fields=['date', 'open', 'close', 'high', 'low', 'volume', 'money'],  # 返回数据包含的字段
                     end_dt='2022-01-12'  # 数据获取截止时间
                     )
print(period_df)
