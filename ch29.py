# encoding: UTF-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.width", 120)
# 设定字体类型，用于正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

BOCM = pd.read_csv(r'./data/BOCM.csv')
BOCM.index = BOCM.iloc[:, 1]
BOCM.index = pd.to_datetime(BOCM.index, format="%Y-%m-%d")
BOCM = BOCM.iloc[:, 2:]
print(BOCM.head())

BOCMclp = BOCM.Close
clprcChange = BOCMclp - BOCMclp.shift(1)
clprcChange = clprcChange.dropna()
print(clprcChange.head(6))

indexprc = clprcChange.index
upPrc = pd.Series(0, index=indexprc)
upPrc[clprcChange > 0] = clprcChange[clprcChange > 0]
downPrc = pd.Series(0, index=indexprc)
downPrc[clprcChange < 0] = -clprcChange[clprcChange < 0]
rsidata = pd.concat([BOCMclp, clprcChange, upPrc, downPrc], axis=1)
rsidata.columns = ['Close', 'PrcChange', 'upPrc', 'downPrc']
rsidata.dropna(inplace=True)
print(rsidata.head(10))

SMUP = []
SMDOWN = []
for i in range(6, len(upPrc) + 1):
    SMUP.append(np.mean(upPrc.values[(i-6):i], dtype=np.float32))
    SMDOWN.append(np.mean(downPrc.values[(i-6):i], dtype=np.float32))
rsi6 = [100*SMUP[i]/(SMUP[i]+SMDOWN[i]) for i in range(0, len(SMUP))]
indexRsi = indexprc[5:]
Rsi6 = pd.Series(rsi6, index=indexRsi)
print(Rsi6.head())
print(Rsi6.describe())
