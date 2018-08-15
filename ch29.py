# encoding: UTF-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.width", 120)
# 设定字体类型，用于正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def rsi(price, period=6):
    clprcChange = price - price.shift(1)
    clprcChange = clprcChange.dropna()
    indexprc = clprcChange.index
    upPrc = pd.Series(0, index=indexprc)
    upPrc[clprcChange > 0] = clprcChange[clprcChange > 0]
    downPrc = pd.Series(0, index=indexprc)
    downPrc[clprcChange < 0] = -clprcChange[clprcChange < 0]
    rsidata = pd.concat([BOCMclp, clprcChange, upPrc, downPrc], axis=1)
    rsidata.columns = ['Close', 'PrcChange', 'upPrc', 'downPrc']
    rsidata.dropna(inplace=True)
    SMUP = []
    SMDOWN = []
    for i in range(period, len(upPrc) + 1):
        SMUP.append(np.mean(upPrc.values[(i - period):i], dtype=np.float32))
        SMDOWN.append(np.mean(downPrc.values[(i - period):i], dtype=np.float32))
    rsi = [100 * SMUP[i] / (SMUP[i] + SMDOWN[i]) for i in range(0, len(SMUP))]
    indexRsi = indexprc[(period - 1):]
    Rsi = pd.Series(rsi, index=indexRsi)
    return Rsi


BOCM = pd.read_csv(r'./data/BOCM.csv')
BOCM.index = BOCM.iloc[:, 1]
BOCM.index = pd.to_datetime(BOCM.index, format="%Y-%m-%d")
BOCM = BOCM.iloc[:, 2:]
# print(BOCM.tail())

BOCMclp = BOCM.Close
print(BOCMclp[0:4])
rsi6 = rsi(BOCMclp, 6)
rsi24 = rsi(BOCMclp, 24)
Sig1 = []
for i in rsi6:
    if i > 80:
        Sig1.append(-1)
    elif i < 20:
        Sig1.append(1)
    else:
        Sig1.append(0)
date1 = rsi6.index
Signal1 = pd.Series(Sig1, index=date1)
print(Signal1[Signal1 == 1].head())
print(Signal1[Signal1 == -1].head())
Signal2 = pd.Series(0, index=rsi24.index)
lagrsi6 = rsi6.shift(1)
lagrsi24 = rsi24.shift(1)
for i in rsi24.index:
    if rsi6[i] > rsi24[i] and lagrsi6[i] < lagrsi24[i]:
        Signal2[i] = 1
    elif rsi6[i] < rsi24[i] and lagrsi6[i] < lagrsi24[i]:
        Signal2[i] = -1
signal = Signal1 + Signal2
signal[signal >= 1] = 1
signal[signal <= -1] = -1
signal = signal.dropna()
# print(signal)

# plt.plot(Rsi6['2015-01-03':], label="Rsi6")
# plt.plot(Rsi24['2015-01-03':], label="Rsi24", color="red", linestyle='dashed')
# plt.title("RSI的黄金交叉与死亡交叉")
# plt.ylim(-10, 110)
# plt.legend()
#
# plt.show()
