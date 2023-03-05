
import ccxt
import pandas as pd
import pandas_ta as ta
import numpy as np
import os
from datetime import date, datetime, timezone, tzinfo
import time
import schedule
import numpy as np
import requests
from math import floor
import matplotlib.pyplot as plt
import ta as tl
import math
import functools
from pandas import DataFrame
import warnings
from io import StringIO
from pathlib import Path
from scipy.signal import argrelextrema
from collections import deque
import itertools
import talib.abstract as tt
import talib
warnings.filterwarnings("ignore")
symbol = "ETH/BUSD"  # Binance
pos_size = 1
timeframe = "5m"
pret_y = 0
prechat = 0
initlen = 50
trend = 0
itrend = 0
oss = 0
os1 = 0
upper = 0
lower = 0
top = 0
btm = 0
bear_concordant = True
t=[]
b=[]
it=[]
ib=[]
data=[]
top_y = 0 
top_x = 0
btm_y = 0 
btm_x = 0
show_ibull = 'All'
itop_y = 0 
itop_x = 0
ibtm_y = 0 
ibtm_x = 0
line_style = ['solid','dashed','dotted']
# API TANIMLAMALARI
account_binance = ccxt.binance({
    "apiKey": '',
    "secret": '',
    "enableRateLimit": True,
    'options': {
        'defaultType': 'spot'
    }
})
def high(i, len):
    return dfLB.high[i-len]
def low(i, len):
    return dfLB.low[i-len]
def ta_highest(i, len):
    return dfLB.high[i-len:i].max()
def ta_lowest(i, len):
    return dfLB.low[i-len:i].min()
def ta_crossover(a,b):
    if a>b:
        return True
    else:
        return False
def swings(i, len):
    b=0
    t=0
    upper = ta_highest(i, len)
    lower = ta_lowest(i, len)
    if dfLB.os[i]==0 and dfLB.os[i-1]!=0:
        t=high(i-1, len)
    if dfLB.os[i]==1 and dfLB.os[i-1]!=1:
        b=low(i-1, len)
    data.append([dfLB.time[i-1],high(i-1, len),low(i-1, len), upper,lower,0,len,0,0])
    return [t, b]
def ta_crossunder(a,b):
    return a<b
def ta_pivothigh(i):
    if dfLB.high[i-6:i].argmax()==(i-3):
        return dfLB.high[i-3]
    else:
        return 0
def ta_pivotlow(i):
    if dfLB.low[i-6:i].argmin()==(i-3):
        return dfLB.low[i-3]
    else:
        return 0





