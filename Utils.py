'''
Created on 2019/06/05

@author: aokan
'''
import datetime

import QuantLib as ql


def to_date_vector(int_arr):
    tmpvec = ql.DateVector()
    i = 0
    for intdate in int_arr:
        intdate = int(int_arr[i])
        tmpvec.append(ql.Date(intdate))
        i = i + 1
    return tmpvec


def to_real_vector(real_arr):
    tmpvec = ql.DoubleVector()
    i = 0
    for real in real_arr:
        real = float(real_arr[i])
        tmpvec.append(real)
        i = i + 1
    return tmpvec


def pythondate_to_excel_date(pythondate):
    temp = datetime.date(1899, 12, 30)
    delta = pythondate - temp
    intdatetime = int(float(delta.days) + (float(delta.seconds) / 86400))
    return intdatetime
