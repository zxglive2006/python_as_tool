# encoding: UTF-8
from scipy import stats
import numpy as np
import pandas as pd

# pd.set_option("display.width", 240)
pd.set_option('display.max_columns', 8)

x = [10.1, 10, 9.8, 10.5, 9.7, 10.1, 9.9, 10.2, 10.3, 9.9]
print(stats.t.interval(0.95, len(x) - 1, np.mean(x), stats.sem(x)))
SHindex = pd.read_csv(r".\data\TRD_Index.csv")
print(SHindex.head(3))
