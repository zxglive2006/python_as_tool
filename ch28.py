# encoding: UTF-8
import pandas as pd
import matplotlib.pyplot as plt


def momentum(price, period):
    lagPrice = price.shift(period)
    momen = price - lagPrice
    momen.dropna(inplace=True)
    return momen


pd.set_option("display.width", 120)
# 设定字体类型，用于正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


Vanke = pd.read_csv(r"data\Vanke.csv")
Vanke.index = Vanke.iloc[:, 1]
Vanke.index = pd.to_datetime(Vanke.index, format="%Y-%m-%d")
Vanke = Vanke.iloc[:, 2:].copy()
print(Vanke.head(10))
Close = Vanke.Close
# print(Close.describe())
lag5Close = Close.shift(5)
print(lag5Close.head(10))
monmentum5 = Close - lag5Close
print(monmentum5.tail())
Momen5 = Close/lag5Close - 1
Momen5.dropna(inplace=True)
print(Momen5[:5])
print(momentum(Close, 5).tail())

# plt.subplot(211)
# plt.plot(Close, "b*")
# plt.xlabel('date')
# plt.ylabel('Close')
# plt.title('万科股份5日动量图')
#
# plt.subplot(212)
# plt.plot(monmentum5, "r-*")
# plt.xlabel('date')
# plt.ylabel('Momentum5')
#
# plt.show()
