'''
Created on 2019/06/03

@author: aokan
'''

from simpleOption import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

op = Option('06/C21000')
op.v(21120, 15.78 , 20190612)
print(f'delta= {op.delta():.2}')
print(f'gamma= {op.gamma():.2}')
print(f'thetaPerDay= {op.thetaPerDay():.2f}')
print(f'vega= {op.vega():.2f}')

