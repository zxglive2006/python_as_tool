# encoding: UTF-8
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 设置DataFrame显示宽度和列数
pd.set_option("display.width", 200)
pd.set_option('display.max_columns', 16)


if __name__ == '__main__':
    print("ch20")
    indexcd = pd.read_csv(r"./data/020/TRD_Index.csv", index_col="Trddt")
    mktcd = indexcd[indexcd.Indexcd==902]
    print(mktcd.head())
    mktret = pd.Series(mktcd.Retindex.values, index=pd.to_datetime(mktcd.index))
    mktret.name = "mktret"
    print(mktret.head())
    mktret = mktret["2014-01-02":"2014"]
    print(mktret.tail())
    xin_an = pd.read_csv(r"./data/020/xin_an.csv", index_col="Date")
    xin_an.index = pd.to_datetime(xin_an.index)
    print(xin_an.head())
    xin_an = xin_an[xin_an.Volume != 0]
    xin_anret = (xin_an.Close - xin_an.Close.shift(1)) / xin_an.Close.shift(1)
    xin_anret.name = "returns"
    xin_anret = xin_anret.dropna()
    print(xin_anret.head())
    print(xin_anret.tail())
    Ret = pd.merge(pd.DataFrame(mktret), pd.DataFrame(xin_anret),
                   left_index=True, right_index=True, how="inner")
    rf = 1.036 ** (1/360) - 1
    print(rf)
    Eret = Ret - rf
    print(Eret.head())
    plt.scatter(Eret.values[:,0], Eret.values[:,1])
    plt.title("XinAnGuFen return and market return")
    plt.show()
    model = sm.OLS(Eret.returns[1:], sm.add_constant(Eret.mktret[1:]))
    result = model.fit()
    print(result.summary())
