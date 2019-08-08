'''
Created on 2019/06/03

@author: aokan
'''
import math

from matplotlib import pyplot

import numpy as np

pi = math.pi  # mathモジュールの�?を利用

x = np.linspace(0, 2 * pi, 100)  # 0から2�?までの�?囲�?100�?割したnumpy配�??
y = np.sin(x)

pyplot.plot(x, y)
pyplot.show()
