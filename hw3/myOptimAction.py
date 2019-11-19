import numpy as np

def myOptimAction(priceMat, transFeeRate):
    # user definition
    dataLen, stockCount = priceMat.shape # 3236, 4
    actionMat = []

    # default
    cash = 1000

    ## DP
    # stock/cash matrix
    CMat, SMat = np.zeros(dataLen), np.zeros((dataLen, stockCount))
    # where the cash/stock comes from
    CFrom, SFrom = np.zeros(dataLen), np.zeros((dataLen, stockCount))

    # DP matrix initialization
    CMat[0] = cash
    SMat[0][0] = cash*(1-transFeeRate)/priceMat[0][0]
    SMat[0][1] = cash*(1-transFeeRate)/priceMat[0][1]
    SMat[0][2] = cash*(1-transFeeRate)/priceMat[0][2]
    SMat[0][3] = cash*(1-transFeeRate)/priceMat[0][3]

    # fill the DP table
    for i in range(1, dataLen):
        dayPrices = priceMat[i]

        ## optimal cash
        holdCash, sellStockCash, which = 0, 0, -1
        for j in range(stockCount):
            # two options: {yesterday's cash, sell stock to get cash}
            hold = CMat[i-1]
            sell = SMat[i-1][j]*(dayPrices[j])*(1-transFeeRate)

            if hold > holdCash:
                holdCash = hold

            if sell > sellStockCash:
                sellStockCash = sell
                which = j

        maxCash = max(holdCash, sellStockCash)
        if maxCash == holdCash:
            CMat[i] = holdCash
            CFrom[i] = -1 # cash
        elif maxCash == sellStockCash:
            CMat[i] = sellStockCash
            CFrom[i] = which # stock

        ## optimal stock
        for j in range(stockCount):
            # three options:
            # {yesterday's stock, buy stock with cash, sell other stock and buy
            # the specific stock}
            holdStock = SMat[i-1][j]
            buyWithCash = CMat[i-1]*(1-transFeeRate)/dayPrices[j]
            sellOtherStock, which = 0, -1
            for k in range(stockCount):
                if k != j:
                    val = SMat[i-1][k]*dayPrices[k]*(1-transFeeRate)
                    val = val*(1-transFeeRate)/dayPrices[j]
                    if val > sellOtherStock:
                        sellOtherStock, which = val, k

            maxStock = max(holdStock, buyWithCash, sellOtherStock)
            if maxStock == holdStock:
                SMat[i][j] = holdStock
                SFrom[i][j] = j # stock j
            elif maxStock == sellOtherStock:
                SMat[i][j] = sellOtherStock
                SFrom[i][j] = which # stock k
            elif maxStock == buyWithCash:
                SMat[i][j] = buyWithCash
                SFrom[i][j] = -1 # cash

    ## fill action matrix
    reversedAction = []

    # the best solution
    bestVal = CMat[-1]
    where = CFrom[-1]
    toType = 'C'

    # trace back
    i == dataLen-1
    while(i >= 0):
        if toType == 'C':
            if where == -1: # hold cash
                toType = 'C'
                bestVal = CMat[i]
                where = CFrom[i]
            else: # sell stock to get cash
                toType = 'S'
                idx = int(where)
                equivCash = SMat[i][idx]*priceMat[i+1][idx]
                bestVal = SMat[i][idx]
                where = SFrom[i][idx]
                reversedAction.append([i+1, idx, -1, equivCash])
                #print([i+1, idx, -1, equivCash])
        else: # toType == 'S'
            if where == -1: # use cash to buy stock
                to = -5
                for j in range(stockCount):
                    if CMat[i]*(1-transFeeRate)/priceMat[i+1][j] == bestVal:
                        to = j
                        break
                reversedAction.append([i+1, -1, to, CMat[i]])
                #print([i+1, -1, to, CMat[i]/(1-transFeeRate)])
                toType = 'C'
                bestVal = CMat[i]
                where = CFrom[i]
            else: # hold stock, or sell other stock to buy stock
                toType = 'S'
                idx = int(where)
                if SMat[i][idx] == bestVal: # hold stock
                    bestVal = SMat[i][idx]
                    where = SFrom[i][idx]
                else: # sell other stock to buy stock
                    to = -5
                    for k in range(stockCount):
                        if idx != k:
                            tmp = SMat[i][idx]*priceMat[i+1][idx]*(1-transFeeRate)
                            tmp = tmp*(1-transFeeRate)/priceMat[i+1][k]
                            if tmp == bestVal:
                                to = k
                                break

                    equivCash = SMat[i][idx]*priceMat[i+1][idx]
                    reversedAction.append([i+1, idx, to, equivCash])
                    #print([i+1, idx, to, equivCash])
                    bestVal = SMat[i][idx]
                    where = SFrom[i][idx]

        i = i-1

    for i in reversed(range(len(reversedAction))):
        actionMat.append(reversedAction[i])
        #print(reversedAction[i])

    return actionMat
