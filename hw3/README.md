# When to Buy or Sell?
## rrEstimateOpen.py
the main program to estimate the rr

## priceMat.txt
the price of four stocks

## myOptimAction.py
- the strategy to try to maximize return rate (rr)
- can see the wholo (future) data, utilize this feature to get the maximum rr!
- I use DP!

### breif description
- priceMat: 
    - An m×n matrix which holds n stocks' price over m days. 
    - That is, each of the n columns is the price vector of m days for a specific stock.
- transFeeRate: Rate for transaction fee, which is usually 1/100.
- actionMat: 
    - An k×4 action matrix which holds k transaction records. 
    - In particular, each row of [d,a,b,z] represents a transaction record, as explained next:
        - d: The index of day, starting from 0 with monotonically increasing values.
        - a: The index of "from" stock, with "-1" being "cash" and all the other integers being stock index (within [0,n−1]).
        - b: The index of "to" stock, with "-1 being "cash" and all the other integers being stock index (within [0,n−1]).
        - z: The equivalent cash for such transaction. This value must be positive.
    - For instance:
        - [5, -1, 7, 100]: 
            - At day 5, use cash of 100 dollars to buy stock 7.
        - [3, 8, -1, 50]: 
            - At day 3, sell stock 8 to have cash of 50(1−ρ), where ρ is the rate for transaction fee.
        - [12, 6, 9, 80]: 
            - At day 12, sell stock 6 and buy stock 9. 
            - Such a transaction between stocks incurs two-time transaction fees. 
            - That is, the cash equivalent of stock 6 you sell is 80(1−ρ), and that of stock 9 you buy is 80(1−ρ)2.

### the DP matrix
- CASH: CMat (dimension: 1*dataLen)
- STOCK: SMat (dimension: 4*dataLen, since there are four stocks)

#### the DP initialization
- CMat[0] = 1000 (original cash is 1000)
- SMat[0][0] = 1000/priceMat[0][0]
- SMat[0][1] = 1000/priceMat[0][1]
- SMat[0][2] = 1000/priceMat[0][2]
- SMat[0][3] = 1000/priceMat[0][3]

#### to fill other DP entries
- assume the ith day:
- CMat[i] = max{yesterday's cash, sell yesterday's stock (there are four
    options) to get cash}
- SMat[i][j] = max{yesterday's stock j, use yesterday's cash to buy stock j, sell other
    stocks (three options) to buy stock j}

### the record matrix (record DP entries)
- CFrom (dimension: 1*dataLen)
    - if yesterday's cash (hold cash): -1
    - if sell yesterday's stock j: j
- SFrom (dimension: 4*dataLen)
    - if yesterday's stock j (hold stock): j
    - if yesterday's cash to buy stock j: -1
    - if sell yesterday's other stock k to buy stock j: k
 
### to run the main program: 
- `$ python rrEstimateOpen.py priceMat.txt 0.01`
- my return rate: 4062975318429.566895%  

