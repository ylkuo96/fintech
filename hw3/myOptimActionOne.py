import numpy as np
import operator

def myOptimActionOne(priceVec, transFeeRate):
	dataLen = len(priceVec)
	actionVec = np.zeros(dataLen)
	conCount = 3
	for ic in range(dataLen):
		if ic + conCount + 1 > dataLen:
			continue
		if all(x > 0 for x in list(map(operator.sub,priceVec[ic+1:ic+1+conCount], priceVec[ic:ic+conCount]))):
			actionVec[ic] = 1
		if all(x < 0 for x in list(map(operator.sub,priceVec[ic+1:ic+1+conCount], priceVec[ic:ic+conCount]))):
			actionVec[ic] = -1
	prevAction = -1
	for ic in range(dataLen):
		if actionVec[ic] == prevAction:
			actionVec[ic] = 0
		elif actionVec[ic] == -prevAction:
			prevAction = actionVec[ic]
	return actionVec
