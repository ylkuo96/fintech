# Trading Strategy for 台指期

## evaluate performance formula
- `$ python projectEval.py ohlcv_daily.csv ohlcv_minutely.csv`
- TA gives us projectEval.py 

## myStrategy.py
- write by myself
- projectEval.py will call this code to evaluate the performance
- my strategy:
    - use RSI and MA these two technical indicators
    - short RSI set 14 days; long RSI set 20 days
    - short windowSize for MA set 20 days; long windowSize for MA set 60 days
    - if short RSI \geq long RSI then buy
        - buy for loose condition
        - since the election is coming, I predict the overall stock will continue to increase :P 
    - if short RSI < long RSI and short MA < long MA then sell
        - sell for strict condition

## new.py
- copy evaluate and myStrategy 

## run.py
- use 12 threads to call the 'evaluate' function in new.py
- use brute force to search the best return rate and the best parameters
- `$ python run.py`
