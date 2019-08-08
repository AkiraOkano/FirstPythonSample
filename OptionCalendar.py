'''
Created on 2019/06/03

@author: aokan

Option Profit/Loss
'''

from JapanOption import OkanoOption, Portfolio, setting
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style('darkgrid')

p = Portfolio(
"""
    07/C21250[-1]!336
    08/C21250[1]!473
    07/P21250[-1]!360
	08/P21250[1]!503
""")

x = np.arange(20000, 22500)  # グラフを描く�?囲(現�?産価格�?囲?�?
setting(21260, 15, 20190624)  # マ�?�ケ�?ト情報1?�?IV26?�?と仮定�?
fig, ax = plt.subplots(2, 1)
ax[0].plot(x, np.vectorize(p.v)(x), label='Ratio_June24')

setting(evaluationDate=20190630)  # 日付を7日に経過させたものもグラフ描画
ax[0].plot(x, np.vectorize(p.v)(x), label='Ratio_June30')
setting(evaluationDate=20190707)  # 日付を7日に経過させたものもグラフ描画
ax[0].plot(x, np.vectorize(p.v)(x), label='Ratio_July07')
ax[0].plot(x, np.vectorize(p.pay)(x), label='Payoff', linestyle="dashed")
ax[0].legend(loc="best")
# ax[0].axis('off')

data = []

for op, num in zip(p.items, p.nums):
    data.append(op.getGreeks(num))

subjects = ['δ', 'γ', 'θ', 'κ']

df = pd.DataFrame(data, columns=subjects)

df = df.append(df.sum(axis=0).rename('sum'))
print(df)

ax[1].axis('off')

tbl = ax[1].table(cellText=df.values,
               bbox=[0, 0, 1, 1],
               colLabels=df.columns,
               rowLabels=df.index, fontsize=10)
plt.show()

