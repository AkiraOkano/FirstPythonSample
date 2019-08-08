'''
Created on 2019/06/06

@author: aokan
'''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas.plotting as plotting

df = pd.DataFrame(np.random.randn(5, 5))

fig, ax = plt.subplots(1, 1)
plotting.table(ax, df, loc='center')

ax.axis('off')

plt.show()

#
#
#

# fig = plt.figure()
# ax = fig.add_subplot(111)
# y = [1, 2, 3, 4, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1]
col_labels = ['col1', 'col2', 'col3']
row_labels = ['row1', 'row2', 'row3']
table_vals = [[11, 12, 13], [21, 22, 23], [31, 32, 33]]

the_table = plt.table(cellText=table_vals,
                      colWidths=[0.1] * 3,
                      rowLabels=row_labels,
                      colLabels=col_labels,
                      loc='center right')
the_table.auto_set_font_size(False)
the_table.set_fontsize(24)
the_table.scale(2, 2)

plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
plt.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
for pos in ['right', 'top', 'bottom', 'left']:
    plt.gca().spines[pos].set_visible(False)
# plt.savefig('matplotlib-table.png', bbox_inches='tight', pad_inches=0.05)
plt.show()
