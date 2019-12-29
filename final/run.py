import concurrent.futures
import math
from new1 import *

LRange = range(16, 70)

def search(l):
    bestRR = 0
    bestL = 0
    bestS = 0
    bestLw = 0
    bestSw = 0
    for s in range(3, 32):
        if s >= l:
            continue

        lwin = 60; swin = 20
        rr = evaluate(l, s, lwin, swin)
        if rr > bestRR:
            bestRR = rr
            bestL = l
            bestS = s
            bestLw = lwin
            bestSw = swin

    return bestRR, bestL, bestS, bestLw, bestSw

def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=12) as executor:
        for l, ret in zip(LRange, executor.map(search, LRange)):
            print("best rr:", ret[0], "best rsil:", ret[1], "best rsis:", ret[2], "best mal:", ret[3], "best mas:", ret[4])

if __name__ == '__main__':
    main()
