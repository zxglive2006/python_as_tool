# encoding: UTF-8
import pandas as pd
import ffn

# 设置DataFrame显示宽度和列数
pd.set_option("display.width", 200)
pd.set_option('display.max_columns', 16)


def cal_simple_return():
    stock = pd.read_csv(r"./data/stockszA.csv", index_col="Trddt")
    Vanke = stock[stock.Stkcd == 2]
    close = Vanke.Clsprc
    close.index = pd.to_datetime(close.index)
    close.index.name = "Date"
    print(close.head())
    lagclose = close.shift(1)
    print(lagclose.head())
    Calclose = pd.DataFrame({'close':close, 'lagclose':lagclose})
    print(Calclose.head())
    simpleret = (close - lagclose) / lagclose
    simpleret.name = 'simpleret'
    print(simpleret.head())
    calret = pd.merge(Calclose, pd.DataFrame(simpleret), left_index=True, right_index=True)
    simpleret2 = (close - close.shift(2)) / close.shift(2)
    simpleret2.name = 'simpleret2'
    calret['simpleret2'] = simpleret2
    print(calret.head())
    print(calret.iloc[5,:])
    ffnSimpleret = ffn.to_returns(close)
    ffnSimpleret.name = 'ffnSimpleret'
    print(ffnSimpleret.head())


if __name__ == '__main__':
    print("ch18")
    cal_simple_return()
