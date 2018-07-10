# encoding: UTF-8
import pandas as pd
import numpy as np
import candle as cd
import matplotlib.pyplot as plt


shzheng = pd.read_csv(r'data\problem27-1.csv', index_col='date')
shzheng.index.name = 'Date'
shzheng.index = pd.to_datetime(shzheng.index, format='%Y-%m-%d')
shzheng13 = shzheng['2013-03-01':'2013-05-31'].copy()
cd.candleVolume(shzheng13, candletitle='Candle Plot of Shanghai Composite Index', bartitle='volume')
