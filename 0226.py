
import ccxt
import pandas as pd
import pandas_ta as ta
import numpy as np
import os
from datetime import date, datetime, timezone, tzinfo,timedelta
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
ob_filter = 'Atr'
target_top=[]
target_btm=[]
target_left=[]
target_type=[]
# line_style = ['solid','dashed','dotted']
# API TANIMLAMALARI


account_binance = ccxt.binance({
    "apiKey": '',
    "secret": '',
    "enableRateLimit": True,
    'options': {
        'defaultType': 'spot'
    }
})
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
dfLB['atr']=0
enddate=dfLB.time[len(dfLB)-1]+timedelta(minutes=100)
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
    if dfLB.high[i-6:i+1].argmax()==3:
        return dfLB.high[i-3]
    else:
        return 0
def ta_pivotlow(i):
    if dfLB.low[i-6:i+1].argmin()==3:
        return dfLB.low[i-3]
    else:
        return 0
def ta_wma(j,length) :
    norm = 0.0
    sum = 0.0
    for i in range(j-length, j - 1):
        weight = (length - i) * length
        norm = norm + weight
        tr=max(abs(dfLB.high[i]-dfLB.close[i]),abs(dfLB.high[i]-dfLB.close[i-1]),abs(dfLB.low[i]-dfLB.close[i-1]))
        sum = sum + tr * weight
    return sum / norm

def ta_ema(j,length) :
    alpha = 2 / (length + 1)
    sum=ta_sma(length+1,length)
    for i in range(length+2, j):
        print(i)
        tr=max(abs(dfLB.high[i]-dfLB.close[i]),abs(dfLB.high[i]-dfLB.close[i-1]),abs(dfLB.low[i]-dfLB.close[i-1]))
        sum = alpha * tr + (1 - alpha) * sum
    return sum

def ta_sma(j,length) :
    sum = 0.0
    for i  in range(j-length, j - 1):
        tr=max(abs(dfLB.high[i]-dfLB.close[i]),abs(dfLB.high[i]-dfLB.close[i-1]),abs(dfLB.low[i]-dfLB.close[i-1]))
        sum += tr / length
    return sum
def fullatr(time,val):
    idx=0
    for i in range(0,len(dfLB)-1):
        datastr=dfLB.time[i].strftime('%Y-%m-%d %H:%M:%S')
        if datastr==time:
            dfLB.atr[i]= val 
            idx=i           
            break
    for i in range(idx+1,len(dfLB)-1):
        tr=max(abs(dfLB.high[i]-dfLB.low[i]),abs(dfLB.high[i]-dfLB.close[i-1]),abs(dfLB.low[i]-dfLB.close[i-1]))
        # print(dfLB.time[i],dfLB.high[i],dfLB.close[i],tr)
        dfLB.atr[i]=(dfLB.atr[i-1]*199+tr)/200
    i=idx-1
    while i>0:
        tr=max(abs(dfLB.high[i+1]-dfLB.low[i+1]),abs(dfLB.high[i+1]-dfLB.close[i]),abs(dfLB.low[i+1]-dfLB.close[i]))
        # print(dfLB.time[i],tr)
        dfLB.atr[i]=(dfLB.atr[i+1]*200-tr)/199 
        i=i-1
def ob_coord(j,use_max,loc,addin,cls):
            #  ,use_max, loc, target_top, target_btm, target_left, target_type):
    minval = 99999999.
    maxval = 0.
    idx = 1
    # print(dfLB.atr[j])
# j is current
    # if ob_filter == 'Atr' :
    #     ob_threshold =dfLB.atr[j] 
    # else:
    #     ob_threshold =cmean_range
    if use_max:
        for i in range(1,loc-1) :
            if (dfLB.high[j-i] - dfLB.low[j-i] ) < dfLB.atr[j-i] * 2:
                maxval = max(dfLB.high[j-i], maxval)
                if  maxval == dfLB.high[j-i]:
                    minval = dfLB.low[j-i] 
                    idx = i
                else:
                    minval = minval
    else:
        for i in range(1,loc-1):
            if (dfLB.high[j-i] - dfLB.low[j-i] ) < dfLB.atr[j-i] * 2:
                minval = min(dfLB.low[j-i] , minval)
                if minval== dfLB.low[j-i] :
                    maxval = dfLB.high[j-i] 
                    idx = i
                else : 
                    maxval = maxval
    target_top.append(maxval)
    target_btm.append(minval)
    target_left.append(j-idx)
    if use_max:
        target_type.append(-1)
    else:
        target_type.append(1)
    