try:
    orderTime = datetime.utcnow()
    ohlcvLB = account_binance.fetch_ohlcv(symbol, timeframe)
    dfLB = pd.DataFrame(
        ohlcvLB, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    indiPoint = pd.DataFrame(columns=['time'])
    if len(ohlcvLB):
        dfLB['time'] = pd.to_datetime(dfLB['time'], unit='ms')
    dfLB['os']=0
except Exception as e:
    print(e)
for i in range(initlen+1, len(dfLB)):    
    trail_up = dfLB.high[i]
    trail_dn = dfLB.low[i]
    [top,btm]=swings(i,initlen)
    [itop, ibtm] = swings(i,5)    
i=1
# time,high,low, upper,lower,os,len
while i <len(data):
    data[i][5]=data[i-2][5]
    if data[i][1]>data[i][3]:
        data[i][5]=0
    elif data[i][2]<data[i][4]:
        data[i][5]=1       
    i=i+1 
# print(data)
i=1
while i<int(len(data)/2):
    if data[i*2][5]==0 and data[i*2-2][5]!=0:
        top=data[i*2][1]
    else:
        top=0

    if data[i*2][5]==1 and data[i*2-2][5]!=1:
        btm=data[i*2][2]
    else:
        btm=0
    t.append(top)
    b.append(btm)
    # if data[i*2][6]==5:
    #     print(data[i*2][0],data[i*2][1],data[i*2][2],data[i*2][3],data[i*2][4],data[i*2][5],data[i*2-2][5],top,btm)
    # if data[i*2][6]==50:
    #     print(data[i*2][0],top,btm)
    i=i+1



i=1
while i<int(len(data)/2):
    if data[i*2+1][5]==0 and data[i*2-1][5]!=0:
        top=data[i*2+1][1]
    else:
        top=0

    if data[i*2+1][5]==1 and data[i*2-1][5]!=1:
        btm=data[i*2+1][2]
    else:
        btm=0
    it.append(top)
    ib.append(btm)
    # if data[i*2+1][6]==5:
    #     print(data[i*2+1][0],data[i*2+1][1],data[i*2+1][2],data[i*2+1][3],data[i*2+1][4],data[i*2+1][5],data[i*2-1][5],top,btm)
    
    i=i+1
# 523 line all fixed

top_y = 0
top_x = 0

btm_y = 0
btm_x = 0


itop_y = 0
itop_x = 0

ibtm_y = 0
ibtm_x = 0


top_cross = True
btm_cross = True
pret_c = True
itop_cross = True
ibtm_cross = True

txt_top=''
bull_concordant = True
choch = False 
i=initlen
t_c=[]
t_y=[]
while i<int(len(data)/2-1):
    # print(len(data),i)
    if t[i]>0:
        top_cross = True
        if t[i] > top_y:
            txt_top =  'HH' 
        else : 
            txt_top = 'LH'
        
        top_y = t[i]
        top_x = i - initlen

        trail_up = t[i]
        trail_up_x = i - initlen

    if it[i]>0:
        itop_cross = True
        
        itop_y = it[i]
        itop_x = i - 5



    if b[i]>0:
        btm_cross = True
        if b[i] < btm_y:
            txt_btm =  'LL' 
        else : 
            txt_btm = 'HL'
        
        btm_y = b[i]
        btm_x = i - initlen

        trail_dn = b[i]
        trail_dn_x = i - initlen

    if ib[i]>0:
        ibtm_cross = True
        
        ibtm_y = ib[i]
        ibtm_x = i - 5



    if ta_crossover(dfLB.close[i+initlen], itop_y) and itop_cross and top_y != itop_y and bull_concordant:
        choch = False
        if itrend < 0:
            choch = True
            bull_ichoch_alert = True
        else :
            bull_ibos_alert = True
        if choch:
            txt = 'CHoCH' 
        else : 
            txt ='BOS'
        itrend = 1
        print("GREEN DOTTED    ",itop_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[itop_x+initlen+1],dfLB.time[i+initlen],itop_y,txt)
        itop_cross = False
    if ta_crossover(dfLB.close[i+initlen], pret_y) and pret_c:
        choch = False
        if trend < 0:
            choch = True
            bull_choch_alert = True
        else :
            bull_bos_alert = True
        
        if choch :
            txt = 'CHoCH' 
        else : 
            txt = 'BOS'
        if top_y>0:
            print("GREEN Line      ",top_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[top_x+initlen+1],dfLB.time[i+initlen],top_y,txt)
        top_cross = False
        trend = 1

    if ta_crossunder(dfLB.close[i+initlen], ibtm_y) and ibtm_cross and btm_y != ibtm_y and bear_concordant:
        choch = False
    
        if itrend > 0:
            choch = True
            bear_ichoch_alert = True
        else :
            bear_ibos_alert = True
        if choch:
            txt = 'CHoCH' 
        else : txt ='BOS'
        ibtm_cross = False
        itrend = -1
        print("RED DOTTED      ",ibtm_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[ibtm_x+initlen+1],dfLB.time[i+initlen], ibtm_y,txt)

    if ta_crossunder(dfLB.close[i+initlen], btm_y) and btm_cross:
        choch = False
    
        if trend > 0:
            choch = True
            bear_choch_alert = True
        else :
            bear_bos_alert = True
        if choch:
            txt = 'CHoCH' 
        else : 
            txt ='BOS'
        if prechat!=btm_x+initlen+1:
            print("RED LINE        ",btm_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[btm_x+initlen+1],dfLB.time[i+initlen], btm_y,txt)
        prechat=btm_x+initlen+1


    pret_y=top_y
    pret_c=top_cross

    i=i+1





# 836 line 
