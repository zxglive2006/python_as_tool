# encoding: UTF-8
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy.stats as stats

pd.set_option("display.width", 240)
pd.set_option('display.max_columns', 8)

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号


def single_regression():
    TRD_Index = pd.read_csv(r'.\data\017\TRD_Index.txt', sep='\t')
    SHindex = TRD_Index[TRD_Index.Indexcd == 1]
    SZindex = TRD_Index[TRD_Index.Indexcd == 399106]
    SHRet = SHindex.Retindex
    SZRet = SZindex.Retindex
    SZRet.index = SHRet.index
    print(SHRet.head())
    model = sm.OLS(SHRet, sm.add_constant(SZRet)).fit()
    print(model.summary())
    print(model.fittedvalues[:5])
    # plt.scatter(model.fittedvalues, model.resid)
    # plt.xlabel('拟合值')
    # plt.ylabel('残差')
    # plt.show()
    # sm.qqplot(model.resid_pearson, stats.norm, line='45')
    plt.scatter(model.fittedvalues, model.resid_pearson**0.5)
    plt.ylabel('拟合值')
    plt.xlabel('标准化残差的平方根')


if __name__ == '__main__':
    print("ch17")
    single_regression()
