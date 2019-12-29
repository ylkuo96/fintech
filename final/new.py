import os, sys, math
import sys
import numpy as np
import pandas as pd

dailyOhlcv = pd.read_csv('ohlcv_daily.csv')
minutelyOhlcv = pd.read_csv('ohlcv_minutely.csv')

def myStrategy(daily, minutely, openpricev, lday, sday, lwin, swin):
    # default
    action = 0

    # close
    tmp = daily["close"]
    dataLen = len(tmp)
    pastPriceVec = np.zeros(dataLen)
    for i in range(dataLen):
        pastPriceVec[i] = tmp[i]

    SusedData = pastPriceVec[-(sday+1):]
    LusedData = pastPriceVec[-(lday+1):]

    SMAu = 0
    SMAd = 0
    prev = SusedData[0]
    for idx in range(len(SusedData)):
        curr = SusedData[idx]
        if curr > prev:
            SMAu = SMAu + (curr - prev)
        if curr < prev:
            SMAd = SMAd + (prev - curr)
        prev = curr

    Srsi = SMAu/(SMAu+SMAd) * 100.0

    SMAu = 0
    SMAd = 0
    prev = LusedData[0]
    for idx in range(len(LusedData)):
        curr = LusedData[idx]
        if curr > prev:
            SMAu = SMAu + (curr - prev)
        if curr < prev:
            SMAd = SMAd + (prev - curr)
        prev = curr

    Lrsi = SMAu/(SMAu+SMAd) * 100.0

    if Srsi >= Lrsi:
        RSI = True
    else:
        RSI = False

    ## MA
    windowS = swin
    windowL = lwin

    windowedDataS = pastPriceVec[-windowS:]
    windowedDataL = pastPriceVec[-windowL:]

    maS = np.mean(windowedDataS)
    maL = np.mean(windowedDataL)

    if maS >= maL:
        MA = True
    else:
        MA = False

    ## conclusion
    if RSI == True:
        action = 1
    elif RSI == False and MA == False:
        action = -1

    return action

def evaluate(l, s, lwin, swin):
    capital = 500000.0
    capitalOrig=capital
    transFee = 100
    evalDays = 14
    action = np.zeros((evalDays,1))
    realAction = np.zeros((evalDays,1))
    total = np.zeros((evalDays,1))
    total[0] = capital
    Holding = 0.0
    openPricev = dailyOhlcv["open"].tail(evalDays).values
    clearPrice = dailyOhlcv.iloc[-3]["close"]

    for ic in range(evalDays,0,-1):
        dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
        dateStr = dailyOhlcvFile.iloc[-1,0]
        minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
        action[evalDays-ic] = myStrategy(dailyOhlcvFile, minutelyOhlcvFile, openPricev[evalDays-ic], l, s, lwin, swin)
        currPrice = openPricev[evalDays-ic]
        if action[evalDays-ic] == 1:
            if Holding == 0 and capital > transFee:
                Holding = (capital-transFee)/currPrice
                capital = 0
                realAction[evalDays-ic] = 1
        elif action[evalDays-ic] == -1:
            if Holding > 0 and Holding*currPrice > transFee:
                capital = Holding*currPrice - transFee
                Holding = 0
                realAction[evalDays-ic] = -1
        elif action[evalDays-ic] == 0:
            realAction[evalDays-ic] = 0
        else:
            assert False
        if ic == 3 and Holding > 0: #遇到每個月的第三個禮拜三要平倉，請根據data的日期自行修改
            capital = Holding*clearPrice - transFee
            Holding = 0

        total[evalDays - ic] = capital + float(Holding > 0) * (Holding * currPrice - transFee)

    returnRate = (total[-1] - capitalOrig)/capitalOrig
    return returnRate


