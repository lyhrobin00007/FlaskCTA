# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 14:08:57 2016

@author: 020242
"""
#import ChinaCalendar
#from QuantLib import *
#import datetime
#import csv
#import pandas as pd
import numpy as np
from time import time
from random import gauss, seed
import random
from math import exp, sqrt, log

from numba import jit


#=====================================================
#FR007IRS5Y 2016-12-01
@jit
def calcMC(S0,sigma,r,dt,M,I):
    
    S = [None] * I
    for i in range(I):
        S[i] = [0]*(M+1)
    #end for

    
    for i in range(I):
        path = S[i]
        for t in range(M+1):
            if t == 0:
                path[t] = S0
            else:
#                z = gauss(0.0,1.0)
                z = random.normalvariate(0.0,1.0)
                St = path[t-1] * exp((r - 0.05 * sigma ** 2) * dt + sigma * sqrt(dt) * z)
                path[t] = St
            #end if
        #end for
        S[i] = path
    #end for
    return S
#end def


#S0 = 0.0357
#S0 = 0.029893 #十年国债收益率
S0 = 0.029893
#T = 91. / 365
T = 0.25
#sigma = 0.103993516
#sigma = 0.056285 #十年国债年化波动率
sigma = 0.13
#sigma = 0.2
r = 0.027
M = 91
dt = T / M
I = 250000
firmRate = 0.0372

#seed(20000)

S = calcMC(S0,sigma,r,dt,M,I)

#------------------------------------------------------
#Type 1: Down and Out Alternative
#1. 如果未曾触发敲出时事件，年化收益率R0
#2. 如果敲出，且期末收益率水平大院100%，年化收益率R0
#3. 如果敲出，且期末收益率水平小于100%， 年化收益率0

knockOut = 0.95
R0 = 0.04

p1 = float(sum([min(path) > S0 * knockOut for path in S])) / I
p2 = float(sum([min(path) < S0 * knockOut and path[-1] >= S0 for path in S])) / I
p3 = float(sum([min(path) < S0 * knockOut and path[-1] < S0 for path in S])) / I

optionPrice = R0 * (p1+p2) + 0 * p3
print 'knock-out option %.10f, base rate: %.10f'%(optionPrice,firmRate - optionPrice)


#------------------------------------------------------
#Type 2: Double No Touch
#1. 如果未曾触发敲出时事件，年化收益率R0
#3. 如果敲出，且期末收益率水平小于100%， 年化收益率0

knockOut1 = 0.95
knockOut2 = 1.05
R0 = 0.03

p1 = float(sum([min(path) > S0 * knockOut1 and min(path) < S0 * knockOut2 for path in S])) / I
p2 = float(sum([min(path) < S0 * knockOut1 or min(path) > S0 * knockOut2 for path in S])) / I

optionPrice = R0 * p1 + 0 * p2
print 'double-no-touch option %.10f, base rate: %.10f'%(optionPrice,firmRate - optionPrice)


#------------------------------------------------------
#Type 3: Out of range rate
#1. 最终受益=超出规定范围的天数/总天数 *Ｒ０

range1 = 0.95
range2 = 1.05
R0 = 0.03

p1 = sum([float(sum([i >= S0 * range1 and i <= S0 * range2 for i in path])) / (M+1) for path in S]) / I
#p2 = sum([float(sum([i > S0 * range2 or i < S0 * range1 for i in path])) / (M+1) for path in S]) / I

optionPrice = R0 * p1
print 'out-of-range option %.10f, base rate: %.10f'%(optionPrice,firmRate - optionPrice)

#------------------------------------------------------
#Type 4: 温和看涨期权
#1. 如果未曾触发敲出时事件，年化收益率为max(0,期末价格/期初价格-100%)
#2. 如果敲出，且期末收益率水平大院100%，年化收益率0

knockOut = 1.1
R0 = 0.01

payOff = []
for path in S:
    if max(path) > S0 * knockOut:
        payOff.append(R0)
    else:
        payOff.append(max(path[-1] / S0 - 1,0))
    #end if
#end for
        
p1 = float(sum([max(path) >= S0 * knockOut for path in S])) / I
p2 = float(sum([max(path) < S0 * knockOut and path[-1] <= S0 for path in S])) / I
p3 = float(sum([max(path) < S0 * knockOut and path[-1] > S0 for path in S])) / I

#p2 = sum([float(sum([i > S0 * range2 or i < S0 * range1 for i in path])) / (M+1) for path in S]) / I

optionPrice = np.mean(payOff)
print '温和看涨期权: %.10f, base rate: %.10f'%(optionPrice,firmRate - optionPrice)

#------------------------------------------------------
#Type 5: call-spread

baseRate = 0
participationRate = 0.75
point1 = 1
point2 = 1.1

#payOff = float(sum([baseRate + np.min((knockOut2-knockOut1)*participationRate,np.max((path[-1] / S0 - 1) * participationRate,0)) for path in S])) / I

payOff = []
for path in S:
    if path[-1] <= S0 * point1:
        payOff.append(baseRate*T)
    elif path[-1] >= S0 * point2:
        payOff.append((baseRate + (point2-point1)*participationRate)*T)
    else:
        payOff.append((baseRate + (path[-1] / S0 - point1) * participationRate)*T)
    #end if
#end for

p1 = float(sum([max(path) <= S0 * point1 for path in S])) / I
p2 = float(sum([max(path) > S0 * point1 and path[-1] < S0 * point2 for path in S])) / I
p3 = float(sum([max(path) >= S0 * point2 for path in S])) / I

#p2 = sum([float(sum([i > S0 * range2 or i < S0 * range1 for i in path])) / (M+1) for path in S]) / I

optionPrice = np.mean(payOff)
print 'call-spread: %.10f, base rate: %.10f'%(optionPrice,firmRate - optionPrice)
#
##------------------------------------------------------
##Type 6: call
#
##payOff = []
##for path in S:
##    if path[-1] <= S0 * point1:
##        payOff.append(baseRate*T)
##    elif path[-1] >= S0 * point2:
##        payOff.append((baseRate + (point2-point1)*participationRate)*T)
##    else:
##        payOff.append((baseRate + (path[-1] / S0 - point1) * participationRate)*T)
##    #end if
###end for
##
##p1 = float(sum([max(path) <= S0 * point1 for path in S])) / I
##p2 = float(sum([max(path) > S0 * point1 and path[-1] < S0 * point2 for path in S])) / I
##p3 = float(sum([max(path) >= S0 * point2 for path in S])) / I
#
##p2 = sum([float(sum([i > S0 * range2 or i < S0 * range1 for i in path])) / (M+1) for path in S]) / I
#
#optionPrice = float(sum([max(0.0,path[-1] / S0 - 1) for path in S])) / I
#print 'call: %.10f, base rate: %.10f'%(optionPrice,firmRate - optionPrice)
