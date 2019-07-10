# coding:utf8
import scipy as sp
import numpy as np
import pandas as pd
import scipy.stats as stats
from scipy import log,sqrt,exp
from sympy import *
from sympy.abc import x,y

D = 30 # debt 负债情况
E = 70 # equity 资产净值
T =1   # maturity 到期
r = 0.07 # risk-free 无风险
sigmaE = 0.4 #volatility of equity 股价波动率

def N(x):
    return stats.norm.cdf(x)

def KMV_f(E,D,T,r,sigmaE):
    n = 10000
    m = 2000
    diffOld = 1e6
    # for i in sp.arange(1,10):
    #     for j in sp.arange(1,m):
    # A = E+D/2+i*D/n  #资产价值 = 股票价值 + 债务
    sigmaA = 0.05 + 2*(1.0-0.001)/2
    # d1 = (log(A/D) + (r+ sigmaA*sigmaA/2)*T)/(sigmaA*sqrt(T))
    # d2 = d1 - sigmaA*sqrt(T)
    # A= (E + D*exp(-r*T)*N(d2))/N(d1)
    output = solve([(E + D*exp(-r*T)*N(y - sigmaA*sqrt(T)))/N(y)-x,log(x/D) + ((r+sigmaA*sigmaA/2)*T)/(sigmaA*sqrt(T))-y],[x,y])
    return output

# print("KMV=",KMV_f(D,E,T,r,sigmaE))
print("KMV=",KMV_f(D=2000,E=10000,T=1,r=0.01,sigmaE=0.2))