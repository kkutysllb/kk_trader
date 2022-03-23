#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import jqdata_stocks.stock_data.get_stock_data as std
import jqdata_stocks.stock_strategy.base as strat

"""
布林轨交易策略
计算公式:
中轨线（MID） = N 日的移动平均线
上轨线（UPPER） = 中轨线 + 两倍的标准差
下轨线（LOWER） = 中轨线 - 两倍的标准差

交易信号:
当天价格下穿（小于）下轨：买入
当天价格上穿（大于）上轨：卖出
"""


def boll_strategy(data, mid_window=10):
    """
    布林轨交易策略，生成交易信号，计算单次收益率和累计收益率
    :param data: DataFrame，股票行情数据
    :param mid_window: N日移动平均线时间窗口，默认为10日移动平均线
    :return:
    """
    data = pd.DataFrame(data)
    # 计算布林轨的值
    data['mid'] = data['close'].rolling(window=mid_window).mean()  # 中轨线
    data['upper'] = data['mid'] + (2 * data['mid'].std())  # 上轨线
    data['lower'] = data['mid'] - (2 * data['mid'].std())  # 下轨线

    # 生成交易信号
    data['buy_signal'] = np.where(data['close'] < data['lower'], 1, 0)
    data['sell_signal'] = np.where(data['close'] > data['upper'], -1, 0)

    # 整合信号
    data = strat.compose_signal(data)

    # 计算单次收益率
    data = strat.calculate_profit_pct(data)

    # 计算累计收益率
    data = strat.calculate_cum_profit(data)

    # 删除多余的列
    data = data.drop(labels=['buy_signal', 'sell_signal'], axis=1)

    # 数据预览
    # print(data[['close', 'upper', 'mid', 'lower', 'signal']])

    return data


if __name__ == '__main__':
    code = '600392.XSHG'
    df = std.get_csv_price_data(code=code, start_date='2022-01-01', end_date='2022-01-14')
    # 测试布林轨策略
    data_res = boll_strategy(data=df, mid_window=5)
    # data_res = data_res[data_res['signal'] != 0]
    print(data_res[['close', 'upper', 'mid', 'lower', 'signal', 'profit_pct', 'cum_profit']])