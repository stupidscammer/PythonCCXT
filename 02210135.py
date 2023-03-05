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

except Exception as e:
    print(e)
    # continue



def swings(i, len):
    b=0
    t=0
    upper = ta_highest(i, len)
    lower = ta_lowest(i, len)
    if len==5:
        print(dfLB.time[i-1],high(i-1, len),low(i-1, len), upper,lower,prev_os)
    if high(i-1, len) > upper:
        os1 = 0
        b=0 
        if prev_os == 1:
            t = high(i, len)
    elif low(i-1, len) < lower:
        os1 = 1
        t=0
        if prev_os == 0:
            b = low(i, len)
    # print(t,b)
    prev_os = os1
    
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

    [top,btm]=swings(i,initlen)
    [itop, ibtm] = swings(i,5)
    # print(dfLB.time[i-1], top,btm,itop, ibtm,initlen)
    if top > 0:
        top_cross = True
        txt_top ='LH'
        if top > top_y:
            txt_top ='HH'
        top_y=top
        top_x=i-initlen
    if itop>0:
        itop_cross = True

        itop_y = itop
        itop_x = i - 5
    if dfLB.high[i]>=trail_up:
        trail_up = dfLB.high[i]
    else:
        trail_up = trail_up
    if trail_up == dfLB.high[i]:
        trail_up_x =  i 
    # arguement value for printing
    # x=0
    # y=0
    # txt=''
    # css=''
    # dashed=''
    # # down=''
    # lbl_size=0
    # # print(x,y,txt,css,dashed,down,lbl_size)
    # print(x,y,txt,css,dashed,lbl_size)

    # print(dfLB.time[i], itop_y,itop)
    if ta_crossover(dfLB.close[i], itop_y) and itop_cross and top_y != itop_y and bull_concordant:
        choch = False
        
        if itrend < 0:
            choch = True
            bull_ichoch_alert = True
        else :
            bull_ibos_alert = True
        txt = 'BOS'
        if choch:
            txt = 'CHoCH'

        if True:
            if show_ibull == 'All' or (show_ibull == 'BOS' and not choch) or (show_ibull == 'CHoCH' and choch):
                print("tttt",dfLB.time[i], itop_x,itop_y,txt,"GREY",True,"TINY")
                # display_Structure(itop_x, itop_y, txt, ibull_css, true, true, internal_structure_lbl_size)
        
        itop_cross = False
        itrend = 1
        
    
