#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


from jqdatasdk import *
import pandas as pd
import numpy as np

auth('15619292819', 'Oms_2600')
pd.set_option('expand_frame_repr', False)

"""
基础策略
"""


def evaluate_strategy(data):
    """
    评估策略收益情况：总收益率，年化收益率，最大回撤，夏普比率
    :param data: DataFrame，包含单次收益率的data
    :return: data, DataFrame，包含总收益率，年化收益率，最大回撤，夏普比率等键值对
    """
    data = calculate_cum_profit(data)

    # 计算总收益率
    total_return = data['cum_profit'].iloc[-1]

    # 计算年化收益率
    annual_return = data['profit_pct'].mean() * 12

    data = calculate_max_drawdown(data, window=12)

    # 计算近一年最大回撤
    max_drawdown = data['max_drawdown'].iloc[-1]

    # 计算夏普比率
    sharpe, annual_sharpe = calculate_sharpe(data, window=12)

    # 返回数据
    results = {
        '总收益率: ': total_return,
        '年化收益率: ': annual_return,
        '最大回撤: ': max_drawdown,
        '夏普比率: ': annual_sharpe
    }

    # 数据预览
    for key, value in results.items():
        print(key, value)
    return data


def compose_signal(data):
    """
    整合信号
    :param data:
    :return:
    """
    # 整合信号，剔除重复信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def calculate_profit_pct(data):
    """
    计算单次收益率
    :param data:
    :return:
    """
    # 计算收益率
    data.loc[data['signal'] != 0, 'profit_pct'] = data[data['signal'] != 0]['close'].pct_change()
    data = data[data['signal'] == -1]
    return data


def calculate_cum_profit(data):
    """
    计算累计收益率
    :param data:
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def calculate_protfolio_profit(data, signal, n_stock):
    """
    计算投资组合累计收益率（等权重）
    :param data: DataFrame, 投资组合标的各累计收益率统计
    :param signal: 交易信号
    :param n_stock: 标的个数
    :return: prot_result, DataFrame
    """
    # 拷贝数据
    prot_result = data.copy()

    # 计算单次收益率
    prot_result['profit_pct'] = (signal * prot_result.shift(-1)).T.sum() / n_stock

    # 计算累计收益率
    prot_result = calculate_cum_profit(prot_result)
    return prot_result.shift(1)


def calculate_max_drawdown(data, window):
    """
    计算最大回撤比
    :param data: 股票行情数据
    :param window: 要统计的时间窗口值
    :return:
    """
    # 模拟持仓值
    data['close'] = 1 + data['cum_profit']
    # 计算窗口期的最大净值
    data['max_net_value'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算每一天的回撤
    data['close_drawdown'] = data['close'] / data['max_net_value'] - 1
    # 计算最大回撤比
    data['max_drawdown'] = data['close_drawdown'].rolling(window=window, min_periods=1).min()
    return data


def calculate_sharpe(data, window=252):
    """
    计算夏普比率
    :param data: 股票行情数据
    :param window: 要统计的时间窗口值, 默认年化为252个交易日
    :return:
    """
    # 获取股票的每天回报率，按照收盘价计算
    daily_return = data['profit_pct']

    # 计算股票的回报率均值
    avg_return = daily_return.mean()

    # 计算股票回报率标准差
    std_return = daily_return.std()

    # 计算夏普比率
    sharpe = avg_return / std_return
    sharpe_year = sharpe * np.sqrt(window)
    return sharpe, sharpe_year
