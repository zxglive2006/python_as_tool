# encoding: UTF-8
import pandas as pd
import numpy as np
import candle as cd
import matplotlib.pyplot as plt


# shzheng = pd.read_csv(r'data\problem27-1.csv', index_col='date')
# shzheng.index.name = 'Date'
# shzheng.index = pd.to_datetime(shzheng.index, format='%Y-%m-%d')
# shzheng13 = shzheng['2013-03-01':'2013-05-31'].copy()
# cd.candleVolume(shzheng13, candletitle='上证指数', bartitle='成交量')

shzheng = pd.read_csv('data\problem27-2.csv', index_col='date')
shzheng.index.name = 'Date'
shzheng.index = pd.to_datetime(shzheng.index, format='%Y-%m-%d')
shzheng131 = shzheng['2013-01-01':'2013-06-30'].copy()
CL_OP = shzheng131.Close - shzheng131.Open
print(CL_OP.describe())
Doji = pd.Series(np.where(np.abs(CL_OP.values) < 5, 1, 0), index=CL_OP.index)
print(Doji[Doji == 1].index)
cd.candlePlot(shzheng131, title='Candle Plot of Shanghai Composite Index')
