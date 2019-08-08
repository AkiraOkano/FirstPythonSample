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
    06/C22000[1]!210
    06/C22125[-2]!170
    06/P19750[1]!155
	06/P19625[-2]!140
	06/P18750[1]!70
""")

x = np.arange(19000, 23000)  # グラフを描く�?囲(現�?産価格�?囲?�?
setting(21150, 26, 20190604)  # マ�?�ケ�?ト情報1?�?IV26?�?と仮定�?
fig, ax = plt.subplots(2, 1)
ax[0].plot(x, np.vectorize(p.v)(x), label='Butterfly_Jun04')

setting(evaluationDate=20190607)  # 日付を7日に経過させたものもグラフ描画
ax[0].plot(x, np.vectorize(p.v)(x), label='Butterfly_Jun7')
ax[0].plot(x, np.vectorize(p.pay)(x), label='Payoff', linestyle="dashed")
ax[0].legend(loc="best")
# ax[0].axis('off')

data = []

for op, num in zip(p.items, p.nums):
    data.append(op.getGreeks(num))

subjects = ['δ', 'γ', 'θ', 'κ']
# DataFrameを生�?
df = pd.DataFrame(data, columns=subjects)
# 個人別の平�?を算�?�
# df['mean'] = df.mean(axis=1)
# 教科別の平�?を算�?�
df = df.append(df.sum(axis=0).rename('sum'))
print(df)
# Matplotlibにて表を�?��?
# fig,ax = plt.subplots(figsize=((len(df.columns)+1)*1.2, (len(df)+1)*0.4))
ax[1].axis('off')

tbl = ax[1].table(cellText=df.values,
               bbox=[0, 0, 1, 1],
               colLabels=df.columns,
               rowLabels=df.index)

plt.show()

