#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


from jqdatasdk import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jqdata_stocks.stock_data.get_stock_data as std
import datetime

auth('13609247807', 'Imscfg_2252')
pd.set_option('expand_frame_repr', False)


"""
简单周交易策略，周四买入，周一卖出
"""


def week_period_strategy(code, freq, start_date, end_date):
    """
    简单周交易策略，周四买入，周一卖出
    :param code: 股票代码
    :param freq: 时间周期
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    data = std.get_stock_price(code, start_date=start_date, end_date=end_date, freq=freq)
    # print(data)
    # exit()
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    # 整合信号
    data = compose_signal(data)
    # 删除多余的列
    data = data.drop(['buy_signal', 'sell_signal'], axis=1)
    # 计算单次收益率
    data = calculate_profit_pct(data)
    # 计算累计收益率
    data = calculate_cum_profit(data)
    # 计算最大回撤比
    data = calculate_max_drowdown(data, window=252)  # 窗口期取一年252天

    return data


# if __name__ == '__main__':
#     # df = week_period_strategy('601699.XSHG', 'daily', None, '2022-01-14')
#     # print(df)
#     # print(df.describe())
#
#     # 计算北方稀土, 五矿稀土，盛和资源近一年的最大回撤比
#     df1 = std.get_stock_price('600111.XSHG', start_date='2021-12-01', end_date=datetime.datetime.today(), freq='daily')
#     df2 = std.get_stock_price('000831.XSHE', start_date='2021-12-01', end_date=datetime.datetime.today(), freq='daily')
#     df3 = std.get_stock_price('600392.XSHG', start_date='2021-12-01', end_date=datetime.datetime.today(), freq='daily')
#     df1 = calculate_max_drowdown(df1, window=31)
#     df2 = calculate_max_drowdown(df2, window=31)
#     df3 = calculate_max_drowdown(df3, window=31)
#     df = pd.DataFrame()
#     df['600111'] = df1['max_drowdown']
#     df['000831'] = df2['max_drowdown']
#     df['600392'] = df3['max_drowdown']
#     df[['600111', '000831', '600392']].plot()
#     plt.show()
