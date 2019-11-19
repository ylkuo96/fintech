# This function is used by TA to evaluate your performance. You are not allowed to submit this function.
import sys
import numpy as np
import pandas as pd
from myOptimActionOne import myOptimActionOne

# Estimate return rate over a given price vector
def rrEstimateOneOpen(priceVec, transFeeRate, actionVec):
	capital=1000	# Initial available capital
	capitalOrig=capital		# original capital
	dataCount=len(priceVec)				# day size
	suggestedAction=actionVec
	stockHolding=np.zeros((dataCount,1))  	# Vec of stock holdings
	total=np.zeros((dataCount,1))	 	# Vec of total asset
	realAction=np.zeros((dataCount,1))	# Real action, which might be different from suggested action. For instance, when the suggested action is 1 (buy) but you don't have any capital, then the real action is 0 (hold, or do nothing). 
	# Run through each day
	for ic in range(dataCount):
		currentPrice=priceVec[ic]	# current price
		if ic>0:
			stockHolding[ic]=stockHolding[ic-1]	# The stock holding from the previous day
		if suggestedAction[ic]==1:	# Suggested action is "buy"
			if stockHolding[ic]==0:		# "buy" only if you don't have stock holding
				stockHolding[ic]=capital*(1-transFeeRate)/currentPrice # Buy stock using cash
				capital=0	# Cash
				realAction[ic]=1
		elif suggestedAction[ic]==-1:	# Suggested action is "sell"
			if stockHolding[ic]>0:		# "sell" only if you have stock holding
				capital=stockHolding[ic]*currentPrice*(1-transFeeRate) # Sell stock to have cash
				stockHolding[ic]=0	# Stocking holding
				realAction[ic]=-1
		elif suggestedAction[ic]==0:	# No action
			realAction[ic]=0
		else:
			assert False
		total[ic]=capital+stockHolding[ic]*currentPrice*(1-transFeeRate)
	returnRate=(total[-1]-capitalOrig)/capitalOrig		# Return rate of this run
	return returnRate

# How to invoke this program: python rrEstimateOpenOne.py data\SPY.csv 0.01
if __name__ == "__main__":
	print("Reading %s..." %(sys.argv[1]))
	df=pd.read_csv(sys.argv[1])
	transFeeRate=float(sys.argv[2])
	priceVec=df["Adj Close"].values
	actionVec=myOptimActionOne(priceVec, transFeeRate)
	rr=rrEstimateOneOpen(priceVec, transFeeRate, actionVec)
	print("rr=%f%%" %(rr*100))
