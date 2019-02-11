# encoding: UTF-8
import pandas as pd

history = pd.read_csv(r".\exercise_data\history.csv")
print(history.head())

print("Emerging.Markets statistics data")
print(history["Emerging.Markets"].mean())
print(history["Emerging.Markets"].median())
print(history["Emerging.Markets"].mode())
print([history["Emerging.Markets"].quantile(i) for i in (0.1, 0.9)])
