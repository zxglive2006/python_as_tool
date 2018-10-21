# encoding: UTF-8
import pandas as pd
# import matplotlib.pyplot as plt

returns = pd.read_csv(r".\data\retdata.csv")
gsyh = returns.gsyh
# plt.hist(gsyh)
# plt.show()
print("数据的位置")
print(returns.zglt.mean())
print(returns.pfyh.mean())
print(returns.zglt.median())
print(returns.pfyh.median())
print(returns.zglt.mode())
print(returns.pfyh.mode())
print([returns.zglt.quantile(i) for i in (0.25, 0.75)])
print([returns.pfyh.quantile(i) for i in (0.25, 0.75)])
print("数据的离散度")
print(returns.zglt.max() - returns.zglt.min())
print(returns.zglt.mad())
print(returns.zglt.var())
print(returns.zglt.std())
print(returns.pfyh.max() - returns.pfyh.min())
print(returns.pfyh.mad())
print(returns.pfyh.var())
print(returns.pfyh.std())
