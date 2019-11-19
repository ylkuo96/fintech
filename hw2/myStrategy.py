def myStrategy(pastPriceVec, currentPrice, stockType):
    # Explanation of my approach:
    # 1. Technical indicator used: RSI
    # 2. if rsi > alpha and rsi <= x ==> buy
    #    if rsi < beta and rsi >= y ==> sell
    #    if rsi > x ==> sell
    #    if rsi < y ==> buy
    # 3. Modified parameters: alpha, beta, Nday, x, and y for RSI
    # 4. Use exhaustive search to obtain these parameter values

    import numpy as np
    action = 0
    dataLen = len(pastPriceVec)

    # stockType='SPY', 'IAU', 'LQD', 'DSI'
    paramSetting={'DSI': {'alpha':91, 'beta':28, 'Nday':14, 'x':95, 'y':25}, # 4.885961
                  'SPY': {'alpha':72, 'beta':32, 'Nday':26, 'x':77, 'y':30}, # 5.709861
                  'LQD': {'Nday':21, 'alpha':80, 'beta':31, 'x':85, 'y':28}, # 1.705539
    # Current Best Settings: Nday=29, alpha=70, beta=32, x=81, y=30,
    # returnRate=1.789192 X
    # Current Best Settings: Nday=32, alpha=65, beta=33, x=77, y=32,
    # returnRate=1.874861 X
                  'IAU': {'Nday':21, 'alpha':69, 'beta':37, 'x':75, 'y':35}} # 7.044731
    Nday = paramSetting[stockType]['Nday']
    alpha = paramSetting[stockType]['alpha']
    beta = paramSetting[stockType]['beta']
    x = paramSetting[stockType]['x']
    y = paramSetting[stockType]['y']

    if dataLen < Nday:
        return action

    usedData = pastPriceVec[-(Nday+1):]

    SMAu = 0
    SMAd = 0
    prev = usedData[0]
    for idx in range(len(usedData)):
        curr = usedData[idx]
        if curr > prev:
            SMAu = SMAu + (curr - prev)
        if curr < prev:
            SMAd = SMAd + (prev - curr)
        prev = curr

    rsi = SMAu/(SMAu+SMAd)

    if (rsi*100 > alpha) and (rsi*100 <= x):
        action = 1
    elif (rsi*100 < beta) and (rsi*100 >= y):
        action = -1
    elif rsi*100 > x:
        action = -1
    elif rsi*100 < y:
        action = 1

    return action
