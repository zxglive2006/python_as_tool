# encoding: UTF-8
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 设置DataFrame显示宽度和列数
pd.set_option("display.width", 120)
pd.set_option('display.max_columns', 16)


def show_hxthrfac():
    plt.subplot(2, 2, 1)
    plt.scatter(HXThrFac.HXRet, HXThrFac.RiskPremium2)
    plt.subplot(2, 2, 2)
    plt.scatter(HXThrFac.HXRet, HXThrFac.SMB2)
    plt.subplot(2, 2, 3)
    plt.scatter(HXThrFac.HXRet, HXThrFac.HML2)
    plt.show()


if __name__ == '__main__':
    print("ch21")
    stock = pd.read_csv(r"./data/021/stock.txt", sep="\t", index_col="Trddt")
    print(stock.head(n=3))
    HSBank = stock[stock.Stkcd == 600015]
    print(HSBank.head(n=3))
    HSBank.index = pd.to_datetime(HSBank.index)
    HXRet = HSBank.Dretwd
    HXRet.name = 'HXRet'
    print("HXRet head")
    print(HXRet.head())
    print("HXRet tail")
    print(HXRet.tail())
    # HSRet.plot()
    # plt.show()
    ThreeFactors = pd.read_csv(r"./data/021/ThreeFactors.txt", sep="\t", index_col="TradingDate")
    print(ThreeFactors.head(n=3))
    ThreeFactors.index = pd.to_datetime(ThreeFactors.index)
    ThrFac = ThreeFactors["2014-01-02":]
    ThrFac = ThrFac.iloc[:, [2, 4, 6]]
    print(ThrFac.head())
    HXThrFac = pd.merge(pd.DataFrame(HXRet), pd.DataFrame(ThrFac), left_index=True, right_index=True)
    print(HXThrFac.head(n=3))
    print(HXThrFac.tail(n=3))
    regThrFac = sm.OLS(HXThrFac.HXRet, sm.add_constant(HXThrFac.iloc[:, 1:4]))
    result = regThrFac.fit()
    print(result.summary())
    print(result.params)