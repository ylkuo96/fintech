# Profit Optimization for Trading
> can only look the 'past' data to predict the action

## myStrategy.py
- use brute force to search the parameters
- Explanation of my approach:
    - 1. Technical indicator used: RSI
    - 2. (condition statements)
        - if rsi > alpha and rsi <= x: buy
        - elif rsi < beta and rsi >= y: sell
        - elif rsi > x: sell
        - elif rsi < y: buy
    - 3. Modified parameters: alpha, beta, Nday, x, and y for RSI
    - 4. Use exhaustive search to obtain these parameter values

## run the program
- `$ python rrEstimateAll.py`
- return rate:
    - file=SPY.csv ==> rr=5.709861
    - file=DSI.csv ==> rr=4.885961
    - file=IAU.csv ==> rr=7.044731
    - file=LQD.csv ==> rr=1.705539
    - Average return rate = 4.836523
