#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB

import jqdata_stocks.stock_data.get_stock_data as std
import jqdata_stocks.stock_strategy.base as strat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
双均线策略
"""


def tow_ma_strategy(data, short_window=5, long_window=20):
    """
    双均线策略
    :param data: DataFrame，股票行情数据，从本地获取也可从jq网站获取
    :param short_window: 短的时间窗口，默认为5，表示5日均线
    :param long_window: 长的时间窗口，默认为20，表示20日均线
    :return:
    """
    data = pd.DataFrame(data)
    print('============== 当前时间周期对: ', short_window, long_window)
    # 计算时间窗口的均值
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()

    # 计算交易策略，生成信号：金叉-买入，死叉-卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)
    # print(data)

    # 整合信号
    data = strat.compose_signal(data)

    # 计算单次收益
    data = strat.calculate_profit_pct(data)

    # 计算累计收益
    data = strat.calculate_cum_profit(data)

    # 删除多余的列
    data = data.drop(labels=['buy_signal', 'sell_signal'], axis=1)

    # 数据预览
    print(data[['close', 'short_ma', 'long_ma', 'signal', 'cum_profit']])

    return data


if __name__ == '__main__':
    # code = '000001.XSHE'
    # df = std.get_csv_price_data(code=code, start_date='2020-01-01', end_date='2021-01-01')
    # df = tow_ma_strategy(df)
    # df = df[df['signal'] != 0]
    # print('开仓次数: ', len(df))
    # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])
    # print(df)
    stocks = ['600111.XSHG', '601012.XSHG', '002594.XSHE']
    cum_profits = pd.DataFrame()
    for code in stocks:
        # 从本地数据库获取股票行情数据
        df = std.get_csv_price_data(code=code, start_date='2021-01-01', end_date='2022-01-01')
        # df = std.get_stock_price(code=code, freq='daily', start_date='2016-01-01', end_date='2022-01-01')
        # 按照5日，10日均线的双均线策略生成交易信号
        df = tow_ma_strategy(df)
        # 存储累计收益
        cum_profits[code] = df['cum_profit'].reset_index(drop=True)
        # 画出每个股票累计收益率折线图
        df['cum_profit'].plot(label=code)
        print('开仓次数: ', len(df))
    print(cum_profits)

    plt.title('Compora of MA Strategy Profits')
    plt.legend()
    plt.show()