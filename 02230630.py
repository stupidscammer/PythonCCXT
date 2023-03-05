# 1. OHLC data will be captured with CCXT

# 2.Pandas must be used

# 3. After converting pinescript to python, all output should be displayed in a dataframe


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


initlen = 50

trend = 0
itrend = 0
oss = 0
os1 = 0
upper = 0
lower = 0
top = 0
btm = 0
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


# while True:
try:
    orderTime = datetime.utcnow()
    ohlcvLB = account_binance.fetch_ohlcv(symbol, timeframe)
    dfLB = pd.DataFrame(
        ohlcvLB, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    indiPoint = pd.DataFrame(columns=['time'])
    if len(ohlcvLB):
        dfLB['time'] = pd.to_datetime(dfLB['time'], unit='ms')
        # print(dfLB)  # this is the dataframe
    dfLB['os']=0
except Exception as e:
    print(e)
    # continue

def swings(i, len, os1,oss):
    b=0
    t=0
    oss=0
    upper = ta_highest(i, len)
    lower = ta_lowest(i, len)
    
    if high(i-1, len) > upper:
        oss = 0        
    elif low(i-1, len) < lower:
        oss = 1       
    else:
        oss = dfLB.os[i-1]
    
    if dfLB.os[i]==0 and dfLB.os[i-1]!=0:
        t=high(i-1, len)
    if dfLB.os[i]==1 and dfLB.os[i-1]!=1:
        b=low(i-1, len)

    # if len==50:
    #     print(dfLB.time[i-1],high(i-1, len),low(i-1, len), upper,lower,oss)
    data.append([dfLB.time[i-1],high(i-1, len),low(i-1, len), upper,lower,0,len])
    os1=oss
    return [t, b]


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
for i in range(initlen+1, len(dfLB)):
    bull_choch_alert = False
    bull_bos_alert = False

    bear_choch_alert = False
    bear_bos_alert = False
    top_cross = True
    btm_cross = True
    itop_cross = True
    ibtm_cross = True
    txt_top = ''
    txt_btm = ''
    
    trail_up = dfLB.high[i]
    trail_dn = dfLB.low[i]

    trail_up_x = 0
    trail_dn_x = 0
    trend = 0
    itrend = 0


    top_y = 0
    top_x = 0

    btm_y = 0
    btm_x = 0


    itop_y = 0
    itop_x = 0

    ibtm_y = 0
    ibtm_x = 0

    [top,btm]=swings(i,initlen,os1,oss)
    [itop, ibtm] = swings(i,5,os1,oss)
    
   
def get_top_btm(i,len):
    b=0
    t=0
    if len==50:
        i=i*2
    else:
        i=i*2+1
    if data[i][5]==0 and data[i-1][5]!=0:
        t=data[i][1]
    else:
        t=0
    if data[i][5]==1 and data[i-1][5]!=1:
        b=data[i][2]
    else:
        b=0
    return [t,b]
# print(data)
i=1
# time,high,low, upper,lower,os,len
while i <len(data):
    data[i][5]=data[i-2][5]
    if data[i][1]>data[i][3]:
        data[i][5]=0
    elif data[i][2]<data[i][4]:
        data[i][5]=1
    
        

    # if data[i][6]==50:
    #     print(data[i][0], data[i][1],data[i][2],data[i][3],data[i][4],data[i][5])    
    
    i=i+1

i=1
for i in range(0,int(len(data)/2)):
    [top,btm]=get_top_btm(i,50)
    [itop, ibtm] = get_top_btm(i,5)
    print(data[i*2][0],top,btm,itop, ibtm)