def revomveob(i):
    for j in range(0,len(target_type)-1):
        if target_type[j]==1:
            if dfLB.close[i]<target_btm[j]:
                target_type[j]=0
        elif dfLB.close[i]>target_btm[j]:
            target_type[j]=0


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
atrarray=[]
fullatr("2023-02-28 23:20:00",2.9566639859)
while i<int(len(data)/2-1):
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
        itop_cross = False
        print("GREEN DASH        ",itop_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[itop_x+initlen+1],dfLB.time[i+initlen],itop_y,txt)
        ob_coord(i+initlen,False,i-1-itop_x,itop_x,dfLB.close[i+initlen])
        
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
            print("GREEN SOLID       ",top_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[top_x+initlen+1],dfLB.time[i+initlen],top_y,txt)
        ob_coord(i+initlen,False, i-1-top_x,top_x,dfLB.close[i+initlen])
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
        print("RED DASH          ",ibtm_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[ibtm_x+initlen+1],dfLB.time[i+initlen], ibtm_y,txt)
        ob_coord(i+initlen,True, i-1-ibtm_x, ibtm_x,dfLB.close[i+initlen])
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
            print("RED SOLID         ",btm_x+initlen+1,"-",i+initlen,"Time:",dfLB.time[btm_x+initlen+1],dfLB.time[i+initlen], btm_y,txt)
        # ob_coord(i+initlen,True, i-1-btm_x, btm_x,dfLB.close[i+initlen])
        prechat=btm_x+initlen+1  
             
    pret_y=top_y
    pret_c=top_cross
    i=i+1
    trail_up=max(dfLB.high[i],trail_up)
    if(trail_up==dfLB.high[i]):
        trail_up_x =i 
    revomveob((i+initlen))
print("Weak " , trail_up)
i=7
eq_prv_top=0
eq_top_x = 0
eq_prv_btm = 0.
eq_btm_x = 0
while i<len(dfLB):        
    if i>7:
        eq_top = ta_pivothigh(i)
        eq_btm = ta_pivotlow(i)        
        if eq_top>0:
            if eq_top > eq_prv_top:
                eq_max=eq_top
                eq_min=eq_prv_top
            else:
                eq_max=eq_prv_top
                eq_min=eq_top

            if eq_max<(eq_min+dfLB.atr[i]*0.1):
                print("EQH RED DOT       ",eq_top_x,"-",i-3,"Time:", dfLB.time[eq_top_x],"(",eq_prv_top,")","-",dfLB.time[i-3],"(",   eq_top,")")            
            eq_prv_top=eq_top
            eq_top_x=i-3
        if eq_btm>0:
            if eq_btm > eq_prv_btm:
                eq_max=eq_btm
                eq_min=eq_prv_btm
            else:
                eq_max=eq_prv_btm
                eq_min=eq_btm
            if eq_min>(eq_max-dfLB.atr[i]*0.1):
                print("EQL GREEN DOT     ",eq_btm_x,"-",i-3,"Time:", dfLB.time[eq_btm_x],"(",eq_prv_btm,")","-",dfLB.time[i-3],"(",   eq_btm,")")  
            eq_prv_btm=eq_btm
            eq_btm_x=i-3
    i=i+1

for i in range(0,len(target_btm)-1):
    if target_type[i]==-1:
        print("RED type ",dfLB.time[target_left[i]],enddate,target_btm[i],target_top[i])
    elif target_type[i]==1:
        print("GREY type ",dfLB.time[target_left[i]],enddate,target_btm[i],target_top[i])