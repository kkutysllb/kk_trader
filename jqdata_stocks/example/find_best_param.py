#!/usr/bin/env python
# _*_ encoding: utf-8 _*_
# @Author: KkutysLLB


import jqdata_stocks.stock_data.get_stock_data as std
import jqdata_stocks.stock_strategy.ma_strategy as ma
import pandas as pd


"""
双均线策略寻找最优参数测试
"""
def ma_best_param(code, start_date, end_date):
    """
    双均线策略寻找最优参数测试，选取不同股票
    :param code: 股票代码
    :param start_date: 股票行情数据的起始日期，默认为None，表示股票的上市日期
    :param end_date: 股票行情数据的终止日期，默认为None，表示今天
    :return:
    """
    param = [3, 5, 10, 20, 30, 60, 100, 120, 250]
    res = []
    cum_profit = 0.0
    for short in param:
        for long in param:
            if short < long:
                # 从本地获取股票数据
                df = std.get_csv_price_data(code=code, start_date=start_date, end_date=end_date)
                # 调用双均线策略
                res_data = ma.tow_ma_strategy(data=df, short_window=short, long_window=long)
                # 删选策略最终收益值
                try:
                    cum_profit = res_data['cum_profit'].iloc[-1]
                except Exception:
                    pass
                # 将周期策略和最终收益存入列表res
                res.append([short, long, cum_profit])
    # 将res转换为DataFrame进行排序
    res_df = pd.DataFrame(res, columns=['short_wd', 'long_wd', 'cum_profit'])
    res_df = res_df.sort_values(by='cum_profit', ascending=0)  # 逆序排序
    return res_df


if __name__ == '__main__':
    code = '601012.XSHG'
    df_test = ma_best_param(code, start_date='2022-01-01', end_date='2022-01-14')
    print(df_test)