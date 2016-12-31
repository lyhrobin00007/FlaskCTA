# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:28:57 2016

@author: 024536
"""

import sys
sys.path.append('D:\\Code\\github\\vnpy\\vn.trader\\ctaAlgo\\')
sys.path.append('D:\\Code\\github\\vnpy\\vn.trader\\')
sys.path.append('D:\\Code\\github\\FlaskCTA\data\\')

from ctaBacktesting import BacktestingEngine

def ctaBacktestingRun(username, strategyName, 
        setting = {"dbName":'VnTrader_1Min_Db',
                   "symbol":"IF0000",
                   "setStartDate":'20160101',
                   "setEndDate":'',
                   "setInitDays":10,
                   "setSlippage":0.2,
                   "setRate":0.3/10000,
                   "setSize":300}):
    
    # 创建回测引擎
    engine = BacktestingEngine()
    
    # 设置引擎的回测模式为K线
    engine.setBacktestingMode(engine.BAR_MODE)

    # 设置回测用的数据起始日期
    engine.setStartDate(setting['setStartDate'], setting['setInitDays'])
    engine.setEndDate(setting['setEndDate'])
    
    # 载入历史数据到引擎中
    engine.setDatabase(setting['dbName'], setting['symbol'])
    
    # 设置产品相关参数
    engine.setSlippage(setting['setSlippage'])     # 股指1跳
    engine.setRate(setting['setRate'])   # 万0.3
    engine.setSize(setting['setSize'])         # 股指合约大小    
    
    # 在引擎中创建策略对象
    importstring = "from strategy.%s.%s import %s as strategyClass"%(username,strategyName,strategyName)
    exec importstring
    engine.initStrategy(strategyClass, {})
    
    # 开始跑回测
    engine.runBacktesting()
    
    # 显示回测结果
    # spyder或者ipython notebook中运行时，会弹出盈亏曲线图
    # 直接在cmd中回测则只会打印一些回测数值
#    engine.showBacktestingResult()
    d = engine.calculateBacktestingResult()

    return d

if __name__ == "__main__":
    d = ctaBacktestingRun("lyhrobin00007","DoubleEmaDemo")