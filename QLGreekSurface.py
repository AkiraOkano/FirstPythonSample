'''
Created on 2019/06/05

@author: aokan
http://www.smileofthales.com/computation/quantlib-python-option-pricing/
'''
import datetime
from math import log

from matplotlib import cm
from matplotlib import ticker
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

import QuantLib as ql
from com.okano.QLAnalytics import QLOption
import com.okano.QLAnalytics
import matplotlib.pyplot as plt
import numpy as np


def ShowChart(xx, yy, zz, output, nbchart, color):

    print ("Plotting " + output + " surface ...")

    ax = fig.add_subplot(3, 4, nbchart, projection='3d')
    ax.set_title(output)

    surf = ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, alpha=0.65, cmap=color, vmin=zz.min(), vmax=zz.max())
    ax.set_xlabel('S')
    ax.set_ylabel('T')
    ax.set_zlabel(output)
    # Plot 3D contour
    zzlevels = np.linspace(zz.min(), zz.max(), num=3, endpoint=True)
    xxlevels = np.linspace(xx.min(), xx.max(), num=3, endpoint=True)
    yylevels = np.linspace(yy.min(), yy.max(), num=3, endpoint=True)
    cset = ax.contour(xx, yy, zz, zzlevels, zdir='z', offset=zz.min(),
    cmap=color, linestyles='dashed')
    cset = ax.contour(xx, yy, zz, xxlevels, zdir='x', offset=xx.min(),
    cmap=color, linestyles='dashed')
    cset = ax.contour(xx, yy, zz, yylevels, zdir='y', offset=yy.max(),
    cmap=color, linestyles='dashed')
    for c in cset.collections:
        c.set_dashes([(0, (2.0, 2.0))])  # Dash contours
    plt.clabel(cset, fontsize=8, inline=1)
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_zlim(zz.min(), zz.max())

    for tick in ax.xaxis.get_major_ticks():
                    tick.label.set_fontsize(6)
    for tick in ax.yaxis.get_major_ticks():
                    tick.label.set_fontsize(6)
    for tick in ax.zaxis.get_major_ticks():
                    tick.label.set_fontsize(6)

    plt.xticks(np.arange(xx.min(), xx.max(), int((xx.max() - xx.min()) / 3)))
    plt.yticks(np.arange(yy.min(), yy.max(), int((yy.max() - yy.min()) / 3)))

    # Colorbar
    colbar = plt.colorbar(surf, shrink=1.0, extend='both', aspect=10)
    l, b, w, h = plt.gca().get_position().bounds
    ll, bb, ww, hh = colbar.ax.get_position().bounds
    colbar.ax.set_position([ll, b + 0.1 * h, ww, h * 0.8])
    tick_locator = ticker.MaxNLocator(nbins=4)
    colbar.locator = tick_locator
    colbar.update_ticks()


if __name__ == '__main__':

    # Pricing parameters
    todaysdate = datetime.date(2015, 4, 21)
    expirydate = datetime.date(2015, 7, 21)

    strike = 5500
    epsilon = 0.20

    shortexpiry = 42145
    longexpiry = 42846

    r = 0.02
    q = 0.01

    ################ Charting: 1st, IV Surface ##################

    data = np.genfromtxt('ImpliedVol.txt')
    # expiry dates
    y = data[:, 0]
    # strikes
    x = data[:, 1]
    # implied volatilities
    z = data[:, 2]

    # expiries chart axis
    uniquemat = np.unique(y)
    end = log(np.max(uniquemat)) / log(uniquemat[0])
    # the expiries axis is arranged in log space
    yi = np.logspace(1, end, len(uniquemat), True, uniquemat[0])

    # #strike chart axis
    xi = np.unique(x)

    X, Y = np.meshgrid(xi, yi)
    # Z = griddata(x, y, z, xi, yi,method='linear')
    # Z = griddata(x, y, z, xi, yi)

    fig = plt.figure()
    # ex: cm.hsv, jet, terrain, rainbow, winter, summer, spring, cool. see http://matplotlib.org/users/colormaps.html
    color = plt.get_cmap('jet')

    ################   Charting: IV Surface    ##################

    ShowChart(X, Y, Y, "IV", 1, color)

    ################  Chart: General settings  ##################

    dx = 10
    dy = 10

    surface = ql.Matrix(len(xi), len(uniquemat))

    dateiter = 0
    strikeiter = 0
    iter = 0

    for volitem in data:
        surface[strikeiter][dateiter] = data[iter, 2] / 100.0
        iter = iter + 1
        dateiter = dateiter + 1
        if (dateiter == len(uniquemat)):
            dateiter = 0
            strikeiter = strikeiter + 1

    xx, yy = np.meshgrid(np.linspace(strike * (1 - epsilon), (1 + epsilon) * strike, dx), np.linspace(shortexpiry, longexpiry, dy))

    ################ Charting: Premium Surface ##################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "PREMIUM"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Premium", 2, color)

    ################  Charting: Delta Surface  ##################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "DELTA"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Delta", 3, color)

    ################  Charting: Gamma Surface  ##################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "GAMMA"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Gamma", 4, color)

    ################  Charting: Vega Surface  ##################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "VEGA"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Vega", 5, color)

    ################  Charting: Theta Surface  ##################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "THETA"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Theta", 6, color)

    ################  Charting: Rho Surface  ####################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "RHO"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Rho", 7, color)

    ################  Charting: DivRho Surface  #################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "DIVRHO"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Div Rho", 8, color)

    ################  Charting: dPdX Surface  ###################

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "DPDSTRIKE"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "dPdX", 9, color)

    ################  Charting: Theta/1day Surface  #############

    zz = np.array([QLOption([todaysdate, ql.Option.Call, y, x, strike, r, q, uniquemat, xi, surface, "THETADAY"]) for
                   x, y in zip(np.ravel(xx), np.ravel(yy))])
    zz = zz.reshape(xx.shape)

    ShowChart(xx, yy, zz, "Theta 1d", 10, color)

    # Show subplots
    plt.show()
