def myStrategy(daily, minutelyOhlcvFile, openPrice):
    import numpy as np
    #from talib import abstract

    # default
    action = 0

    # close
    tmp = daily["close"]
    dataLen = len(tmp)
    pastPriceVec = np.zeros(dataLen)
    for i in range(dataLen):
        pastPriceVec[i] = tmp[i]

    """
    # high
    tmp = daily["high"]
    dataLen = len(tmp)
    high = np.zeros(dataLen)
    for i in range(dataLen):
        high[i] = tmp[i]

    # low
    tmp = daily["low"]
    dataLen = len(tmp)
    low = np.zeros(dataLen)
    for i in range(dataLen):
        low[i] = tmp[i]
    """

    ## rsi
    sday = 14
    lday = 20

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
    windowS = 20
    windowL = 60

    windowedDataS = pastPriceVec[-windowS:]
    windowedDataL = pastPriceVec[-windowL:]

    maS = np.mean(windowedDataS)
    maL = np.mean(windowedDataL)

    if maS >= maL:
        MA = True
    else:
        MA = False

    """
    ## KD
    K, D = abstract.STOCH(high, low, pastPriceVec, fastk_period=9)

    ktoday = K[-1]; dtoday = D[-1]
    kprev = K[-2]; dprev = D[-2]

    if ktoday >= kprev and ktoday >= dtoday:
        KD = True
    else:
        KD = False
    """

    ## conclusion
    if RSI == True:
        action = 1
    elif RSI == False and MA == False:
        action = -1

    return action

